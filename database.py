import sqlite3

def init_db():
    conn = sqlite3.connect('light_data.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS light (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            light_detected INTEGER NOT NULL,
            timestamp DATETIME DEFAULT (datetime('now'))
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()