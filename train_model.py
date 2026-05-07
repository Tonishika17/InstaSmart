import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

os.makedirs("plots", exist_ok=True)

data = pd.read_csv("Instagram_Analytics.csv")

if "engagement" not in data.columns:
    data["engagement"] = data[["likes", "comments", "shares", "saves"]].sum(axis=1)

data["has_call_to_action"] = data["has_call_to_action"].fillna(0).astype(int)

data["day_of_week"] = data["day_of_week"].fillna("Unknown")

data["traffic_source"] = data["traffic_source"].fillna("Home Feed")

features = [
    "follower_count",
    "post_hour",
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
    "content_category",
    "media_type",
    "traffic_source",
    "day_of_week",
    "has_call_to_action"
]

X = data[features]
y = data["engagement_rate"].fillna(0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer(
    transformers=[
        (
            'cat',
            OneHotEncoder(handle_unknown='ignore', sparse_output=False),
            ["content_category", "media_type", "traffic_source", "day_of_week"],
        )
    ],
    remainder='passthrough'
)

model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("=" * 50)
print("MODEL PERFORMANCE METRICS")
print("=" * 50)
print(f"MAE: {mae:.4f}")
print(f"R2 Score: {r2:.4f}")
print("=" * 50)

feature_importance = model.named_steps['regressor'].feature_importances_
feature_names = model.named_steps['preprocessor'].get_feature_names_out()

plt.figure(figsize=(12, 8))
indices = np.argsort(feature_importance)[-10:]
plt.barh(np.arange(len(indices)), feature_importance[indices], edgecolor='k', alpha=0.7)
plt.yticks(np.arange(len(indices)), [feature_names[i] for i in indices])
plt.xlabel('Feature Importance', fontsize=12)
plt.ylabel('Features', fontsize=12)
plt.title('Top 10 Feature Importance', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('plots/feature_importance.png', dpi=300, bbox_inches='tight')
print("✓ Feature importance plot saved")

y_test_bins = pd.cut(y_test, bins=3, labels=['Low', 'Medium', 'High'])
predictions_bins = pd.cut(predictions, bins=3, labels=['Low', 'Medium', 'High'])
cm = confusion_matrix(y_test_bins, predictions_bins, labels=['Low', 'Medium', 'High'])

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
            xticklabels=['Low', 'Medium', 'High'],
            yticklabels=['Low', 'Medium', 'High'])
plt.xlabel('Predicted Engagement Level', fontsize=12)
plt.ylabel('Actual Engagement Level', fontsize=12)
plt.title('Confusion Matrix (Engagement Level Classification)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('plots/confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✓ Confusion matrix plot saved")

print("\nClassification Report (Binned Engagement Levels):")
print(classification_report(y_test_bins, predictions_bins, labels=['Low', 'Medium', 'High']))

joblib.dump(model, "model.pkl")
print("Model saved to model.pkl")
