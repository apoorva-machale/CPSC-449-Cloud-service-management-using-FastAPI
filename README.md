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
