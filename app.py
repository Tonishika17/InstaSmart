from flask import Flask, render_template, request
app = Flask(__name__)
posts = []
@app.route("/", methods=["GET","POST"])
def home():
    if request.method=="POST":
        followers = int(request.form["followers"])
        likes = int(request.form["likes"])
        comments = int(request.form["comments"])
        content_type = request.form["content_type"]

        engagement_rate = (likes+comments)/followers*100

        values = {
            "followers": followers,
            "likes": likes,
            "comments": comments,
            "engagement": engagement_rate,
            "content_type": content_type
        }
        posts.append(values)
        print(posts)
        return render_template(
            "index.html",
            engagement=engagement_rate,
            content_type=content_type,
            posts=posts)

    return render_template("index.html")

@app.route("/about")
def about():
    return "This is an Instagram Analysis Dashboard"
if __name__ == "__main__":
    app.run(debug=True)