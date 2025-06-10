# Proxima Centauri community
Welcome to the backend of the Proxima Centauri community ! This project is built with Flask and SQLAlchemy. 
It handles user authentication, transaction management, and database interactions, all while using JWT for secure authentication.
## Features
 User Authentication: Users can register and log in using JWT tokens.
Transactions: Users can deposit money into different groups.
Database Management: Utilizes SQLAlchemy for handling users, groups, and transaction data.

## Tech Stack
Backend: Flask, SQLAlchemy, JWT
Database: SQLite (or any relational database supported by SQLAlchemy)
Authentication: JWT (JSON Web Token)

## Setup Instructions
### Prerequisites
Before you begin, ensure you have the following installed:
Python 3.x
pip (Python package installer)

## Steps to Set Up Locally
Clone the repository:
git clone git@github.com:roselyne30/proxima-backend.git
cd proxima-backend.git
Create a virtual environment 
python3 -m venv venv
source  venv\Scripts\activate

###  Install the necessary dependencies:

pip install -r requirements.txt
Set up the database:

from app import db
db.create_all()  # Creates the database tables based on the models
Run the Flask app:

python run.py
The backend should now be running at http://localhost:5000.

API Endpoints
Authentication
POST /register: Register a new user.

Request: { "username": "user", "password": "password123", "email": "user@gmail.com"}

Response: Success message or error.

POST /login: Log in to an existing user account.

Request: { "username": "user", "password": "password123" }

Response: { "access_token": "JWT_TOKEN" }

Transactions
POST /deposit: Make a deposit into a group.

Request: { "amount": 100, "name": "Money Group" }

Response: Success message or error.

GET /transactions/{group_id}: Get transaction history for a group.

Response: A list of transactions for the specified group.


