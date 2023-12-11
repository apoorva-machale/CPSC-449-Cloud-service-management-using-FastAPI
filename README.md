# Project Teammates
Padmini
Apoorva Machale 
Akshay Patil
Devashri Manepatil

# FastAPI Project Setup Guide

This guide provides step-by-step instructions on how to set up and run this FastAPI project using a virtual environment and MongoDB cloud database.

## Prerequisites

- Git
- Python 3.x

## Setup Instructions

### 1. Clone the Repository

Clone the project repository by running:

```bash
git clone https://github.com/Padmini-RK/CPSC-449-Cloud-service-management-using-FastAPI.git
```
### 2. Virtual Environment Setup

A virtual environment is recommended for Python projects.

#### 2.1 Create Virtual Environment
Create a virtual environment in the project directory:

```bash
py -m venv ./venv-fastapi
```
#### 2.2 Activate Virtual Environment
Activate the virtual environment
On Windows:
```bash
.\venv-fastapi\Scripts\activate
```
### 3. Install Dependencies

Install the required packages from requirements.txt:

```bash
pip install -r requirements.txt
```
### 4. MongoDB Cloud Database Setup
#### 4.1 Create MongoDB Cloud Account
Create an account at MongoDB Cloud.

#### 4.2 Setup Database
Navigate to the database section in MongoDB Cloud and set up your database.

#### 4.3 Connect to the Database
Follow the steps to connect your application to the database.

#### 4.4 Drivers Setup
In the 'Drivers' section, keep the default settings.

### 5. Run the Application
Start the FastAPI application using Uvicorn:

``` bash
uvicorn main:app --reload
```
### 6. Accessing the API
Access the Swagger UI to interact with the API at the localhost url.

### 7. Add Admin user
Access the Swaager UI, register admin user using register api. { "username": "userA", "email": "userA@gmail.com", "role": "admin", "password": "abcd1234" }

### 8. Setup Permissions
Add first create_permission to the admin user Navigate to routes/permissions.py file .In /create_permission API .Comment the below lines: //if not await validate_permission("create_permission",token): // raise HTTPException(status_code=403,detail=f"User is not authorised to perform this action") for adding first create permission

Get the token from /login API. Copy the token and put token in /create_permission API

Hit /create_permissions API with following payload { "permissionName": "create_permission", "role": "admin" }

Once this permission is added successfully . Uncomment the commented lines in step1

Get the new token from /login API

Now we need to add permissions for Admin and constomer role as required in API.

Below is list of permissions for Admin:
update_subscription
list_all_subscriptions
delete_subscription
add_subscription 
list_role_permissions
delete_permissions
list_role_permissions
create_permission

Below is list of permissions for Customer:
update_own_subscription
get_own_subscription
get_own_subscription_details

