from flask import Flask, render_template, request, redirect
from application.model import User, Post, PostStats, UserStats, create_all, db
from app import app
import requests

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
                return redirect("/dashboard")
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