import sqlite3
from sqlite3 import Error
import sqlalchemy
from sqlalchemy import create_engine

db_file = "database.db"

#DEFINICJA NOWEJ TABELI
#aby obaczyć wykonywany kod SQL należy dodać warunek echo=True
#engine = create_engine('sqlite:///database.db', echo=True)
   
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')

meta = MetaData()
students = Table(
   'students', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String),
   Column('lastname', String),
)

meta.create_all(engine)
print(engine.table_names())


