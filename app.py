from flask import Flask, render_template
import sqlite3
import os

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)