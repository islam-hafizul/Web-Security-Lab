from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key in production
csrf = CSRFProtect(app)

def init_database():
    """Initialize the database if it doesn't exist"""
    db_path = 'database/vulnerable.db'
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print("Database not found. Initializing...")
        from database.init_db import init_database
        init_database()
    else:
        print(f"Database found at: {db_path}")
    
    # Test connection
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")
        conn.close()
    except Exception as e:
        print(f"Error checking database: {e}")

# Database helper function
def get_db_connection():
    conn = sqlite3.connect('database/vulnerable.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on startup
init_database()

@app.route('/')
def index():
    return render_template('index.html')

# Test route to verify database connection
@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM users LIMIT 5")
        users = cursor.fetchall()
        conn.close()
        return f"Database connection successful! Found {len(users)} users."
    except Exception as e:
        return f"Database error: {str(e)}"
    
@app.route('/sqli')
def sqli():
    return render_template('sqli.html')

@app.route('/sqli/vulnerable', methods=['POST'])
def sqli_vulnerable():
    username = request.form.get('username', '')
    
    query = f"SELECT * FROM users WHERE username = '{username}'"  # VULNERABLE: Direct string concatenation
    
    conn = get_db_connection()
    try:
        cursor = conn.execute(query)
        results = cursor.fetchall()
        users = [dict(row) for row in results]
    except Exception as e:
        users = []
        error = str(e)
    finally:
        conn.close()
    
    return jsonify({'users': users, 'query': query})

@app.route('/sqli/secure', methods=['POST'])
def sqli_secure():
    username = request.form.get('username', '')
    
    query = "SELECT * FROM users WHERE username = ?"   # SECURE: Parameterized query
    
    conn = get_db_connection()
    try:
        cursor = conn.execute(query, (username,))
        results = cursor.fetchall()
        users = [dict(row) for row in results]
    except Exception as e:
        users = []
        error = str(e)
    finally:
        conn.close()
    
    return jsonify({'users': users, 'query': query})

@app.route('/csrf')
def csrf_page():
    return render_template('csrf.html')

@app.route('/csrf/vulnerable/transfer', methods=['POST'])
def csrf_vulnerable_transfer():
    amount = request.form.get('amount')
    to_account = request.form.get('to_account')
    return f"Transferred ${amount} to account {to_account} (No CSRF protection!)"

if __name__ == '__main__':
    app.run(debug=True, port=5000)