import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
    FunctionTransformer,
)
from sklearn.impute import SimpleImputer

# Output artifact directory for plots and saved models.
os.makedirs("plots", exist_ok=True)

DATA_PATH = "Instagram_Analytics.csv"
TARGET_COLUMN = "engagement_rate"
RANDOM_STATE = 42

# Explicit feature groups for professional preprocessing.
SKEWED_NUMERIC_FEATURES = [
    "follower_count",
    "caption_length",
    "hashtags_count",
    "likes",
    "comments",
    "shares",
    "saves",
    "followers_gained",
    "engagement",
    "reach",
    "impressions",
    "reach_impression_ratio",
]

LINEAR_NUMERIC_FEATURES = [
    "post_hour",
]

BINARY_FEATURES = [
    "has_call_to_action",
]

CATEGORICAL_FEATURES = [
    "content_category",
    "media_type",
    "traffic_source",
    "day_of_week",
    "posting_period",
]

MODEL_FEATURES = SKEWED_NUMERIC_FEATURES + LINEAR_NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATURES


def load_dataset(path: str) -> pd.DataFrame:
    """Load the dataset and normalize column names."""
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create consistent time-based features for the posting hour and weekday."""
    df["post_hour"] = pd.to_numeric(df["post_hour"], errors="coerce").fillna(0).astype(int).clip(0, 23)

    def get_posting_period(hour: int) -> str:
        if hour < 5:
            return "Late Night"
        if hour < 12:
            return "Morning"
        if hour < 17:
            return "Afternoon"
        if hour < 21:
            return "Evening"
        return "Night"

    df["posting_period"] = df["post_hour"].apply(get_posting_period)
    df["day_of_week"] = df["day_of_week"].fillna("Unknown").astype(str)
    return df


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values in both numeric and categorical features."""
    df["has_call_to_action"] = df["has_call_to_action"].fillna(0).astype(int)
    df["followers_gained"] = pd.to_numeric(df["followers_gained"], errors="coerce")
    df["followers_gained"] = df["followers_gained"].fillna(df["followers_gained"].median())

    for col in [
        "follower_count",
        "post_hour",
        "caption_length",
        "hashtags_count",
        "likes",
        "comments",
        "shares",
        "saves",
        "reach",
        "impressions",
        "engagement",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["reach"] = df["reach"].fillna(df["reach"].median())
    df["impressions"] = df["impressions"].fillna(df["impressions"].median())

    for col in [
        "content_category",
        "media_type",
        "traffic_source",
        "day_of_week",
        "posting_period",
    ]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").astype(str)

    return df


def correct_data_inconsistencies(df: pd.DataFrame) -> pd.DataFrame:
    """Fix domain-specific inconsistencies such as reach > impressions."""
    if (df["reach"] > df["impressions"]).any():
        df.loc[df["reach"] > df["impressions"], "reach"] = df.loc[
            df["reach"] > df["impressions"], "impressions"
        ]

    df["engagement_rate"] = pd.to_numeric(df["engagement_rate"], errors="coerce")
    df["engagement_rate"] = df["engagement_rate"].clip(0.0, 1.0)

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create secondary social media features for more realistic model context."""
    if "engagement" not in df.columns:
        df["engagement"] = df[["likes", "comments", "shares", "saves"]].sum(axis=1)

    df["reach_impression_ratio"] = df["reach"] / df["impressions"].replace(0, np.nan)
    df["reach_impression_ratio"] = df["reach_impression_ratio"].fillna(0).clip(0, 1)

    return df


def cap_extreme_values(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Limit the influence of extreme outliers while keeping viral posts intact."""
    for col in columns:
        if col not in df.columns:
            continue
        lower = df[col].quantile(0.01)
        upper = df[col].quantile(0.99)
        df[col] = df[col].clip(lower, upper)
    return df


def build_preprocessing_pipeline() -> ColumnTransformer:
    """Build the numeric and categorical preprocessing pipeline."""
    skewed_numeric_transformer = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("log_transform", FunctionTransformer(np.log1p, validate=False)),
            ("scaler", StandardScaler()),
        ]
    )

    linear_numeric_transformer = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    boolean_transformer = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            (
                "skewed_numeric",
                skewed_numeric_transformer,
                SKEWED_NUMERIC_FEATURES,
            ),
            (
                "linear_numeric",
                linear_numeric_transformer,
                LINEAR_NUMERIC_FEATURES,
            ),
            ("binary", boolean_transformer, BINARY_FEATURES),
            (
                "categorical",
                categorical_transformer,
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )


