from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
    return "Your Instagram Reach"

@app.route("/about")
def about():
    return "This is an Instagram Analysis Dashboard"
if __name__ == "__main__":
    app.run(debug=True)