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

class ParseException(Exception):
    pass

def consume(filename, datastore):
  with open(filename, 'r') as f:
    db = lite.connect(datastore)
    with db:
      cursor = db.cursor()
      initializeDB(cursor)
      db_buffer = BufferedWrites(cursor)
      # python read lines lazily
      for line in f:
        try:
          datum = parseLine(line)
          db_buffer.insertDatum(datum)
        except ParseException:
          # throw out bad data
          print 'failed to parse:', line,
      db_buffer.dumpBuffer()

# reads a log line and returns a normalized datum
def parseLine(line):
  try:
    data = line.strip().split('|')
    params = {
      'timestamp': datetime.strptime(data.pop(0), '%Y-%m-%dT%H:%M'),
      'location': data.pop(0).split(','),
      'temperature': data.pop(0),
      'observatory': data.pop(0)
    }
    return normalizer.Datum(**params)
  except:
    raise ParseException

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
    datastore = sys.argv[2]
    consume(filename, datastore)

