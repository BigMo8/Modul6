import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to a SQLite database """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   return conn
   #finally:
   #    if conn:
   #        conn.close()

#def create_connection_in_memory():
#   """ create a database connection to a SQLite database """
#   conn = None
#   try:
#       conn = sqlite3.connect(":memory:")
#       print(f"Connected, sqlite version: {sqlite3.version}")
#   except Error as e:
#       print(e)
#   finally:
#      if conn:
#           conn.close()

if __name__ == '__main__':
   create_connection(r"database.db")
   #create_connection_in_memory()

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
   wykon = ("Guano Apes", "rock")

   conn = create_connection("playlista.db")
   wykonawca_id = add_wykonawca(conn, wykon)

   utwor = ( wykonawca_id, "Open your eye", "19")

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

# ex_05_update.py

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by the db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
   except Error as e:
       print(e)

   return conn

def update(conn, table, id, **kwargs):
   """
   update wykonawcy_id, nazwa, odtworzenia
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

if __name__ == "__main__":
   conn = create_connection("playlista.db")
   update(conn, "utwory", 1, odtworzenia=89)
   conn.close()

# ex_06_delete.py

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

def delete_where(conn, table, **kwargs):
   """
   Delete from table where attributes from
   :param conn:  Connection to the SQLite database
   :param table: table name
   :param kwargs: dict of attributes and values
   :return:
   """
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

def delete_all(conn, table):
   """
   Delete all rows from table
   :param conn: Connection to the SQLite database
   :param table: table name
   :return:
   """
   sql = f'DELETE FROM {table}'
   cur = conn.cursor()
   cur.execute(sql)
   conn.commit()
   print("Deleted")

if __name__ == "__main__":
   conn = create_connection("playlista.db")
   #delete_where(conn, "utwory", id=4)
   #delete_all(conn, "wykonawcy")
   #delete_all(conn, "utwory")
