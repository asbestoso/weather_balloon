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

DB_WRITE_BUFFER = []
BUFFER_SIZE = 1000 # number of rows to batch
AGGREGATE = {
  'entries': 0
  'mean_temp': 0
  'total_dist': 0
  'observatories': {}
}


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
          aggregate(datum)
        except:
          # TODO better error handling / parsing corrupted data
          pass
      dumpBuffer()
      storeAggregrate()

def parseLine(line):
  data = line.strip().split('|')
  params = {
    'timestamp': datetime.strptime(data.pop(0), '%Y-%m-%dT%H:%M'),
    'location': data.pop(0).split(','),
    'temperature': data.pop(0),
    'observatory': data.pop(0)
  }
  return params

def aggregate(datum):
  AGGREGATE['mean_temp'] = (AGGREGATE['mean_temp'] * AGGREGATE['entries']) /
                           (AGGREGATE['entries']+1)
  AGGREGATE['entries'] += 1

  if not 'min_temp' in AGGREGATE or AGGREGATE['min_temp'] > datum.temperature:
    AGGREGATE['min_temp'] = datum.temperature
  if not 'max_temp' in AGGREGATE or AGGREGATE['max_temp'] < datum.temperature:
    AGGREGATE['max_temp'] = datum.temperature

  observatories = AGGREGATE['observatories']
  observatories.setdefault(datum.observatory, 0)
  observatories[datum.observatories] += 1

def storeAggregate():
  pass

def insertDatum(datum, cursor):
  if len(DB_WRITE_BUFFER) >= BUFFER_SIZE:
    dumpBuffer()
  buffer_row = (
    data.timestamp,
    data.location_x,
    data.location_y,
    data.temperature,
    data.observatory)
  DB_WRITE_BUFFER.append(buffer_row)

def dumpBuffer():
  command = """
    INSERT INTO
      Weather(
        timestamp, location_x, location_y, temperature, observatory)
      VALUES(?, ?, ?, ?, ?);"""
  cursor.executemany(command, DB_WRITE_BUFFER)
  DB_WRITE_BUFFER = []

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
