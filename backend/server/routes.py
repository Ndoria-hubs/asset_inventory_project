from server import app, db, bcrypt
from flask import jsonify, request
from server.models import Users, Department, Category, Asset, RequestStatus,Request,ReviewRequests
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

#creating the first admin user
@app.route('/setup', methods=['POST'])
def setup():
    user = Users.query.filter_by(role='admin').first()
    if user:
        return jsonify(message="Admin user already exists."), 400
    elif user.query.filter_by(email=email).first():
        return jsonify(message="Email already exists.please choose a different one"), 400
    else:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        department = data.get('department')
        role = 'Admin'
    
        new_user = Users(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            department=department,
            role=role
            )
        db.session.add(new_user)
        db.session.commit()

    return jsonify(message="Admin user created successfully."), 201

@app.route('/register', methods=["POST", "GET"])
@login_required
def Register():
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    department_id = data.get("department_id")
    role = data.get("role")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Email already registered, please choose a different one"}), 409
 
    new_user = Users(
        username=username,
        email=email,
        password=bcrypt.generate_password_hash(password).decode('utf-8'),
        department_id=department_id,
        role=role,
        created_at=datetime.utcnow()
    )
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
#@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/assets')
#@login_required
def assets():
    assets = Asset.query.all()
    asset_list = []
    for asset in assets:
        asset = {
            'asset_image': asset.image_url,
            'asset_name': asset.asset_name,
            'asset_status': asset.status,
            'description': asset.description,
            'category': asset.category.category_name,
            'department': asset.department.department_name,
            'allocated_to': asset.user_allocated_assets.username if asset.allocated_to else 'Not allocated',
            'created_at': asset.created_at.strftime('%d/%m/%Y %H:%M')
        }
        asset_list.append(asset)
    return jsonify({'assets': asset_list})

@app.route('/asset/<int:id>')
#@login_required
def asset(id):
    asset = Asset.query.get(id)
    asset_data = {
        'asset_image': asset.image_url,
        'asset_name': asset.asset_name,
        'asset_status': asset.status,
        'description': asset.description,
        'category': asset.category.category_name,
        'department': asset.department.department_name,
        'allocated_to': asset.user_allocated_assets.username if asset.allocated_to else 'Not allocated',
        'created_at': asset.created_at.strftime('%d/%m/%Y %H:%M')
    }
    return jsonify({'asset': asset_data})


@app.route('/add_asset', methods=['POST'])
#@login_required
def add_asset():
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    data = request.get_json()
    new_asset = Asset(asset_name=data.get("asset_name"), description=data.get("description"),
                    category_id=data.get('category_id'),image_url= data.get("image_url"), status=data.get("status"),
                    department_id=data.get("department_id"),allocated_to=data.get("allocated_to"),
                    created_at=datetime.utcnow())
    db.session.add(new_asset)
    db.session.commit()
    return jsonify({'message': 'Asset added successfully'})

@app.route('/asset/<int:id>/edit', methods=['POST'])
#@login_required
def edit_asset(id):
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    asset = Asset.query.get(id)
    data = request.get_json()
    asset.asset_name = data.get("asset_name", asset.asset_name)
    asset.description = data.get("description", asset.description)
    asset.category_id = data.get("category_id", asset.category_id)
    asset.image_url = data.get("image_url", asset.image_url)
    asset.status = data.get("status", asset.status)
    asset.department_id = data.get("department_id", asset.department_id)
    asset.allocated_to = data.get("allocated_to", asset.allocated_to)
    db.session.commit()
    return jsonify({'message': 'Asset updated successfully'})

