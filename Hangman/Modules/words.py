import sqlite3
from sqlite3 import Error

database_path = 'Database/hangman'

def create_connection():
    conn = sqlite3.connect(database_path)
    return conn


def insert_words_to_database(word_list):
    sql = '''INSERT INTO Words(word) VALUES(?)'''
    conn = create_connection()
    cursor = conn.cursor()
    for word in word_list:
        cursor.execute(sql, (word,))
    conn.commit()  
    conn.close()  

def retrieve_all_words():
    conn = create_connection()
    sql = 'SELECT word FROM Words'
    cursor = conn.cursor()
    cursor.execute(sql)
    words = cursor.fetchall()
    conn.close()
    return [word[0] for word in words]




