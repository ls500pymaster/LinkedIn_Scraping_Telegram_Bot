import sqlite3 as sq


def insert_db(username_key, status_value):
    try:
        sqliteConnection = sq.connect('/parserdb.db', timeout=10)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        cursor.execute('INSERT INTO parsing (name, status) VALUES(?, ?)', (username_key, status_value))
        sqliteConnection.commit()
        cursor.close()
        sqliteConnection.close()

    except sq.Error as error:
        print("Failed to read data from sqlite table", error)