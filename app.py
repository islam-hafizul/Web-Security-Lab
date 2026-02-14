from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import html
import re 

app = Flask(__name__)

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

@app.route('/test-db')
def test_db():
    """Test route to verify database connection"""
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM users LIMIT 5")
        users = cursor.fetchall()
        conn.close()
        return f"Database connection successful! Found {len(users)} users."
    except Exception as e:
        return f"Database error: {str(e)}"
    
@app.route('/sqli')
def sqli_page():
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
    
    # SECURE: Parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    
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

@app.route('/xss')
def xss_page():
    return render_template('xss.html')

@app.route('/xss/vulnerable', methods=['POST'])
def xss_vulnerable():
    comment = request.form.get('comment', '')
    return jsonify({'comment': comment})   # VULNERABLE: No escaping

@app.route('/xss/secure', methods=['POST'])
def xss_secure():
    comment = request.form.get('comment', '')
    escaped_comment = html.escape(comment)  # SECURE: Escape user input
    return jsonify({'comment': escaped_comment})
@app.route('/validation')
def validation():
    return render_template('validation.html')

@app.route('/validation/vulnerable', methods=['POST'])
def validation_vulnerable():
    email = request.form.get('email', '')
    age = request.form.get('age', '')
    # VULNERABLE: No validation
    return jsonify({'email': email, 'age': age, 'status': 'accepted'})

@app.route('/validation/secure', methods=['POST'])
def validation_secure():
    email = request.form.get('email', '')
    age = request.form.get('age', '')
    
    errors = []
    
    # Email validation
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append('Invalid email format')
    
    # Age validation
    try:
        age_int = int(age)
        if age_int < 1 or age_int > 120:
            errors.append('Age must be between 1 and 120')
    except ValueError:
        errors.append('Age must be a valid number')
    
    if errors:
        return jsonify({'errors': errors, 'status': 'error'})
    
    return jsonify({'email': email, 'age': age, 'status': 'accepted'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)