import sqlite3
from pathlib import Path


class DBConnection:
    project_path = Path(__file__).resolve().parents[2]
    data_path = str(project_path) + "/data/raw/"
    conn = sqlite3.connect(data_path + 'linedin_data.db')
    cur = conn.cursor()

    def __init__(self):
        self.initialize()

    def initialize(self):
        """Check if DB exists, create table if it doesnt
        """
        self.cur.execute("""CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY NOT NULL,
            position TEXT,
            company TEXT,
            location TEXT,
            details TEXT,
            date INT
            );
        """)
        self.conn.commit()

    def close(self):
        """Close DB connection"""
        self.conn.close()

    def insert_position(self, data):
        """Checks for duplicate in DB, inserts if no dup.
        """
        # check DB for duplicate:
        self.cur.execute("""
            SELECT *
            FROM positions
            WHERE position = ?
            AND company = ?
            AND location = ?
            AND details = ?
            ;
            """, data)

        if self.cur.fetchone() is None:
            # if no duplicate, insert and commit:
            self.cur.execute("""
            INSERT INTO positions(position, company, location, details, date) VALUES (?, ?, ?, ?, date('now'))
            """, data)
            self.conn.commit()

if __name__ == "__main__":
    db = DBConnection()
