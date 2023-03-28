import sqlite3
from sqlite3 import Error
import sqlalchemy
from sqlalchemy import create_engine

db_file = "database.db"

#NAWIĄZANIE POŁĄCZENIA Z BAZĄ 
def create_connection(db_file):
   """ create a database connection to a SQLite database """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   #finally:
   #    if conn:
   #        conn.close()
   return conn

#def create_connection_in_memory():
#   """ create a database connection to a SQLite database """
#   conn = None
#   try:
#       conn = sqlite3.connect(":memory:")
#       print(f"Connected, sqlite version: {sqlite3.version}")
#   except Error as e:
#       print(e)
#   finally:
#       if conn:
#           conn.close()

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

#POZOSTAŁE FUNKCJE OPERACJI NA BAZIE - CRUD
def add_project(conn, project):
   """
   Create a new project into the projects table
   :param conn:
   :param project:
   :return: projekt id
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
   sql = '''INSERT INTO tasks(projekt_id, nazwa, opis, status, start_date, end_date)
             VALUES(?,?,?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, task)
   conn.commit()  
   return cur.lastrowid

def select_task_by_status(conn, status):
   """
   Query tasks by priority
   :param conn: the Connection object
   :param status:
   :return:
   """
   cur = conn.cursor()
   cur.execute("SELECT * FROM tasks WHERE status=?", ("started", ))

   rows = cur.fetchall()
   return rows

def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   return rows

def select_where(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

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

# MAIN -  OPISANIE PAR. OBIEKTÓW, WYWOŁANIE F.
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
      projekt_id integer NOT NULL,
      nazwa VARCHAR(250) NOT NULL,
      opis TEXT,
      status VARCHAR(15) NOT NULL,
      start_date text NOT NULL,
      end_date text NOT NULL,
      FOREIGN KEY (projekt_id) REFERENCES projects(id)
   );
   """
      
   conn = create_connection(db_file)
   if conn is not None:
       execute_sql(conn, create_projects_sql)
       execute_sql(conn, create_tasks_sql)
       #conn.close()

   project = ("Inne powtórki", "2020-05-11 00:00:00", "2020-05-13 00:00:00")
   pr_id = add_project(conn, project)

   task = (
       pr_id,
       "Czasowniki nieregularne",
       "Zapamiętaj czasowniki ze strony 30",
       "started",
       "2020-05-11 12:00:00",
       "2020-05-11 15:00:00"
   )

   task_id = add_task(conn, task)

   print(pr_id, task_id)
   conn.commit()
   print(select_task_by_status(conn, status="started"))

   delete_all(conn, "tasks")
   delete_all(conn, "projects")





#https://python101.readthedocs.io/pl/latest/bazy/sql/


engine = create_engine('sqlite:///database.db')
print(engine.driver)
print(engine.table_names())
print(engine.execute("SELECT * FROM tasks"))
results = engine.execute("SELECT * FROM tasks")
for r in results:
   print(r)

