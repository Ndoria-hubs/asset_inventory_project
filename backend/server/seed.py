from app import app
from models import db, Users, Department, Role, Category, Asset, RequestStatus, Request, RequestReview, ActivityLog
from datetime import datetime

with app.app_context():
    # Delete existing data
    print("Deleting data...")
    ActivityLog.query.delete()
    RequestReview.query.delete()
    Request.query.delete()
    RequestStatus.query.delete()
    Asset.query.delete()
    Category.query.delete()
    Department.query.delete()
    Users.query.delete()
    Role.query.delete()

    # Create Roles
    print("Creating roles...")
    admin_role = Role(role_name="Admin", can_view_requests=True, can_approve_requests=True, can_manage_assets=True, can_view_all_requests=True)
    procurement_manager_role = Role(role_name="Procurement Manager", can_view_requests=True, can_approve_requests=True, can_manage_assets=False, can_view_all_requests=False)
    normal_member_role = Role(role_name="Normal Member", can_view_requests=True, can_approve_requests=False, can_manage_assets=False, can_view_all_requests=False)
    roles = [admin_role, procurement_manager_role, normal_member_role]
    db.session.add_all(roles)

    # Create Departments
    print("Creating departments...")
    hr_department = Department(department_name="Human Resources")
    it_department = Department(department_name="IT Department")
    finance_department = Department(department_name="Finance Department")
    departments = [hr_department, it_department, finance_department]
    db.session.add_all(departments)

    # Create Categories
    print("Creating categories...")
    electronics_category = Category(category_name="Electronics", description="Electronic assets like laptops and phones.")
    furniture_category = Category(category_name="Furniture", description="Furniture assets like desks and chairs.")
    vehicles_category = Category(category_name="Vehicles", description="Company vehicles.")
    categories = [electronics_category, furniture_category, vehicles_category]
    db.session.add_all(categories)

    # Create Users
    print("Creating users...")
    user1 = Users(username="john_doe", email="john@example.com", password="password", role=admin_role, department=it_department)
    user2 = Users(username="jane_smith", email="jane@example.com", password="password", role=procurement_manager_role, department=finance_department)
    user3 = Users(username="alice_jones", email="alice@example.com", password="password", role=normal_member_role, department=hr_department)
    users = [user1, user2, user3]
    db.session.add_all(users)
    db.session.commit()  # Commit to ensure users have IDs before proceeding

    # Create Assets
    print("Creating assets...")
    asset1 = Asset(asset_name="Laptop", description="MacBook Pro", category=electronics_category, department=it_department, allocated_to=user1.id)
    asset2 = Asset(asset_name="Office Chair", description="Ergonomic chair", category=furniture_category, department=hr_department, allocated_to=user3.id)
    asset3 = Asset(asset_name="Company Car", description="Toyota Corolla", category=vehicles_category, department=finance_department)
    assets = [asset1, asset2, asset3]
    db.session.add_all(assets)

    # Create Request Statuses
    print("Creating request statuses...")
    status_pending = RequestStatus(status_name="Pending", description="Request is pending approval.")
    status_approved = RequestStatus(status_name="Approved", description="Request has been approved.")
    status_rejected = RequestStatus(status_name="Rejected", description="Request has been rejected.")
    statuses = [status_pending, status_approved, status_rejected]
    db.session.add_all(statuses)

    # Create Requests
    print("Creating requests...")
    request1 = Request(request_type="New Laptop", asset=asset1, requested_by=user1.id, department=it_department.id, quantity=1, urgency="High", reason="Replacement needed", status=status_pending)
    request2 = Request(request_type="Office Chair", asset=asset2, requested_by=user3.id, department=hr_department.id, quantity=1, urgency="Low", reason="Additional chair", status=status_approved)
    requests = [request1, request2]
    db.session.add_all(requests)
    db.session.commit()  # Commit to ensure requests have IDs before proceeding

    # Create Request Reviews
    print("Creating request reviews...")
    review1 = RequestReview(request=request1, reviewed_by=user2.id, status="Approved", review_comment="Approved for urgent need")
    review2 = RequestReview(request=request2, reviewed_by=user1.id, status="Rejected", review_comment="Insufficient budget")
    reviews = [review1, review2]
    db.session.add_all(reviews)

    # Create Activity Logs
    print("Creating activity logs...")
    log1 = ActivityLog(user_id=user1.id, action="Created a request for a new laptop", request_id=request1.id, timestamp=datetime.now())
    log2 = ActivityLog(user_id=user2.id, action="Reviewed a request for a new chair", request_id=request2.id, timestamp=datetime.now())
    activity_logs = [log1, log2]
    db.session.add_all(activity_logs)

    # Commit all changes
    db.session.commit()
    print("Seeding done!")
