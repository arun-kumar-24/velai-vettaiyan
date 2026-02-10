import sqlite3
import os

DB_NAME = "jobs.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table for storing internship details
    # We store skills as a comma-separated string for simplicity
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internships (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            stipend TEXT,
            duration TEXT,
            type TEXT,
            skills TEXT,
            link TEXT,
            score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table for tracking visited internship IDs to avoid processing/notifying again
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visited_internships (
            id TEXT PRIMARY KEY,
            visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized with table 'internships'.")

if __name__ == "__main__":
    create_table()
