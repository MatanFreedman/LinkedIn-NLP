import sqlite3
from pathlib import Path
import logging


class DBConnection:
    """Database connection object. 

    Notes
    -----
    The object will check for a db called "linkedin_data.db" in the data folder and will 
    create one if it doesn't find it.


    Attributes
    ---------
    project_path : str
        root path string
    data_path : str
        path of data folder for saving files
    conn : sqlite3 connection
        used to connect to DB
    cur : sqlite3 cursor
        used to execute queries with DB
    """

    def __init__(self, rel_path="/data/raw/linkedin_data.db"):
        project_path = Path(__file__).resolve().parents[2]
        DB_path = str(project_path) + str(rel_path)
        self.conn = sqlite3.connect(DB_path)
        self.cur = self.conn.cursor()
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
        self.cur.execute("""CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY NOT NULL
            );
        """)
        self.conn.commit()

    def close(self):
        """Close DB connection"""
        self.conn.close()

    def is_duplicate(self, data):
        """Check if data is duplicate

        Parameters
        ---------
        data : tuple of str
            (position, company, location, details) - all strings

        Returns
        -------
            bool if duplicate
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
            return False 
        else:
            return True


    def insert_position(self, data):
        """Inserts into DB.

        Parameters
        ---------
        data : tuple : (position, company, location, details) - all strings
        """
        self.cur.execute("""
            INSERT INTO positions(position, company, location, details, date) VALUES (?, ?, ?, ?, date('now'))
            """, data)
        self.conn.commit()

    

if __name__ == "__main__":
    db = DBConnection()
