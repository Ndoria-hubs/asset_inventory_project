# Asset Inventory Management System

## Overview

The **Asset Inventory Management System** is a web application designed to help organizations efficiently track, manage, and allocate assets across various departments. It centralizes asset-related data and provides a role-based access system, where users can request assets or repairs, while managers can approve requests, allocate assets, and manage the asset inventory.

---

## Problem Statement

Managing assets in large organizations can be difficult, especially when using spreadsheets or other manual systems. It becomes even more challenging to track repairs, updates, and resource allocation across different departments. This system aims to centralize asset management, provide role-based access control, and ensure that asset requests are processed in an efficient manner.

---

## Key Features

### User Authentication
- Users must authenticate to access the system.
- Users are classified into roles: **Admin**, **Procurement Manager**, and **Normal Employee**.

### Role-Based Access Control
- **Admin**: Can manage assets, users, requests, and more.
- **Procurement Manager**: Can approve/reject asset requests and allocate assets.
- **Normal Employee**: Can request new assets or repairs and view the status of their requests.

### Asset Management
- **Managers** (Admin, Procurement Manager) can add, update, and allocate assets.
- **Employees** can request assets and repairs.
  
### Request Management
- **Employees** can submit requests for assets or repairs.
- **Procurement Managers** can review, approve, or reject these requests.
- **Managers** can view pending, completed, and rejected requests.

---

## Minimum Viable Product (MVP)

- **Authentication & Authorization**: Login system with role-based access (Admin, Procurement Manager, Employee).
- **Request System**: Employees can request new assets or repairs; Managers can approve or reject these requests.
- **Asset Management**: Managers can manage the asset catalog, including adding new assets and assigning them to employees.
- **Role-Specific Views**: Separate views for Admins, Procurement Managers, and Employees.

---

## Technologies Used

- **Backend**: 
  - Flask (Python-based framework)
  - PostgreSQL (Relational database for storing assets, requests, and user data)
  
- **Frontend**: 
  - ReactJS (For building the user interface)
  - Redux Toolkit (State management for the frontend)

- **Testing**:
  - Jest (Frontend testing)
  - Minitests (Backend testing)

- **Design**:
  - Figma (Wireframing tool for designing mobile-friendly layouts)

---

## Database Schema

Here is an outline of the main database tables for asset and request management:

### 1. **Users Table**
Stores user details and roles.

| Column Name      | Data Type       | Description                          |
|------------------|-----------------|--------------------------------------|
| `id`             | `INTEGER`       | Primary Key, Auto-incrementing ID    |
| `username`       | `VARCHAR(255)`   | Unique username                      |
| `email`          | `VARCHAR(255)`   | User's email address                 |
| `password_hash`  | `VARCHAR(255)`   | Hashed password                      |
| `role`           | `VARCHAR(50)`    | Role of the user (e.g., `admin`, `procurement`, `employee`) |

### 2. **Assets Table**
Stores details about each asset.

| Column Name      | Data Type       | Description                          |
|------------------|-----------------|--------------------------------------|
| `id`             | `INTEGER`       | Primary Key, Auto-incrementing ID    |
| `name`           | `VARCHAR(255)`   | Name of the asset                    |
| `description`    | `TEXT`           | Description of the asset             |
| `category`       | `VARCHAR(255)`   | Category of the asset                |
| `quantity`       | `INTEGER`       | Number of available units            |
| `image_url`      | `VARCHAR(255)`   | URL to an image of the asset         |

### 3. **Requests Table**
Stores asset request information.

| Column Name      | Data Type       | Description                          |
|------------------|-----------------|--------------------------------------|
| `id`             | `INTEGER`       | Primary Key, Auto-incrementing ID    |
| `user_id`        | `INTEGER`       | Foreign Key referencing the `Users` table |
| `asset_id`       | `INTEGER`       | Foreign Key referencing the `Assets` table |
| `quantity`       | `INTEGER`       | Quantity requested                   |
| `urgency`        | `VARCHAR(50)`    | Urgency level (`high`, `medium`, `low`) |
| `status`         | `VARCHAR(50)`    | Request status (`pending`, `approved`, `rejected`) |
| `created_at`     | `TIMESTAMP`      | Timestamp of request creation        |
| `updated_at`     | `TIMESTAMP`      | Timestamp of the latest update       |

### 4. **Allocations Table**
Tracks asset allocations to employees.

| Column Name      | Data Type       | Description                          |
|------------------|-----------------|--------------------------------------|
| `id`             | `INTEGER`       | Primary Key, Auto-incrementing ID    |
| `asset_id`       | `INTEGER`       | Foreign Key referencing the `Assets` table |
| `user_id`        | `INTEGER`       | Foreign Key referencing the `Users` table |
| `allocation_date`| `TIMESTAMP`      | Date when the asset was allocated    |
| `return_date`    | `TIMESTAMP`      | Date when the asset is expected to be returned |

---
## authors
Kihoto Ndoria
Mercy Mumbua
Alvine Mugo
Elvis Muthomi
Abdikhafar Mohamed
Victor Koech

## **Installation**

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/asset-inventory-management.git


