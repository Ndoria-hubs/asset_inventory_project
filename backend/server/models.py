from server import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def user_loader(id):
    return Users.query.get(int(id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=3)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    requests = db.relationship('Request', backref='user_requests', lazy=True)
    request_reviews = db.relationship('RequestReview', backref='written_reviews', lazy=True)  # Renamed backref
    allocated_assets = db.relationship('Asset', backref='allocated_user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), unique=True, nullable=False)
    can_view_requests = db.Column(db.Boolean, default=False)
    can_approve_requests = db.Column(db.Boolean, default=False)
    can_manage_assets = db.Column(db.Boolean, default=False)
    can_view_all_requests = db.Column(db.Boolean, default=False)

    users = db.relationship('Users', backref='role', lazy=True)

    def __repr__(self):
        return f"Role('{self.role_name}')"

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), unique=True, nullable=False)

    users = db.relationship('Users', backref='department', lazy=True)
    assets = db.relationship('Asset', backref='department', lazy=True)
    requests = db.relationship('Request', backref='department', lazy=True)

    def __repr__(self):
        return f"Department('{self.department_name}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))

    assets = db.relationship('Asset', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.category_name}')"

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asset_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(40))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(20))  
    allocated_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    requests = db.relationship('Request', backref='asset', lazy=True)

    def __repr__(self):
        return f"Asset('{self.asset_name}', '{self.status}')"

class RequestStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    requests = db.relationship('Request', backref='status', lazy=True)

    def __repr__(self):
        return f"RequestStatus('{self.status_name}')"

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_type = db.Column(db.String(100)) 
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=True)
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    quantity = db.Column(db.Integer)
    urgency = db.Column(db.String(20))
    reason = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('request_status.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('RequestReview', back_populates='request', lazy=True)

    user_requested = db.relationship('Users', backref='requestss', lazy=True)

    def __repr__(self):
        return f"Request('{self.request_type}', '{self.status_id}')"


class RequestReview(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20)) 
    review_comment = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime, default=datetime.utcnow)

    request = db.relationship('Request', back_populates='reviews')
    reviewed_by_user = db.relationship('Users', backref='requesting_reviews', lazy=True)  # Renamed to prevent conflict

    def __repr__(self):
        return f"RequestReview('{self.status}', '{self.reviewed_by}')"

    def __repr__(self):
        return f"RequestReview('{self.status}', '{self.reviewed_by}')"
    
        admin_role = Role(
            role_name="Admin",
            can_view_requests=True,
            can_approve_requests=True,
            can_manage_assets=True,
            can_view_all_requests=True
        )
        procurement_manager_role = Role(
            role_name="Procurement Manager",
            can_view_requests=True,
            can_approve_requests=True,
            can_manage_assets=False,
            can_view_all_requests=False
        )
        admin_role = Role(
            role_name="Admin",
            can_view_requests=True,
            can_approve_requests=True,
            can_manage_assets=True,
            can_view_all_requests=True
        )