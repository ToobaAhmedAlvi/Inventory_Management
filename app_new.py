from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pyodbc
import secrets


app = Flask(__name__)

secure_key = secrets.token_hex(24)  # Generates a 48-character hex string

app.secret_key = secure_key # Replace with a secure secret key

# SQL Server Database configuration
DB_CONFIG = {
    'server': '(localdb)\MSSQLLOCALDB',       # Replace with your SQL Server name
    'database': 'Inventory',          # Replace with your database name
    #'username': 'your_username',        # Replace with your SQL Server username
    #'password': 'your_password',        # Replace with your SQL Server password
    'driver': '{ODBC Driver 17 for SQL Server}'  # Ensure the correct ODBC driver is installed
}

# Function to connect to the SQL Server database
def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        #f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']}"
    )
    return conn

# Initialize the database (run this manually to create tables)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create user_details table
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='user_details' AND xtype='U')
        CREATE TABLE user_details (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(50) UNIQUE NOT NULL,
            password NVARCHAR(255) NOT NULL
        );
    """)
    # Create inventory details table
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='inventory_details' AND xtype='U')
        CREATE TABLE inventory_details (
            id INT IDENTITY(1,1) PRIMARY KEY,
            item_name NVARCHAR(100) NOT NULL,
            price FLOAT NOT NULL,
            vendor_name NVARCHAR(100) NOT NULL,
            date_added DATE NOT NULL,
            quantity INT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

   


@app.route('/')
def home():
    init_db()
    return "Flask is working!"
'''
# Route: Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO user_details (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Sign-up successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except pyodbc.IntegrityError:
            flash('Username already exists.', 'danger')
        finally:
            conn.close()
    return render_template('signup.html')

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_details WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

# Route: Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', items=items)

# Route: Add Inventory Item
@app.route('/add_item', methods=['POST'])
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    item_name = request.form['item_name']
    price = request.form['price']
    vendor_name = request.form['vendor_name']
    date_added = datetime.now().strftime('%Y-%m-%d')
    quantity = request.form['quantity']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inventory (item_name, price, vendor_name, date_added, quantity)
        VALUES (?, ?, ?, ?, ?)
    """, (item_name, price, vendor_name, date_added, quantity))
    conn.commit()
    conn.close()

    flash('Item added successfully!', 'success')
    return redirect(url_for('dashboard'))

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))
'''



if __name__ == '__main__':
    app.run(debug=True)