@app.route('/asset/<int:id>/delete', methods=['POST'])
#@login_required
def delete_asset(id):
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    asset = Asset.query.get(id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Asset deleted successfully'})

@app.route('/requests')
@login_required
def requests():
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    requests = Request.query.all()
    request_data = []
    for req in requests:
        req = {
            'request_type': req.request_type,
            'asset_name': req.related_asset.asset_name,
            'asset_image': req.related_asset.image_url,
            'requested_by': req.user_requesting.username,
            'department': req.department_requesting.department_name,
            'quantity': req.quantity,
            'urgency': req.urgency,
            'reason': req.reason,
            'status': req.request_status.status_name,
            'created_at': req.created_at.strftime('%d/%m/%Y %H:%M')
        }
        request_data.append(req)
    return jsonify({'requests': request_data})

@app.route('/request/<int:id>')
#@login_required
def get_request(id):
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    get_request = Request.query.get_or_404(id)
    request_data = {
        'request_type': get_request.request_type,
        'asset_name': get_request.related_asset.asset_name,
        'asset_image': get_request.related_asset.image_url,
        'requested_by': get_request.user_requesting.username,
        'department': get_request.department_requesting.department_name,
        'quantity': get_request.quantity,
        'urgency': get_request.urgency,
        'reason': get_request.reason,
        'status': get_request.request_status.status_name,
        'created_at': get_request.created_at.strftime('%d/%m/%Y %H:%M')
    }
    return jsonify({'get_request': request_data})

@app.route('/new_request', methods=['POST'])
#@login_required 
def add_request():
    if request.method == 'POST':
        data = request.get_json()

        request_type = data.get("request_type")
        asset_id = data.get("asset_id")
        department_id = data.get("department_id")
        quantity = data.get("quantity")
        urgency = data.get("urgency")
        reason = data.get("reason")

        user_department_ids = [dept.id for dept in current_user.departments]
        if department_id not in user_department_ids:
            return jsonify({'error': 'User is not part of the specified department'}), 403

        new_request = Request(
            request_type=request_type,
            asset_id=asset_id,
            requested_by=current_user.id,
            department_id=department_id,
            quantity=quantity,
            urgency=urgency,
            reason=reason,
            status_id=1,  
            created_at=datetime.utcnow()
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Request added successfully'}), 201

@app.route('/request/<int:id>/review', methods=['POST'])
#@login_required
def review_request(id):
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    data = request.get_json()
    get_request = Request.query.get_or_404(id)
    if data.get("status") == 2:
        new_review = ReviewRequests(request_id=id, reviewed_by=current_user.id, status=data.get("status"),
                                review_comment=data.get("review_comment"), reviewed_at=datetime.utcnow())
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Request approved successfully'})
    else:
        new_review = ReviewRequests(request_id=id, reviewed_by=current_user.id, status=data.get("status"),
                                review_comment=data.get("review_comment"), reviewed_at=datetime.utcnow())
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Request rejected, reason: {}'.format(data.get("review_comment"))})
    

@app.route('/requests/pending', methods=['GET'])
#@login_required
def pending_requests():
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    requests = Request.query.filter_by(status_id=1).all()
    request_data = []
    for req in requests:
        req = {
            'request_type': req.request_type,
            'asset_name': req.related_asset.asset_name,
            'asset_image': req.related_asset.image_url,
            'requested_by': req.user_requesting.username,
            'department': req.department_requesting.department_name,
            'quantity': req.quantity,
            'urgency': req.urgency,
            'reason': req.reason,
            'status': req.request_status.status_name,
            'created_at': req.created_at.strftime('%d/%m/%Y %H:%M')
        }
        request_data.append(req)
    return jsonify({'requests': request_data})

@app.route('/departments', methods=['GET'])
#@login_required
def departments():
    departments = Department.query.all()
    department_data = {}
    for department in departments:
        department_data[department.department_name] = {
            'assets': [asset.asset_name for asset in department.assets],
             'requests': [
                {
                   "request_type": request.request_type,
                    "asset_name": request.related_asset.asset_name,
                    "asset_image": request.related_asset.image_url,
                    "requested_by":request.user_requesting.username,
                    "quantity": request.quantity,
                    "urgency": request.urgency,
                    "reason": request.reason,
                    "status": request.request_status.status_name,
                    "created_at": request.created_at.strftime('%d/%m/%Y %H:%M')
                }
                for request in department.requests
            ],
            'members': [user.username for user in department.users]
        }
    return jsonify({'departments': department_data})

@app.route('/department/<int:id>')
#@login_required
def department(id):
    department = Department.query.get_or_404(id)
    department_data = {
        "department_name":department.department_name,
        'assets': [asset.asset_name for asset in department.assets],
        'requests': [
            {
                "request_type": request.request_type,
                "asset_name": request.related_asset.asset_name,
                "asset_image": request.related_asset.image_url,
                "requested_by":request.user_requesting.username,
                "quantity": request.quantity,
                "urgency": request.urgency,
                "reason": request.reason,
                "status": request.request_status.status_name,
                "created_at": request.created_at.strftime('%d/%m/%Y %H:%M')
            }
            for request in department.requests
        ],
        'members': [user.username for user in department.users]
    }
    return jsonify({'department': department_data})

@app.route('/categories', methods=['GET'])
#@login_required
def categories():
    categories = Category.query.all()
    category_data = {}
    for category in categories:
        category_data[category.category_name] = {
            'assets': [asset.asset_name for asset in category.assets]
        }
    return jsonify({'categories': category_data})

@app.route('/my_profile', methods=['GET'])
#@login_required
def my_profile():
    user = current_user
    user_data = {
        'username': user.username,
        'email': user.email,
        'department': user.department.department_name,
        'allocated assets': [asset.asset_name for asset in user.allocated_assets],
        'role': user.role,
        'created_at': user.created_at.strftime('%d/%m/%Y %H:%M')
    }
    return jsonify({'user': user_data})


@app.route('/users', methods=["GET"])
def home():
    users = Users.query.all()
    user_list = []
    for user in users:
        user = {
            'username': user.username,
            'email': user.email,
            'department': user.department.department_name,
            'role': user.role,
            'created_at': user.created_at
        }
        user_list.append(user)
    return jsonify({'users': user_list})       

@app.route('/user/<int:id>', methods=['GET', 'POST'])
#@login_required
def user(id):
    user = Users.query.get_or_404(id)
    user_data = {
        'username': user.username,
        'email': user.email,
        'department': user.department.department_name,
        'allocated assets': [asset.asset_name for asset in user.allocated_assets],
        'role': user.role,
        'created_at': user.created_at
        }
    return jsonify({'user': user_data})
 
@app.route('/user/<int:id>/edit', methods=['POST'])
#@login_required
def edit_user(id):
    if current_user.role != 'Admin':
        return jsonify({'message': 'Unauthorized to access this page'}), 403
    user = Users.query.get(id)
    data = request.get_json()
    user.username = user.username
    user.email = user.email
    user.role = data.get("role", user.role)
    user.department_id = data.get("department_id", user.department_id)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})