from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.model import User, Post, PostStats, UserStats, create_all, db


app = Flask(__name__)

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ij007/Developer/Bootcamp_march/bloglite.db'
    db.init_app(app)
    create_all(app)
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)