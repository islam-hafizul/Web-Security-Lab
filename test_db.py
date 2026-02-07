#!/usr/bin/env python3
import sqlite3
import os

print("🔍 Checking database setup...")

# Check if database file exists
db_path = 'database/vulnerable.db'
if os.path.exists(db_path):
    print(f"Database file exists: {db_path}")
    
    # Check contents
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"📊 Tables found: {[table[0] for table in tables]}")
    
    # Count users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"👤 Number of users: {user_count}")
    
    # Show sample users
    cursor.execute("SELECT username, email, role FROM users LIMIT 3")
    users = cursor.fetchall()
    print("📝 Sample users:")
    for user in users:
        print(f"  - {user[0]} ({user[1]}) - {user[2]}")
    
    conn.close()
else:
    print("Database file not found!")
    print("Run: python database/init_db.py")