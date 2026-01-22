from flask import Flask, render_template, request
app = Flask(__name__)
posts = []
@app.route("/", methods=["GET","POST"])

def home():
    engagement_rate = None
    content_type = ""
    best_category = ""

    fashion_avg = 0
    beauty_avg = 0
    acting_avg = 0
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
        
    fashion_engagement = 0
    fashion_count = 0
    acting_engagement = 0
    acting_count = 0
    beauty_engagement = 0
    beauty_count = 0

    for post in posts:
        if (post["content_type"]=="fashion"):
            fashion_engagement = fashion_engagement + post["engagement"]
            fashion_count = fashion_count+1
        elif (post["content_type"]=="acting"):
            acting_count = acting_count + 1
            acting_engagement = acting_engagement + post["engagement"]
        else:
            beauty_count = beauty_count+1
            beauty_engagement = beauty_engagement + post["engagement"]
        
        if (fashion_count > 0):
            fashion_avg = fashion_engagement/fashion_count
        else :
            fashion_avg = 0

        if (acting_count > 0):
            acting_avg = acting_engagement/acting_count
        else:
            acting_avg = 0

        if (beauty_count > 0):
            beauty_avg = beauty_engagement/beauty_count
        else:
            beauty_avg = 0

        if(fashion_avg>acting_avg):
            if(fashion_avg>beauty_avg):
                best_category = "fashion"
            else:
                best_category = "beauty"
        elif(acting_avg>beauty_avg):
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
            best_category=best_category)

    return render_template("index.html")

@app.route("/about")
def about():
    return "This is an Instagram Analysis Dashboard"
if __name__ == "__main__":
    app.run(debug=True)