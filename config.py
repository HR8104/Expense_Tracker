import os

class Config:
    """
    Configuration class for the Flask app and database connection.
    """
    # Flask app configurations
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))  # Fetch from environment or generate dynamically
    
    # MySQL database configurations
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')  # Default to 'localhost' if not set
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')       # Default to 'root' if not set
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')  # Default to 'root' if not set
    MYSQL_DB = os.environ.get('MYSQL_DB', 'expense_tracker')   # Default to 'expense_tracker' if not set
