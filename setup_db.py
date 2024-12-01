import mysql.connector

def setup_database():
    try:
        # Connect to MySQL server (without specifying a database)
        connection = mysql.connector.connect(
            host="localhost", # Replace with your MySQL server host
            user="root",  # Replace with your MySQL username
            password="root"  # Replace with your MySQL password
        )
        cursor = connection.cursor()

        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
        print("Database 'expense_tracker' checked/created successfully!")

        # Reconnect to the created database
        connection.database = "expense_tracker"

        # Create the 'expenses' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                amount DECIMAL(10, 2),
                category VARCHAR(100),
                date DATE
            )
        """)
        print("Table 'expenses' checked/created successfully!")

        # Create the 'users' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        print("Table 'users' checked/created successfully!")

        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Database setup completed successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    setup_database()
