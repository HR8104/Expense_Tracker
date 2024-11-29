# db.py

import mysql.connector

def create_connection():
    """
    Create and return a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host="localhost",      # MySQL server host
        user="root",  # MySQL username
        password="12345",  # MySQL password
        database="expense_tracker"  # Database name
    )




