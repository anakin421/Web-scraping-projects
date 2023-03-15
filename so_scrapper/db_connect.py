import sqlite3
from sqlite3 import Error

class database:

    def __init__(self,query):
        self.query = query

    def create_connection(self):

        try:
            self.conn = sqlite3.connect('stack_overflow.db')

        except Error as e:
            print(f"unsuccessful!! Error is: {e}")

        c = self.conn.cursor()
        return c 

    def close_connection(self):
        return self.conn.close()

    def execute(self):
        c = self.create_connection()
        c.execute("PRAGMA foreign_keys = ON")
        try:
            if type(self.query) == tuple:
                c.execute(*self.query)
            else:
                c.execute(self.query)
            data = c.fetchall()
            return data
        except Error as e:
            print(f"unsuccessful!! Error is: {e}")
        finally:
            self.conn.commit()
            c.close()
            self.close_connection()