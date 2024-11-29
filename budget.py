# budget.py

from db import create_connection

def check_budget(category, budget):
    """
    Check if the total spending in a category exceeds the budget.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(amount) FROM expenses WHERE category = %s
    ''', (category,))
    total_spent = cursor.fetchone()[0] or 0  # Default to 0 if no expenses in that category
    
    if total_spent > budget:
        print(f"Warning: You have exceeded your budget for {category}.")
    else:
        print(f"You've spent {total_spent} out of your {budget} budget for {category}.")
    
    cursor.close()
    conn.close()
