# expense.py

from db import create_connection

import mysql.connector

def add_expense(name, amount, category, date):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='root',  # Replace with your MySQL password
            database='expense_tracker'  # Replace with your database name
        )
        cursor = connection.cursor()

        # SQL query to insert the expense
        query = "INSERT INTO expenses (name, amount, category, date) VALUES (%s, %s, %s, %s)"
        values = (name, amount, category, date)
        cursor.execute(query, values)
        connection.commit()

        print(f"Expense '{name}' added successfully!")  # Debug log
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

import mysql.connector

def view_expenses():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='root',  # Replace with your MySQL password
            database='expense_tracker'  # Replace with your database name
        )
        cursor = connection.cursor()

        # SQL query to fetch all expenses
        query = "SELECT * FROM expenses"
        cursor.execute(query)
        expenses = cursor.fetchall()  # This should return a list of tuples

        print(f"Fetched expenses: {expenses}")  # Debug log
        return expenses  # Make sure this is not None or empty

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []  # Return an empty list in case of error
    finally:
        cursor.close()
        connection.close()


import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='expense_tracker'  # Replace with your database name
    )

def filter_expenses(category=None, start_date=None, end_date=None):
    """
    Filter expenses by category and/or date range.
    """
    conn = create_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM expenses WHERE 1=1'
    params = []

    if category:
        query += ' AND category = %s'
        params.append(category)
    
    if start_date:
        query += ' AND date >= %s'
        params.append(start_date)
    
    if end_date:
        query += ' AND date <= %s'
        params.append(end_date)

    # Debug: print the query and parameters
    print(f"Executing query: {query} with params: {params}")

    cursor.execute(query, tuple(params))
    expenses = cursor.fetchall()

    if expenses:
        for expense in expenses:
            print(f"ID: {expense[0]}, Name: {expense[1]}, Amount: {expense[2]}, Category: {expense[3]}, Date: {expense[4]}")
    else:
        print("No expenses found for the given filter criteria.")  # Debug message if no results are found

    cursor.close()
    conn.close()
