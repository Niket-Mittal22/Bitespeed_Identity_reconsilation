import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('bitespeed.db')
    cursor = conn.cursor()

    create_query = '''
    CREATE TABLE IF NOT EXISTS Contact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phoneNumber TEXT,
        email TEXT,
        linkedId INTEGER,
        linkPrecedence TEXT CHECK(linkPrecedence IN ('primary', 'secondary')),
        createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
        updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
        deletedAt DATETIME
    );
    '''

    cursor.execute(create_query)
    conn.commit()
    conn.close()

    print("Database and Contact table created successfully.")


if __name__ == "__main__":
    create_database()