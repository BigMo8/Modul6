# ex_02_create_tables.py

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

   create_projects_sql = """
   -- projects table
   CREATE TABLE IF NOT EXISTS projects (
      id integer PRIMARY KEY,
      nazwa text NOT NULL,
      start_date text,
      end_date text
   );
   """

   create_tasks_sql = """
   -- zadanie table
   CREATE TABLE IF NOT EXISTS tasks (
      id integer PRIMARY KEY,
      project_id integer NOT NULL,
      nazwa VARCHAR(250) NOT NULL,
      opis TEXT,
      status VARCHAR(15) NOT NULL,
      start_date text NOT NULL,
      end_date text NOT NULL,
      FOREIGN KEY (project_id) REFERENCES projects(id)
   );
   """

   db_file = "database.db"

   conn = create_connection(db_file)
   if conn is not None:
       execute_sql(conn, create_projects_sql)
       execute_sql(conn, create_tasks_sql)
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

def add_project(conn, project):
   """
   Create a new project into the projects table
   :param conn:
   :param project:
   :return: project id
   """
   sql = '''INSERT INTO projects(nazwa, start_date, end_date)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, project)
   conn.commit()
   return cur.lastrowid

def add_task(conn, task):
   """
   Create a new task into the tasks table
   :param conn:
   :param task:
   :return: task id
   """
   sql = '''INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
             VALUES(?,?,?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, task)
   conn.commit()
   return cur.lastrowid

if __name__ == "__main__":
   project = ("Powtórka z angielskiego", "2020-05-11 00:00:00", "2020-05-13 00:00:00")

   conn = create_connection("database.db")
   project_id = add_project(conn, project)

   task = (
       project_id,
       "Czasowniki regularne",
       "Zapamiętaj czasowniki ze strony 30",
       "started",
       "2020-05-11 12:00:00",
       "2020-05-11 15:00:00"
   )

   task_id = add_task(conn, task)

   print(project_id, task_id)
   conn.commit()

# from ex_04_selecty import *
#import sqlite3
#from sqlite3 import Error

#def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by the db_file
   :param db_file: database file
   :return: Connection object or None
   """
#   conn = None
#   try:
#       conn = sqlite3.connect(db_file)
#   except Error as e:
#       print(e)

#   return conn

#def select_task_by_status(conn, status):
   """
   Query tasks by priority
   :param conn: the Connection object
   :param status:
   :return:
   """
#   cur = conn.cursor()
#   cur.execute("SELECT * FROM tasks WHERE status=?", ("started", ))

#   rows = cur.fetchall()
#   return rows

#def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
#   cur = conn.cursor()
#   cur.execute(f"SELECT * FROM {table}")
#   rows = cur.fetchall()

#   return rows

#def select_where(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
#   cur = conn.cursor()
#   qs = []
#   values = ()
#   for k, v in query.items():
#       qs.append(f"{k}=?")
#       values += (v,)
#   q = " AND ".join(qs)
#   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
#   rows = cur.fetchall()
#   return rows

   #https://python101.readthedocs.io/pl/latest/bazy/sql/

import sqlalchemy
sqlalchemy.__version__
