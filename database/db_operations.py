import sqlite3


def create_database():

    conn = sqlite3.connect(
        "database/compliance.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS violations(
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        violation_type TEXT
    )
    """)

    conn.commit()
    conn.close()