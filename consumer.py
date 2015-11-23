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

BUFFER_SIZE = 30000 # number of rows to batch

# this could go into its own file
class BufferedWrites:
  def __init__(self, cursor, buffer_size=BUFFER_SIZE):
    self.cursor = cursor
    self.buffer_size = buffer_size
    self.buffer = []

  def insertDatum(self, datum):
    if len(self.buffer) >= self.buffer_size:
      self.dumpBuffer()
    buffer_row = (
      datum.timestamp,
      datum.location_x,
      datum.location_y,
      datum.temperature,
      datum.observatory)
    self.buffer.append(buffer_row)

  def dumpBuffer(self):
    command = """
      INSERT INTO
        Weather(
          timestamp, location_x, location_y, temperature, observatory)
        VALUES(?, ?, ?, ?, ?);"""
    self.cursor.executemany(command, self.buffer)
    self.buffer = []

def parseLine(line):
  data = line.strip().split('|')
  params = {
    'timestamp': datetime.strptime(data.pop(0), '%Y-%m-%dT%H:%M'),
    'location': data.pop(0).split(','),
    'temperature': data.pop(0),
    'observatory': data.pop(0)
  }
  return params

def consume(filename, cursor):
  with open(filename, 'r') as f:
    with db:
      cursor = db.cursor()
      initializeDB(cursor)
      db_buffer = BufferedWrites(cursor)
      # python read lines lazily
      for line in f:
        try:
          datum = normalizer.Datum(**parseLine(line))
          db_buffer.insertDatum(datum)
        except:
          # TODO more specific error handling / parsing corrupted data
          pass
      db_buffer.dumpBuffer()

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
  if len(sys.argv) < 3:
    print "Please provide the <input path>, <datastore path> as an argument."
    # TODO print "Optionally, pass 'keep' as the third argument to append to datastore."
  else:
    filename = sys.argv[1]
    db = lite.connect(sys.argv[2])

    consume(filename, db)


### TODO: try just using sql queries and custom aggregators if they are fast enough,
### if too slow, then move this logic into BufferedWrites
# AGGREGATE = {
#   'entries': 0,
#   'mean_temp': 0,
#   'total_dist': 0,
#   'observatories': {},
# }

# def aggregate(datum):
#   global AGGREGATE
#   AGGREGATE['mean_temp'] = (AGGREGATE['mean_temp'] * AGGREGATE['entries']) / (AGGREGATE['entries']+1)
#   AGGREGATE['entries'] += 1

#   if not 'min_temp' in AGGREGATE or AGGREGATE['min_temp'] > datum.temperature:
#     AGGREGATE['min_temp'] = datum.temperature
#   if not 'max_temp' in AGGREGATE or AGGREGATE['max_temp'] < datum.temperature:
#     AGGREGATE['max_temp'] = datum.temperature

#   observatories = AGGREGATE['observatories']
#   observatories.setdefault(datum.observatory, 0)
#   observatories[datum.observatory] += 1

#   print AGGREGATE

# def storeAggregate():
#   print AGGREGATE
