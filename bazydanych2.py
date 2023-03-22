# bazydanych_cwiczenie_01.py

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)

   return conn

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)
# obiekt połączenia do bazy danych (conn) Oferuje on inny obiekt – cursor – przy pomocy którego możemy wykonywać zapytania
# Drugi parametr to text, który jest kodem SQL

if __name__ == "__main__":

   create_wykonawcy_sql = """
   -- wykonawcy table
   CREATE TABLE IF NOT EXISTS wykonawcy (
      id integer PRIMARY KEY,
      nazwa text NOT NULL,
      gatunek text,
   );
   """

   create_utwory_sql = """
   -- utwory table
   CREATE TABLE IF NOT EXISTS utwory (
      id integer PRIMARY KEY,
      wykonawcy_id integer NOT NULL,
      nazwa VARCHAR(250) NOT NULL,
      odtworzenia integer,
      FOREIGN KEY (wykonawcy_id) REFERENCES wykonawcy (id)
   );
   """

   db_file = "playlista.db"

   conn = create_connection(db_file)
   if conn is not None:
       execute_sql(conn, create_wykonawcy_sql)
       execute_sql(conn, create_utwory_sql)
       conn.close()

# ex_03.py
import sqlite3

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except sqlite3.Error as e:
       print(e)
   return conn

def add_wykonawca(conn, wykon):
   """
   Create a new wykonawca into the wykonawcy table
   :param conn:
   :param wykonawca:
   :return: wykonawca_id
   """
   sql = '''INSERT INTO wykonawcy (nazwa, gatunek)
             VALUES(?,?)'''
   cur = conn.cursor()
   cur.execute(sql, wykon)
   conn.commit()
   return cur.lastrowid

def add_utwory(conn, utwor):
   """
   Create a new task into the tasks table
   :param conn:
   :param utwor:
   :return: utwor_id
   """
   sql = '''INSERT INTO utwory(wykonawcy_id, nazwa, odtworzenia)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, utwor)
   conn.commit()
   return cur.lastrowid

if __name__ == "__main__":
   wykon = ("Gwen Stefani", "pop")

   conn = create_connection("playlista.db")
   wykonawca_id = add_wykonawca(conn, wykon)

   utwor = ( wykonawca_id, "Let me blow your mind", "34")

   utwor_id = add_utwory(conn, utwor)

   print(wykonawca_id, utwor_id)
   conn.commit()

# ex_04_selecty.py

import sqlite3

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except sqlite3.Error as e:
       print(e)
   return conn

def select_wykonawca_by_gatunek(conn, gatunek):
   """
   Query tasks by priority
   :param conn: the Connection object
   :param gatunek:
   :return:
   """
   cur = conn.cursor()
   cur.execute("SELECT * FROM wykonawcy WHERE gatunek=?", ("pop",))

   rows = cur.fetchall()
   return rows