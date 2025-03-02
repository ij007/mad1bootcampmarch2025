from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Post(db.Model):
    __tablename__ = 'post'
    postID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

class PostStats(db.Model):
    __tablename__ = 'post_stats'
    postStatsID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    postID = db.Column(db.Integer, db.ForeignKey('post.postID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    like = db.Column(db.Boolean)
    comment = db.Column(db.String(255))


class UserStats(db.Model):
    __tablename__ = 'user_stats'
    userStatsID = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    followingID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

def create_all(app):
    print("Starting the DB creation...")
    with app.app_context():
        db.create_all()
        print("DB creation completed.")