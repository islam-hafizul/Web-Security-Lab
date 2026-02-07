import sqlite3
import os

def init_database():
    # Create database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)
    
    # Connect to SQLite database (creates file if doesn't exist)
    conn = sqlite3.connect('database/vulnerable.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Check if users table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    
    # Insert sample data only if table is empty
    if count == 0:
        print("Inserting sample data...")
        cursor.executemany('''
            INSERT INTO users (username, password, email, role) 
            VALUES (?, ?, ?, ?)
        ''', [
            ('admin', 'admin123', 'admin@example.com', 'admin'),
            ('john', 'password123', 'john@example.com', 'user'),
            ('alice', 'alice123', 'alice@example.com', 'user'),
            ('test', 'test123', 'test@example.com', 'user'),
            ('user1', 'pass123', 'user1@example.com', 'user')
        ])
        print(f"Inserted {cursor.rowcount} sample users")
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: database/vulnerable.db")
    return True

if __name__ == '__main__':
    init_database()