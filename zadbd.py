import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine('sqlite:///zadbd.db')
from sqlalchemy import Table, Column, Integer, String, Date, Float, MetaData
print(engine.driver)

#clean_measure: station,date,precip,tobs
#clean_stations: station,latitude,longitude,elevation,name,country,state

meta = MetaData()
clean_measure = Table (
    'clean_measure', meta,
    Column('id', Integer, primary_key=True),
    Column('station', String),
    Column('date', Date),
    Column('precip', Float),
    Column('tobs', Integer),
)
clean_station = Table (
    'clean_station', meta,
    Column('id', Integer, primary_key=True),
    Column('station', String),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('elevation', Float),
    Column('name', String),
    Column('country', String),
    Column('state', String),
)

meta.create_all(engine)
print(engine.table_names())

ins = clean_measure.insert()
conn = engine.connect()
result = conn.execute(ins)
#conn.execute(ins, [
#   {'id': '1', 'station': 'ssss', 'date':'2022-10-02', 'precip':'0.65', 'tobs':'987'},
#])