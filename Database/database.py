import sqlite3

path = 'g3--group_5/Database/hangman'

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect(path)
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date_played TEXT DEFAULT CURRENT_TIMESTAMP)''')

conn.commit()
conn.close()
