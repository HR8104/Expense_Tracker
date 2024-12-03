from db import create_connection

def add_expense(name, amount, category, date):
    """
    Add an expense to the database.
    """
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # SQL query to insert the expense
        query = "INSERT INTO expenses (name, amount, category, date) VALUES (%s, %s, %s, %s)"
        values = (name, amount, category, date)
        cursor.execute(query, values)
        conn.commit()

        print(f"Expense '{name}' added successfully!")  # Debug log
        
    except Exception as err:
        print(f"Error while adding expense: {err}")
    finally:
        cursor.close()
        conn.close()

def view_expenses():
    """
    Retrieve all expenses from the database.
    """
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # SQL query to fetch all expenses
        query = "SELECT * FROM expenses"
        cursor.execute(query)
        expenses = cursor.fetchall()  # Returns a list of tuples

        # Debug log
        print(f"Fetched expenses: {expenses}")
        return expenses

    except Exception as err:
        print(f"Error while fetching expenses: {err}")
        return []  # Return an empty list if an error occurs
    finally:
        cursor.close()
        conn.close()

def filter_expenses(category=None, start_date=None, end_date=None):
    """
    Filter expenses by category and/or date range.
    """
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Build dynamic SQL query
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []

        if category:
            query += " AND category = %s"
            params.append(category)
        
        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)

        # Debug log
        print(f"Executing query: {query} with params: {params}")
        cursor.execute(query, tuple(params))
        expenses = cursor.fetchall()

        if expenses:
            # Debug log for filtered results
            for expense in expenses:
                print(f"ID: {expense[0]}, Name: {expense[1]}, Amount: {expense[2]}, Category: {expense[3]}, Date: {expense[4]}")
        else:
            print("No expenses found for the given filter criteria.")  # Debug message if no results

        return expenses

    except Exception as err:
        print(f"Error while filtering expenses: {err}")
        return []  # Return an empty list if an error occurs
    finally:
        cursor.close()
        conn.close()
