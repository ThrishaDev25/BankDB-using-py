# Secure Bank - Banking Management System

## Introduction

Secure Bank is a database-driven banking management system implemented in Python using MySQL as the database. This project allows users to sign up, log in, open a new account, perform transactions, and manage their banking details.

## Features

- **Sign Up:** New users can sign up for an account with a unique username and password.
- **Login:** Users can log in with their credentials securely.
- **Account Operations:**
  - Open a new account
  - Deposit amount
  - Withdraw amount
  - Balance enquiry
  - Customer details
  - Update information
  - Close account
  - Show account data/information

## Technologies Used

- Python
- MySQL
- PrettyTable

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/secure-bank.git
   cd secure-bank
# Install Dependencies:
bash
Copy code
pip install mysql-connector-python prettytable
# Database Configuration:
Make sure you have a MySQL server running.
Update the database connection details in the script (localhost, user, password, database).
# Run the Application:
bash
Copy code
python secure_bank.py
# Usage
Run the script and choose between signing up and logging in.
Perform various banking operations as per the provided menu options.
# Additional Notes
Make sure to handle the MySQL server credentials securely.
Use virtual environments to manage Python dependencies.
# License
This project is licensed under the MIT License.