def train_and_evaluate(df: pd.DataFrame) -> Pipeline:
    """Train the model using a production-style preprocessing pipeline."""
    df = add_time_features(df)
    df = clean_missing_values(df)
    df = correct_data_inconsistencies(df)
    df = engineer_features(df)
    df = cap_extreme_values(
        df,
        [
            "follower_count",
            "likes",
            "comments",
            "shares",
            "saves",
            "followers_gained",
            "reach",
            "impressions",
            "engagement",
            "reach_impression_ratio",
        ],
    )

    df = df.dropna(subset=[TARGET_COLUMN])

    X = df[MODEL_FEATURES].copy()
    y = df[TARGET_COLUMN].astype(float).copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    preprocessor = build_preprocessing_pipeline()

    model_pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE),
            ),
        ]
    )

    model_pipeline.fit(X_train, y_train)

    predictions = model_pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("=" * 50)
    print("MODEL PERFORMANCE METRICS")
    print("=" * 50)
    print(f"MAE: {mae:.4f}")
    print(f"R2 Score: {r2:.4f}")
    print("=" * 50)

    feature_names = preprocessor.get_feature_names_out()
    feature_importance = model_pipeline.named_steps["regressor"].feature_importances_

    plot_feature_importance(feature_names, feature_importance)
    plot_confusion_matrix(y_test, predictions)

    print("\nClassification Report (Binned Engagement Levels):")
    print(
        classification_report(
            pd.cut(y_test, bins=3, labels=["Low", "Medium", "High"]),
            pd.cut(predictions, bins=3, labels=["Low", "Medium", "High"]),
            labels=["Low", "Medium", "High"],
        )
    )

    return model_pipeline


def plot_feature_importance(feature_names: np.ndarray, feature_importance: np.ndarray) -> None:
    """Plot the top model features for easier interpretation."""
    top_idx = np.argsort(feature_importance)[-12:]
    plt.figure(figsize=(12, 8))
    plt.barh(feature_names[top_idx], feature_importance[top_idx], edgecolor="k", alpha=0.8)
    plt.xlabel("Feature Importance")
    plt.title("Top 12 Feature Importances")
    plt.tight_layout()
    plt.savefig("plots/feature_importance.png", dpi=300, bbox_inches="tight")
    print("✓ Feature importance plot saved")


def plot_confusion_matrix(y_true: pd.Series, predictions: np.ndarray) -> None:
    """Plot a confusion matrix for binned engagement prediction."""
    y_true_bins = pd.cut(y_true, bins=3, labels=["Low", "Medium", "High"])
    predictions_bins = pd.cut(predictions, bins=3, labels=["Low", "Medium", "High"])

    cm = confusion_matrix(y_true_bins, predictions_bins, labels=["Low", "Medium", "High"])
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Low", "Medium", "High"],
        yticklabels=["Low", "Medium", "High"],
    )
    plt.xlabel("Predicted Engagement Level")
    plt.ylabel("Actual Engagement Level")
    plt.title("Confusion Matrix (Engagement Level Classification)")
    plt.tight_layout()
    plt.savefig("plots/confusion_matrix.png", dpi=300, bbox_inches="tight")
    print("✓ Confusion matrix plot saved")


if __name__ == "__main__":
    df = load_dataset(DATA_PATH)
    model_pipeline = train_and_evaluate(df)
    joblib.dump(model_pipeline, "model.pkl")
    print("Model saved to model.pkl")
