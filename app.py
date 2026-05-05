import csv, os
import joblib
import pandas as pd
from sqlalchemy import func
from flask import Flask, render_template, request, Response
from models import db, Post

model = joblib.load("model.pkl")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route("/", methods=["GET", "POST"])
def home():
    engagement_rate = None
    content_category = ""
    best_category = ""
    suggestion = ""
    predicted_engagement = 0
    category_averages = {}

    if request.method == "POST":
        follower_count = int(request.form["followers"])
        likes = int(request.form["likes"])
        comments = int(request.form["comments"])
        content_category = request.form["content_type"]
        reach = int(request.form["reach"])
        impressions = int(request.form["impressions"])
        media_type = request.form["post_type"]
        post_hour = int(request.form["hour"])
        caption_length = int(request.form["caption_length"])
        hashtags_count = int(request.form["hashtags"])

        engagement_rate = (likes + comments) / follower_count
        
        # ML prediction using pipeline
        input_df = pd.DataFrame([{
            "follower_count": follower_count,
            "post_hour": post_hour,
            "caption_length": caption_length,
            "hashtags_count": hashtags_count,
            "content_category": content_category,
            "reach": reach,
            "impressions": impressions,
            "media_type": media_type
        }])
        
        predicted_engagement = model.predict(input_df)[0]
        suggestion = ""
        if predicted_engagement < engagement_rate:
            suggestion = "✅ Great performance! Your post exceeded expectations."
        elif predicted_engagement > engagement_rate:
            suggestion = "⚠️ Your post underperformed predicted engagement. Try improving strategy."

        # Smarter rules
        if hashtags_count < 5:
            suggestion += " Use more hashtags to increase reach."
        if post_hour < 12:
            suggestion += " Try posting in evening hours for better visibility."
            
        # Save in db
        new_post = Post(
            follower_count=follower_count,
            likes=likes,
            comments=comments,
            post_hour=post_hour,
            caption_length=caption_length,
            hashtags_count=hashtags_count,
            content_category=content_category,
            reach=reach,
            impressions=impressions,
            media_type=media_type,
            engagement_rate=engagement_rate
        )

        db.session.add(new_post)
        db.session.commit()

    posts = Post.query.all()

    # Optimization: Calculate averages using efficient SQLAlchemy query directly
    avg_results = db.session.query(Post.content_category, func.avg(Post.engagement_rate)).group_by(Post.content_category).all()
    
    # Store in dictionary map
    category_averages = {cat: avg for cat, avg in avg_results if cat}

    # Best Category
    if category_averages:
        best_category = max(category_averages, key=category_averages.get)

    return render_template(
        "index.html",
        engagement=round(engagement_rate * 100, 2) if engagement_rate else None,
        content_type=content_category,
        posts=posts,
        category_averages=category_averages,
        best_category=best_category,
        predicted_engagement=round(predicted_engagement * 100, 2) if predicted_engagement else None,
        suggestion=suggestion
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