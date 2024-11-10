from datetime import datetime
from server import app, db
from server.models import Users, Department, Category, Asset, RequestStatus, Request, ReviewRequests
from werkzeug.security import generate_password_hash

with app.app_context():
    # Delete existing data
    print("Deleting data...")
    ReviewRequests.query.delete()
    Request.query.delete()
    RequestStatus.query.delete()
    Asset.query.delete()
    Category.query.delete()
    Department.query.delete()
    Users.query.delete()

    # Create Departments
    print("Creating departments...")
    hr_department = Department(department_name="Human Resources")
    it_department = Department(department_name="IT Department")
    finance_department = Department(department_name="Finance Department")
    marketing_department = Department(department_name="Marketing Department")
    operations_department = Department(department_name="Operations Department")
    legal_department = Department(department_name="Legal Department")
    
    departments = [hr_department, it_department, finance_department, marketing_department, operations_department, legal_department]
    db.session.add_all(departments)
    db.session.commit()

    # Create Categories
    print("Creating categories...")
    electronics_category = Category(category_name="Electronics", description="Electronic assets like laptops and phones.")
    furniture_category = Category(category_name="Furniture", description="Furniture assets like desks and chairs.")
    vehicles_category = Category(category_name="Vehicles", description="Company vehicles.")
    tools_category = Category(category_name="Tools", description="Operational tools for various departments.")
    
    categories = [electronics_category, furniture_category, vehicles_category, tools_category]
    db.session.add_all(categories)
    db.session.commit()

    # Create Users
    print("Creating users...")
    users = []
    for i in range(1, 11):
        username = f"user{i}"
        email = f"user{i}@example.com"
        password = generate_password_hash("password")
        department = departments[i % len(departments)]
        users.append(Users(username=username, email=email, password=password, department=department, role="User"))
    
    db.session.add_all(users)
    db.session.commit()

    # Create Assets
    print("Creating assets...")
    assets = []
    for i in range(1, 11):
        asset_name = f"Asset {i}"
        description = f"Description of Asset {i}"
        category = categories[i % len(categories)]
        department = departments[i % len(departments)]
        allocated_to = i if i % 2 == 0 else None  # Allocate some assets to users
        assets.append(Asset(asset_name=asset_name, description=description, category=category, department=department, allocated_to=allocated_to))

    db.session.add_all(assets)
    db.session.commit()

    # Create Request Statuses
    print("Creating request statuses...")
    status_pending = RequestStatus(status_name="Pending", description="Request is pending approval.")
    status_approved = RequestStatus(status_name="Approved", description="Request has been approved.")
    status_rejected = RequestStatus(status_name="Rejected", description="Request has been rejected.")
    statuses = [status_pending, status_approved, status_rejected]
    db.session.add_all(statuses)
    db.session.commit()

    # Create Requests
    print("Creating requests...")
    requests = []
    for i in range(1, 11):
        request_type = f"Request {i}"
        asset = assets[i % len(assets)]
        requested_by = users[i % len(users)]
        department = departments[i % len(departments)]
        quantity = i
        urgency = "High" if i % 2 == 0 else "Low"
        reason = f"Reason for request {i}"
        status = statuses[i % len(statuses)]
        requests.append(Request(request_type=request_type, asset=asset, requested_by=requested_by, department=department, quantity=quantity, urgency=urgency, reason=reason, status=status))

    db.session.add_all(requests)
    db.session.commit()

    # Create Request Reviews
    print("Creating request reviews...")
    reviews = []
    for i in range(1, 6):
        request = requests[i - 1]  # Use the first 5 requests for reviews
        reviewed_by = users[(i + 1) % len(users)]  # Get a different user for each review
        status = statuses[(i + 1) % len(statuses)]  # Alternate between statuses
        review_comment = f"Review comment for request {i}"
        reviews.append(ReviewRequests(request=request, reviewed_by=reviewed_by, status=status, review_comment=review_comment))

    db.session.add_all(reviews)
    db.session.commit()

    print("Seeding done!")