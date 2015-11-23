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

      # python read lines lazily
      for line in f:
        try:
          datum = normalizer.Datum(*parseLine(line))
          insertDatum(datum, cursor)
        except:
          # TODO better error handling / parsing corrupted data
          pass

def parseLine(line):
  data = line.split('|')
  time = timestamp.strptime(data.pop(0), '%Y-%m-%dT%H:%M')
  location = data.pop(0).split(',')
  temperature = data.pop(0)
  observatory = data.pop(0)
  return [time, location, temperature, observatory]

def insertDatum(datum):
  # if len(DB_WRITE_BUFFER) < BUFFER_SIZE:
  #   DB_WRITE_BUFFER.append()


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Please provide the <input path> as an argument."
  else:
    filename = sys.argv[1]
    db = lite.connect('test.db')
    consume(filename, db)
