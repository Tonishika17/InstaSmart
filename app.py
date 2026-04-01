import csv,os
import joblib
from flask import Flask, render_template, request, Response
from models import db,Post
model = joblib.load("model.pkl")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route("/", methods=["GET","POST"])
def home():
    engagement_rate = None
    content_type = ""
    best_category = ""
    suggestion = ""
    predicted_engagement = 0
    fashion_avg = 0
    beauty_avg = 0
    acting_avg = 0

    if request.method == "POST":
        followers = int(request.form["followers"])
        likes = int(request.form["likes"])
        comments = int(request.form["comments"])
        content_type = request.form["content_type"]
        reach = int(request.form["reach"])
        impressions = int(request.form["impressions"])
        post_type = request.form["post_type"]
        post_type_map = {
            "reel": 0,
            "photo": 1,
            "video": 2
            }

        post_type_encoded = post_type_map[post_type]
        category_map = {
            "fashion": 0,
            "beauty": 1,
            "acting": 2
        }

        category = category_map[content_type]

        hour = int(request.form["hour"])
        caption_length = int(request.form["caption_length"])
        hashtags = int(request.form["hashtags"])

        engagement_rate = (likes + comments) / followers * 100
        #ML prediction
        input_data = [[
            followers,
            hour,
            caption_length,
            hashtags,
            category,
            reach,
            impressions,
            post_type_encoded
            ]]
        
        predicted_engagement = model.predict(input_data)[0]
        suggestion = ""
        if predicted_engagement < engagement_rate:
            suggestion = "⚠️ Your post underperformed. Try improving strategy."
        elif predicted_engagement > engagement_rate:
            suggestion = "✅ Good performance! Similar posts may work well."
        # smarter rules
        if hashtags < 5:
            suggestion += " Use more hashtags."
        if hour < 12:
            suggestion += " Try posting in evening hours."
        if category == 2:
            suggestion += " Acting content is performing well."
        #save in db
        new_post = Post(
            followers=followers,
            likes=likes,
            comments=comments,
            hour=hour,
            caption_length=caption_length,
            hashtags=hashtags,
            category=category,
            reach=reach,
            impressions=impressions,
            post_type=post_type_encoded,
            engagement=engagement_rate
        )

        db.session.add(new_post)
        db.session.commit()

    # ✅ FETCH POSTS FIRST
    posts = Post.query.all()

    # Initialize counters
    fashion_engagement = 0
    fashion_count = 0
    acting_engagement = 0
    acting_count = 0
    beauty_engagement = 0
    beauty_count = 0

    # ✅ LOOP CORRECTLY
    for post in posts:
        if post.category == 0:
            fashion_engagement += post.engagement
            fashion_count += 1
        elif post.category == 2:
            acting_engagement += post.engagement
            acting_count += 1
        else:
            beauty_engagement += post.engagement
            beauty_count += 1

    # ✅ CALCULATE AVERAGES OUTSIDE LOOP
    if fashion_count > 0:
        fashion_avg = fashion_engagement / fashion_count

    if acting_count > 0:
        acting_avg = acting_engagement / acting_count

    if beauty_count > 0:
        beauty_avg = beauty_engagement / beauty_count

    # ✅ BEST CATEGORY
    if fashion_avg > acting_avg and fashion_avg > beauty_avg:
        best_category = "fashion"
    elif acting_avg > beauty_avg:
        best_category = "acting"
    else:
        best_category = "beauty"

    return render_template(
        "index.html",
        engagement=engagement_rate,
        content_type=content_type,
        posts=posts,
        fashion_avg=fashion_avg,
        beauty_avg=beauty_avg,
        acting_avg=acting_avg,
        best_category=best_category,
        predicted_engagement=round(predicted_engagement, 2),
        suggestion=suggestion
        )

@app.route("/export")
def export():
    posts = Post.query.all()

    file_path = "dataset.csv"

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        # header
        writer.writerow([
            "followers",
            "hour",
            "caption_length",
            "hashtags",
            "category",
            "reach",
            "impressions",
            "post_type",
            "engagement"
            ])

        # data
        for post in posts:
            writer.writerow([
                post.followers,
                post.likes,
                post.comments,
                post.hour,
                post.caption_length,
                post.hashtags,
                post.category,
                post.reach,
                post.impressions,
                post.post_type,
                post.engagement
            ])

    return "CSV saved successfully as dataset.csv"
@app.route("/about")
def about():
    return "This is an Instagram Analysis Dashboard"
if __name__ == "__main__":
    app.run(debug=True)