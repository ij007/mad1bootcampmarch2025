from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from application.model import User, Post, PostStats, UserStats, create_all, db

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
    
        
