import sqlite3

def get_schema(table_name):
    conn = sqlite3.connect('data.db')
    cursor = conn.execute(f'PRAGMA table_info("{table_name}")')
    cols = cursor.fetchall()
    conn.close()
    return [{'name': c[1], 'type': c[2]} for c in cols]

def table_exists(table_name):
    conn = sqlite3.connect('data.db')
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
