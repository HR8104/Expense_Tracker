from db import create_connection

def check_budget(category, budget):
    """
    Check if the total spending in a category exceeds the budget.
    """
    connection = create_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            # Query to calculate total spending in the specified category
            query = '''
                SELECT SUM(amount) FROM expenses WHERE category = %s
            '''
            cursor.execute(query, (category,))
            total_spent = cursor.fetchone()[0] or 0  # Default to 0 if no expenses found

            # Compare the total spent with the budget
            if total_spent > budget:
                print(f"Warning: You have exceeded your budget for {category}.")
            else:
                print(f"You've spent {total_spent} out of your {budget} budget for {category}.")
        except Exception as e:
            print(f"Error checking budget: {e}")
        finally:
            # Ensure resources are properly closed
            cursor.close()
            connection.close()
    else:
        print("Unable to connect to the database.")
