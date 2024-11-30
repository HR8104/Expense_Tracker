from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from expense import add_expense, view_expenses, filter_expenses
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object(Config)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'root'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'expense_tracker'
mysql = MySQL(app)

# Home route (This will now render dashboard.html instead of index.html)
@app.route('/dashboard')
def home():
    return render_template('dashboard.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Hash the password using pbkdf2:sha256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create cursor and execute query
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(email, username, password) VALUES(%s, %s, %s)", (email, username, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Create cursor and execute query
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):  # user[3] is the hashed password
            session['user_id'] = user[0]
            session['username'] = user[2]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to index route (index.html)
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')


# Add expense route
@app.route('/add', methods=['GET', 'POST'])
def add_expense_page():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        add_expense(name, amount, category, date)
        return redirect(url_for('view_expenses_page'))
    
    return render_template('add_expense.html')

# View expenses route
@app.route('/view')
def view_expenses_page():

    # Fetch expenses from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    # Calculate total expense
    total_expense = sum(expense[2] for expense in expenses)

    # Calculate total by category
    total_by_category = {}
    for expense in expenses:
        category = expense[3]
        amount = expense[2]
        if category in total_by_category:
            total_by_category[category] += amount
        else:
            total_by_category[category] = amount
    
    cur.close()

    return render_template('view_expenses.html', expenses=expenses, total_expense=total_expense, total_by_category=total_by_category)


@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('view_expenses_page'))

# Function to create a database connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='expense_tracker'  # Replace with your database name
    )

# Function to filter expenses based on category, start_date, and end_date
def filter_expenses(category=None, start_date=None, end_date=None):
    # Use MySQL connection from flask_mysqldb (no need to use mysql.connector)
    cur = mysql.connection.cursor()

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

    cur.execute(query, tuple(params))
    expenses = cur.fetchall()

    cur.close()
    
    return expenses

@app.route('/filter', methods=['GET', 'POST'])
def filter_expenses_page():
    expenses = []
    category = None
    start_date = None
    end_date = None
    
    if request.method == 'POST':
        category = request.form.get('category')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Check if the date format is correct and convert to proper format
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = None  # Invalid date format

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                end_date = None  # Invalid date format

        # Call the filter function with the processed parameters
        expenses = filter_expenses(category, start_date, end_date)
    
    return render_template('filter_expenses.html', expenses=expenses)

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))  # Redirect to the home page (index.html)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
