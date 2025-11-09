#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        if self.params:
            cursor.execute(self.query, self.params)
        else:
            cursor.execute(self.query)
        self.results = cursor.fetchall()
        return self.results  # return results directly

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
        return False  # allow errors to be raised if they occur


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print(results)

