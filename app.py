from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from application.api import userAPI, postAPI
from application.model import User, Post, PostStats, UserStats, create_all, db


app = Flask(__name__)

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ij007/Developer/Bootcamp_march/mad1bootcampmarch2025/bloglite.db'
    db.init_app(app)
    # create_all(app)
    return app

app = create_app()
api = Api(app)

api.add_resource(userAPI, '/user/<string:username>', '/user')
api.add_resource(postAPI, '/post/<int:userID>', '/post', '/post/update/<int:postID>', '/post/delete_post/<int:postID>')

if __name__ == '__main__':
    from application.controllers import *
    app.run(debug=True, port=5001)