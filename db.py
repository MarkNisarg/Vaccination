import sqlite3

class Database:
  def __init__(self, path):
    self.conn = sqlite3.connect(path)

  def select(self, sql, parameters=[]):
    c = self.conn.cursor()
    c.execute(sql, parameters)
    return c.fetchall()

  def execute(self, sql, parameters=[]):
    c = self.conn.cursor()
    c.execute(sql, parameters)
    self.conn.commit()

  def close(self):
    self.conn.close()
