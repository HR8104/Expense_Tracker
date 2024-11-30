# config.py

import os

class Config:
    SECRET_KEY = os.urandom(24)  # For Flask sessions
    MYSQL_HOST = 'localhost'  # Your MySQL host
    MYSQL_USER = 'root'       # Your MySQL username
    MYSQL_PASSWORD = 'root'       # Your MySQL password
    MYSQL_DB = 'expense_tracker'      # Your MySQL database name
