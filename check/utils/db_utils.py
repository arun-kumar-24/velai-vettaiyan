import sqlite3
import os

DB_NAME = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visited_internships (
            id TEXT PRIMARY KEY,
            visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_visited(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM visited_internships WHERE id = ?", (job_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_visited(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO visited_internships (id) VALUES (?)", (job_id,))
        conn.commit()
    except:
        pass
    finally:
        conn.close()
