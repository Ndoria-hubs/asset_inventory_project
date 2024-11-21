-- Roles table with specific permissions for different user types
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR UNIQUE NOT NULL,
    can_view_requests BOOLEAN DEFAULT false,
    can_approve_requests BOOLEAN DEFAULT false,
    can_manage_assets BOOLEAN DEFAULT false,
    can_view_all_requests BOOLEAN DEFAULT false,
    can_allocate_assets BOOLEAN DEFAULT false,
    can_add_categories BOOLEAN DEFAULT false,
    description TEXT
);

-- Departments table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    department_name VARCHAR UNIQUE NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT true
);

-- Users table with enhanced role management
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    department_id INTEGER REFERENCES departments(id),
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Asset categories with better organization
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR UNIQUE NOT NULL,
    description TEXT,
    parent_category_id INTEGER REFERENCES categories(id),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced assets table with more tracking fields
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    asset_name VARCHAR NOT NULL,
    asset_code VARCHAR UNIQUE,
    category_id INTEGER REFERENCES categories(id),
    image_url VARCHAR,
    status VARCHAR NOT NULL CHECK (status IN ('Available', 'Allocated', 'Under Repair', 'Retired')),
    condition VARCHAR CHECK (condition IN ('New', 'Good', 'Fair', 'Poor')),
    allocated_to INTEGER REFERENCES users(id),
    department_id INTEGER REFERENCES departments(id),
    purchase_date DATE,
    purchase_cost DECIMAL(10,2),
    warranty_expiry DATE,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Request statuses with clearer states
CREATE TABLE request_statuses (
    id SERIAL PRIMARY KEY,
    status_name VARCHAR UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true
);

-- Enhanced requests table with urgency levels
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    request_type VARCHAR NOT NULL CHECK (request_type IN ('New Asset', 'Repair')),
    asset_id INTEGER REFERENCES assets(id),
    requested_by INTEGER REFERENCES users(id),
    department_id INTEGER REFERENCES departments(id),
    quantity INTEGER CHECK (quantity > 0),
    urgency VARCHAR NOT NULL CHECK (urgency IN ('High', 'Medium', 'Low')),
    reason TEXT NOT NULL,
    status_id INTEGER REFERENCES request_statuses(id),
    expected_date DATE,
    total_cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Request reviews with procurement manager approval tracking
CREATE TABLE request_reviews (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES requests(id),
    reviewed_by INTEGER REFERENCES users(id),
    status VARCHAR NOT NULL CHECK (status IN ('Approved', 'Rejected', 'Pending More Info')),
    review_comment TEXT,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approval_level INTEGER DEFAULT 1,
    budget_available BOOLEAN,
    estimated_cost DECIMAL(10,2)
);

-- Detailed activity logging
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR NOT NULL,
    asset_id INTEGER REFERENCES assets(id),
    request_id INTEGER REFERENCES requests(id),
    details JSONB,
    ip_address VARCHAR,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Asset maintenance records
CREATE TABLE maintenance_records (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(id),
    maintenance_date DATE,
    maintenance_type VARCHAR,
    cost DECIMAL(10,2),
    performed_by VARCHAR,
    notes TEXT,
    next_maintenance_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

