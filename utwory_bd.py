#https://py4e.pl/html3/15-database.php

# ex_01_create_tables.py

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn=None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn
 
def execute_sql(conn, sql):
    try:
       c = conn.cursor()
       c.execute(sql)
    except Error as e:
       print(e)

if __name__ == "__main__":

    create_Wykonawcy_sql="""
    CREATE TABLE IF NOT EXISTS Wykonawcy(
    id integer PRIMARY KEY,
    wykonawca text NOT NULL
    );"""
    create_Utwory_sql="""
    CREATE TABLE IF NOT EXISTS Utwory(
    id integer PRIMARY KEY,
    wykonwca_id integer NOT NULL,
    tytuł text NOT NULL,
    odtworzenia integer,
    FOREIGN KEY (wykonawca_id) REFERENCES Wykonawcy(id)
    );""" 
    
    db_file='utwory.db'

    conn = create_connection(db_file)   
    if conn is not None:
       execute_sql(conn, create_Wykonawcy_sql)
       execute_sql(conn, create_Utwory_sql)
       conn.close()

# ex_03.py
import sqlite3

def create_connection(db_file):
    conn = None
    try:
       conn = sqlite3.connect(db_file)
       return conn
    except sqlite3.Error as e:
       print(e)
    return conn

def add_wykon(conn, wykon):
    sql='''
    INSERT INTO Wykonawcy (wykonawca) VALUES (?)'''
    cur = conn.cursor()
    cur.execute(sql, wykon)
    conn.commit()
    return cur.lastrowid

def add_piosenka(conn, piosenka):
    sql='''
    INSERT INTO Utwory (tytuł, odtworzenia) VALUES (?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, piosenka)
    conn.commit()
    return cur.lastrowid

if __name__ == "__main__":
    conn = create_connection("utwory.db")
    wykon = ("Guano Apes")
    wy_id = add_wykon(conn, wykon)

    piosenka = (
       wy_id,
       "Fly high",
       "18" )

    piosenka_id = add_piosenka (conn, piosenka)
 
    print(wy_id, piosenka_id)
    conn.commit()




#SELECT tytuł, odtworzenia FROM Utwory'
#SELECT * FROM Utwory WHERE tytuł = 'My Way'
#SELECT tytuł, odtworzenia FROM Utwory ORDER BY tytuł

#DELETE FROM Utwory WHERE odtworzenia < 100'
#DELETE FROM Utwory WHERE tytuł = 'My Way'
#UPDATE Utwory SET odtworzenia = 16 WHERE tytuł = 'My Way'
