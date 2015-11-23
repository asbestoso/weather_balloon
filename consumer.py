#!/usr/bin/python
import os
import sys
import normalizer
from datetime import datetime

# Using sql for its simplicity; a timeseries/columnar database would work well here.
try:
  import sqlite3 as lite
except ImportError:
  print 'Please install/make availble sqlite3'

# DB_WRITE_BUFFER = []
# BUFFER_SIZE = 1000 # number of rows to batch

def consume(filename, db):
  with open(filename, 'r') as f:
    with db:
      cursor = db.cursor()
      initializeDB(cursor)
      # python read lines lazily
      for line in f:
        try:
          datum = normalizer.Datum(**parseLine(line))
          insertDatum(datum, cursor)
        except:
          # TODO better error handling / parsing corrupted data
          pass

def parseLine(line):
  data = line.strip().split('|')
  params = {
    'timestamp': datetime.strptime(data.pop(0), '%Y-%m-%dT%H:%M'),
    'location': data.pop(0).split(','),
    'temperature': data.pop(0),
    'observatory': data.pop(0)
  }
  return params


# TODO clean up this mess
def insertDatum(datum, cursor):
  # if len(DB_WRITE_BUFFER) < BUFFER_SIZE:
  #   DB_WRITE_BUFFER.append()
  data = datum.to_hash()
  command = """
    INSERT INTO
      Weather(
        timestamp, location_x, location_y, temperature, observatory)
      VALUES(
        '{timestamp}',{location_x},{location_y},{temperature},'{observatory}');
    """.format(**data)
  cursor.execute(command)

def initializeDB(cursor):
  cursor.execute("DROP TABLE IF EXISTS Weather;")
  cursor.execute("""
    CREATE TABLE Weather(
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      timestamp DATETIME,
      location_x INTEGER,
      location_y INTEGER,
      temperature INTEGER,
      observatory VARCHAR(64)
    );
  """)
  cursor.execute("CREATE INDEX timestamp_index on Weather (timestamp);")
  cursor.execute("CREATE INDEX observatory_index on Weather (observatory);")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Please provide the <input path> as an argument."
  else:
    filename = sys.argv[1]
    db = lite.connect('test.db')
    consume(filename, db)
