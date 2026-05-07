import os
import joblib
import pandas as pd
from sqlalchemy import func, inspect, text
from flask import Flask, render_template, request
from models import db, Post
import config

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


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


def initialize_database():
    db.create_all()
    inspector = inspect(db.engine)
    existing_columns = [column["name"] for column in inspector.get_columns(Post.__tablename__)]
    columns_to_add = {
        "traffic_source": "TEXT",
        "has_call_to_action": "INTEGER",
        "day_of_week": "TEXT",
        "shares": "INTEGER",
        "saves": "INTEGER",
        "followers_gained": "INTEGER",
        "engagement": "FLOAT"
    }

    with db.engine.begin() as connection:
        for name, column_type in columns_to_add.items():
            if name not in existing_columns:
                connection.execute(text(f"ALTER TABLE {Post.__tablename__} ADD COLUMN {name} {column_type}"))


with app.app_context():
    initialize_database()

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None
    
@app.route("/", methods=["GET", "POST"])
def home():
    engagement_rate = None
    engagement_count = None
    content_category = ""
    best_category = ""
    suggestion = ""
    predicted_engagement = None
    analytics_insights = []
    category_averages = {}

    if request.method == "POST":
        follower_count = int(request.form.get("followers", 0) or 0)
        likes = int(request.form.get("likes", 0) or 0)
        comments = int(request.form.get("comments", 0) or 0)
        shares = int(request.form.get("shares", 0) or 0)
        saves = int(request.form.get("saves", 0) or 0)
        followers_gained = int(request.form.get("followers_gained", 0) or 0)

        content_category = request.form.get("content_type", "Technology")
        traffic_source = request.form.get("traffic_source", "Home Feed")
        day_of_week = request.form.get("day_of_week", "Monday")
        has_call_to_action = 1 if request.form.get("has_call_to_action") == "on" else 0

        reach = int(request.form.get("reach", 0) or 0)
        impressions = int(request.form.get("impressions", 0) or 0)
        media_type = request.form.get("post_type", "reel")
        post_hour = int(request.form.get("hour", 0) or 0)
        caption_length = int(request.form.get("caption_length", 0) or 0)
        hashtags_count = int(request.form.get("hashtags", 0) or 0)

        engagement_count = likes + comments + shares + saves
        engagement_rate = round((engagement_count / follower_count) if follower_count else 0.0, 4)

        input_df = pd.DataFrame([{
            "follower_count": follower_count,
            "post_hour": post_hour,
            "caption_length": caption_length,
            "hashtags_count": hashtags_count,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "saves": saves,
            "followers_gained": followers_gained,
            "engagement": engagement_count,
            "content_category": content_category,
            "reach": reach,
            "impressions": impressions,
            "media_type": media_type,
            "traffic_source": traffic_source,
            "has_call_to_action": has_call_to_action,
            "day_of_week": day_of_week
        }])

        input_df["posting_period"] = input_df["post_hour"].apply(get_posting_period)
        input_df["day_of_week"] = input_df["day_of_week"].fillna("Unknown").astype(str)
        input_df["content_category"] = input_df["content_category"].fillna("Unknown").astype(str)
        input_df["media_type"] = input_df["media_type"].fillna("Unknown").astype(str)
        input_df["traffic_source"] = input_df["traffic_source"].fillna("Unknown").astype(str)

        if model is not None:
            predicted_engagement = float(model.predict(input_df)[0])

        if predicted_engagement is None:
            suggestion = "⚠️ Model file not found. Train the model with train_model.py before using predictions."
        elif predicted_engagement < engagement_rate:
            suggestion = "✅ Great performance! Your post outperformed predicted engagement."
        else:
            suggestion = "⚠️ Your post underperformed predicted engagement. Try refining content and audience reach."

        if hashtags_count < 5:
            analytics_insights.append("Increase hashtags to widen your reach and engagement potential.")
        if shares < 10:
            analytics_insights.append("Encourage more shares by adding a relatable or shareable hook.")
        if saves < 15:
            analytics_insights.append("More saves often indicate useful content; ask viewers to save for later.")
        if followers_gained < max(1, int(follower_count * 0.03)):
            analytics_insights.append("Improve follow-through by offering clear value or follow prompts.")
        if has_call_to_action:
            analytics_insights.append("A strong call-to-action can help convert impressions into real engagement.")
        else:
            analytics_insights.append("Add a clear call-to-action to increase comments, shares, and saves.")

        if traffic_source == "Hashtags":
            analytics_insights.append("Hashtag traffic can bring new viewers; keep refining your tags.")
        elif traffic_source == "Reels Feed":
            analytics_insights.append("Reels feed distribution is strong, so keep your content short and engaging.")
        elif traffic_source == "External":
            analytics_insights.append("External traffic indicates cross-platform interest; leverage those sources.")

        if day_of_week in ["Saturday", "Sunday"]:
            analytics_insights.append("Weekend posts can perform well if content feels fresh and shareable.")

        new_post = Post(
            follower_count=follower_count,
            likes=likes,
            comments=comments,
            shares=shares,
            saves=saves,
            followers_gained=followers_gained,
            post_hour=post_hour,
            caption_length=caption_length,
            hashtags_count=hashtags_count,
            content_category=content_category,
            traffic_source=traffic_source,
            has_call_to_action=bool(has_call_to_action),
            day_of_week=day_of_week,
            reach=reach,
            impressions=impressions,
            media_type=media_type,
            engagement=engagement_count,
            engagement_rate=engagement_rate
        )

        db.session.add(new_post)
        db.session.commit()

    posts = Post.query.order_by(Post.id.desc()).all()

    avg_results = db.session.query(Post.content_category, func.avg(Post.engagement_rate)).group_by(Post.content_category).all()
    category_averages = {cat: avg for cat, avg in avg_results if cat}

    if category_averages:
        best_category = max(category_averages, key=category_averages.get)

    return render_template(
        "index.html",
        engagement=round(engagement_rate * 100, 2) if engagement_rate is not None else None,
        engagement_count=engagement_count,
        content_type=content_category,
        posts=posts,
        category_averages=category_averages,
        best_category=best_category,
        predicted_engagement=round(predicted_engagement * 100, 2) if predicted_engagement is not None else None,
        suggestion=suggestion,
        analytics_insights=analytics_insights
    )

@app.route("/export")
def export():
    # Optimization: export dataset to CSV natively with Pandas
    df = pd.read_sql(db.session.query(Post).statement, db.session.bind)
    df.to_csv("Instagram_Analytics.csv", index=False)

    return "CSV saved successfully as Instagram_Analytics.csv"

@app.route("/about")
def about():
    return "This is an Instagram Analytics Dashboard"

if __name__ == "__main__":
    app.run(debug=True)