from flask import Flask, render_template, request, redirect
from application.model import User, Post, PostStats, UserStats, create_all, db
from app import app
import requests
import datetime
import os
from PIL import Image

@app.route('/')
def home():
    return "hello world"

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        
        # user = User.query.filter_by(username=username).first()
        # if user and user.password == password:
        #     return redirect("/dashboard")
        # else:
        #     return render_template("login.html", error="Invalid username or password")
        response = requests.get(f"http://127.0.0.1:5001/user/{username}")
        if response.status_code == 200:
            user_data = response.json()
            if user_data["password"] == password:
                return redirect(f"/dashboard/{user_data['username']}")
            else:
                return render_template("login.html", error="password is incorrect")
        else:
            return render_template("login.html", error="username is incorrect")
  
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':
        return render_template("signup.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_data = {
            "username": username,
            "password": password
        }
        response = requests.get(f"http://127.0.0.1:5001/user/{username}")
        if response.status_code == 200:
            return render_template("signup.html", error="Username already exists")
        
        response = requests.post(f"http://127.0.0.1:5001/user", json=user_data)
        if response.status_code == 201:
            return redirect("/login")
        else:
            return render_template("signup.html", error="Failed to create user")
        
@app.route('/dashboard/<string:username>', methods=['GET', 'POST'])
def dashboard(username):
    user = requests.get(f"http://127.0.0.1:5001/user/{username}")
    if user.status_code == 200:
        user_data = user.json()
    else:
        return render_template("dashboard.html", error="User not found")
    
    if request.method == 'GET':
        return render_template("dashboard.html", user=user_data)
    
@app.route('/create_post/<string:username>', methods=['GET', 'POST'])
def create_post(username):
    user = requests.get(f"http://127.0.0.1:5001/user/{username}")
    if user.status_code == 200:
        user_data = user.json()
    else:
        return render_template("dashboard.html", error="User not found")
    
    if request.method == 'GET':
        return render_template("create_post.html", user=user_data)
    
    if request.method == 'POST':
        title = request.form["title"]
        description = request.form["description"]
        image = request.files["image"]
        if not image:
            image = None
        else:
            #saving image to static folder
            image.save(f"static/{image.filename}")
            image = f"/static/{image.filename}"
        userID = user_data["userID"]
        post_data = {
            "title": title,
            "description": description,
            "image": image,
            "userID": userID,
            "timestamp": str(datetime.datetime.now())
        }
        response = requests.post(f"http://127.0.0.1:5001/post", json=post_data)
        if response.status_code == 201:
            return redirect(f"/dashboard/{username}")
        else:
            return render_template("create_post.html", error="Failed to create post", user=user_data)
        
@app.route('/profile/<string:username>', methods=['GET'])
def profile(username):
    user = requests.get(f"http://127.0.0.1:5001/user/{username}")
    if user.status_code == 200:
        user_data = user.json()
    else:
        return render_template("dashboard.html", error="User not found")
    
    if request.method == "GET":
        return render_template("profile.html", user=user_data)
    
@app.route("/all_posts/<string:username>", methods=['GET'])
def all_posts(username):
    user = requests.get(f"http://127.0.0.1:5001/user/{username}")
    if user.status_code == 200:
        user_data = user.json()
    else:
        return render_template("dashboard.html", error="User not found")
    
    if request.method == "GET":
        all_posts = requests.get(f"http://127.0.0.1:5001/post/{user_data['userID']}")
        if all_posts.status_code == 200:
            all_posts_data = all_posts.json()
            return render_template("all_posts.html", posts=all_posts_data, user=user_data)
        else:
            return render_template("all_posts.html", error="No posts found", user=user_data)
        
        