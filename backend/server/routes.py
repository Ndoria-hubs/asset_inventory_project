from server import app, db, bcrypt,cors
from flask import render_template,redirect, url_for,flash, request, jsonify
from server.models import Users, Department, Role, Category, Asset, RequestStatus, Request, RequestReview
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.route('/register', methods=["POST", "GET"])
def Register():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 200
    
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Email already registered, please choose a different one"}), 409
 
    new_user = Users(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 200

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = Users.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/users', methods=["GET"])
def home():
    users = Users.query.all()

    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role.name,
            'department': user.department.name
        }
        user_list.append(user_data)

    return jsonify({'users': user_list})

