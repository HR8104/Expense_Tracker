# setup.py
import os
import subprocess

def create_config():
    db_host = input("Enter your database host (default: localhost): ") or "localhost"
    db_user = input("Enter your database root ID: ")
    db_password = input("Enter your database root password: ")
    db_name = input("Enter your database name (default: expense_tracker): ") or "expense_tracker"

    config_content = f"""
class Config:
    MYSQL_HOST = '{db_host}'
    MYSQL_USER = '{db_user}'
    MYSQL_PASSWORD = '{db_password}'
    MYSQL_DB = '{db_name}'
    SECRET_KEY = 'your_secret_key'  # Replace with a secure secret key
"""

    with open("config.py", "w") as config_file:
        config_file.write(config_content)

    print("Configuration file created successfully.")

def launch_app():
    # Launch the Flask application
    subprocess.Popen(["python", "app.py"])

if __name__ == "__main__":
    create_config()
    launch_app()