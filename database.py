"""
database.py
Handles everything related to the SQLite connection: creating the
database file, creating tables, running queries, and closing up.
No business logic lives here on purpose — that's student_service.py's job.
"""

import sqlite3
from config import DATABASE_NAME


class Database:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()
        return self.connection

    def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS students (
            student_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT NOT NULL,
            age            INTEGER NOT NULL,
            gender         TEXT,
            department     TEXT NOT NULL,
            year           INTEGER,
            email          TEXT UNIQUE NOT NULL,
            phone          TEXT,
            address        TEXT,
            admission_date TEXT,
            cgpa           REAL
        )
        """
        self.execute(query)

    def execute(self, query, params=()):
        """For INSERT / UPDATE / DELETE. Commits and returns the cursor
        so callers can inspect rowcount or lastrowid."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"[DATABASE ERROR] {e}")
            raise

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        if self.connection:
            self.connection.close()
