from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_count = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    shares = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    followers_gained = db.Column(db.Integer)
    post_hour = db.Column(db.Integer)
    caption_length = db.Column(db.Integer)
    hashtags_count = db.Column(db.Integer)
    content_category = db.Column(db.String)
    traffic_source = db.Column(db.String)
    has_call_to_action = db.Column(db.Boolean)
    day_of_week = db.Column(db.String)
    reach = db.Column(db.Integer)
    impressions = db.Column(db.Integer)
    media_type = db.Column(db.String)
    engagement = db.Column(db.Float)
    engagement_rate = db.Column(db.Float)