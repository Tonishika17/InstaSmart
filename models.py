from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy()
db.init_app(app)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    followers = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    caption_length = db.Column(db.Integer)
    hashtags = db.Column(db.Integer)
    category = db.Column(db.Integer)
    engagement = db.Column(db.Float)
    reach = db.Column(db.Integer)
    impressions = db.Column(db.Integer)
    post_type = db.Column(db.Integer)