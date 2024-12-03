# db.py

import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Create and return a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",       # MySQL server host
            user="root",            # MySQL username
            password="root",        # MySQL password
            database="expense_tracker"  # Database name
        )
        if connection.is_connected():
            print("Connection to the database was successful!")
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None
