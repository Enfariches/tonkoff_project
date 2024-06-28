import sqlite3
from datetime import datetime

def init_user(user_id):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO profile (user_username, user_score, last_reset_time) VALUES (?, ?, ?)',
                   (user_id, 0, None))
    conn.commit()
    conn.close()

def get_user_score(user_id):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_score FROM profile WHERE user_username = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_score(user_id, new_score):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE profile SET user_score = ? WHERE user_username = ?', (new_score, user_id))
    conn.commit()
    conn.close()

def get_last_reset_time(user_id):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('SELECT last_reset_time FROM profile WHERE user_username = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return datetime.fromisoformat(result[0]) if result and result[0] else None

def update_last_reset_time(user_username, reset_time):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE profile SET last_reset_time = ? WHERE user_username = ?', (reset_time.isoformat(), user_username))
    conn.commit()
    conn.close()

def reset_score(user_id):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE profile SET user_score = ? WHERE user_username = ?', (0, user_id))
    conn.commit()
    conn.close()
