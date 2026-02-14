import sqlite3
import os

def init_database():
    # Create database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)
    
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect('database/vulnerable.db')
    cursor = conn.cursor()
    
    # Drop tables if they exist (for clean restart)
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS posts')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create posts table
    cursor.execute('''
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create comments table for XSS demo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert sample users
    sample_users = [
        ('admin', 'admin123', 'admin@example.com', 'admin'),
        ('john_doe', 'password123', 'john@example.com', 'user'),
        ('alice_smith', 'alice123', 'alice@example.com', 'user'),
        ('bob_jones', 'bob123', 'bob@example.com', 'user'),
        ('eve_attacker', 'hackme', 'eve@evil.com', 'user')
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, password, email, role)
        VALUES (?, ?, ?, ?)
    ''', sample_users)
    
    # Insert sample posts
    sample_posts = [
        ('Welcome to our platform', 'This is a sample post. Feel free to explore!', 1),
        ('Security Notice', 'Always validate user input and use parameterized queries!', 2),
        ('About SQL Injection', 'SQL injection attacks can be prevented with proper coding practices.', 3)
    ]
    
    cursor.executemany('''
        INSERT INTO posts (title, content, user_id)
        VALUES (?, ?, ?)
    ''', sample_posts)
    
    # Insert sample comments for XSS demo
    sample_comments = [
        ('Great post! Looking forward to more security content.', 2),
        ('I learned a lot about SQL injection from this.', 3),
        ('<script>alert("This is malicious!")</script>', 5)
    ]
    
    cursor.executemany('''
        INSERT INTO comments (content, user_id)
        VALUES (?, ?)
    ''', sample_comments)
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")
    print("Sample data inserted:")
    print("   - 5 users (including 'admin' and 'eve_attacker')")
    print("   - 3 blog posts")
    print("   - 3 comments (including one XSS payload)")

if __name__ == '__main__':
    init_database()