from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from application.model import User, Post, PostStats, UserStats, create_all, db
import datetime
class userAPI(Resource):
    #used to get user data by username
    def get(self, username):
        
        user = User.query.filter_by(username=username).first()
        if user:
            user_data = {
                "userID": user.userID,
                "username": user.username,
                "password": user.password
            }
            return user_data, 200
        else:
            return {"error": "User not found"}, 404
    
    #user to create a new user
    def post(self):
        data = request.get_json()
        try:
            user = User(username=data["username"], password=data["password"])
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
        
    def put():
        pass

    def delete():
        pass
    
class postAPI(Resource):

    def get(self, userID):
        posts = Post.query.filter_by(user_id=userID).all()
        if posts:
            post_data = []
            for post in posts:
                post_data.append({
                    "postID": post.postID,
                    "title": post.title,
                    "description": post.description,
                    "image_url": post.image_url,
                    "timestamp": str(post.timestamp)
                })
            return post_data, 200
        else:
            return {"error": "No posts found"}, 404
        
    def post(self):
        data = request.get_json()
        print(data)
        try:
            title = data["title"]
            description = data["description"]
            image = data["image"]
            userID = data["userID"]
            timestamp = data["timestamp"]
            #convert timestamp to datetime object
            timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            if not image:
                image = None
            post = Post(title=title, description=description, image_url=image, user_id=userID, timestamp=timestamp)
            db.session.add(post)
            db.session.commit()
            return {"message": "Post created successfully"}, 201
        except Exception as e:
            print(e)
            return {"error": str(e)}, 500
        
    def put(self):
        pass
    
    def delete(self):
        pass
    