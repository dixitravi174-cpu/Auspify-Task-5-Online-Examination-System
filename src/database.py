import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'exam.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    # Insert sample questions if table is empty
    count = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    if count == 0:
        sample_questions = [
            ("Which keyword is used to define a function in Python?", "func", "define", "def", "function", "def"),
            ("What is the output ofprint(2 ** 3)?", "6", "8", "9", "none of these", "8"),
            ("Which data structure is immutable in Python?", "List", "Dictionary", "Tuple", "Set", "Tuple"),
            ("What does API stand for?", "Application Programming Interface", "Advanced Program Integration", "Automated Process Interaction", "Application Program Interaction", "Application Programming Interface"),
            ("Which of the following is a NoSQL database?", "SQLite", "MySQL", "PostgreSQL", "MongoDB", "MongoDB")
        ]
        conn.executemany('''
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_questions)
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Exam database initialized with sample questions!")
