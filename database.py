import sqlite3

def get_connection():
    conn = sqlite3.connect('tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            genre TEXT,
            rating INTEGER,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(title, type_, genre, rating, notes):
    conn = get_connection()
    conn.execute('''
        INSERT INTO entries (title, type, genre, rating, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, type_, genre, rating, notes))
    conn.commit()
    conn.close()
def get_all_entries(type_filter=None):
    conn=get_connection()
    if type_filter:
        entries =conn.execute('SELECT * from entries WHERE type= ? ORDER BY id DESC',(type_filter,)).fetchall()
    else:

        entries =conn.execute('SELECT * from entries ORDER BY id DESC').fetchall()
    conn.close()
    return entries
def get_taste_profile():
    conn=get_connection()

    avg_by_genre=conn.execute('''SELECT genre, ROUND(AVG(rating), 1) as avg_rating, COUNT(*) as count
        FROM entries
        WHERE genre IS NOT NULL
        GROUP BY genre
        ORDER BY avg_rating DESC''').fetchall()
    type_split=conn.execute('''SELECT type, COUNT(*) as count
        FROM entries
        GROUP BY type''').fetchall()
    conn.close()
    return {
        'avg_by_genre': avg_by_genre,
        'type_split': type_split
    }
def get_notes_sample():
    conn = get_connection()
    notes = conn.execute('''
        SELECT title, type, genre, rating, notes 
        FROM entries 
        WHERE notes IS NOT NULL
        ORDER BY rating DESC
        LIMIT 10
    ''').fetchall()
    conn.close()
    return notes