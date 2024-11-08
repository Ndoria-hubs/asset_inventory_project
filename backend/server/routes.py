from server import app, db, bcrypt,cors
from flask import render_template,redirect, url_for,flash, request, jsonify
from server.models import Users, Department, Role, Category, Asset, RequestStatus, Request, RequestReview
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

@app.route('/')
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

