#!/usr/bin/python

import os
import sys
import normalizer
from datetime import datetime
from math import hypot
import sqlite3 as lite

def print_data(db, temperature, distance):
  with db:
    db.row_factory = lite.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Weather ORDER BY timestamp ASC")

    while True:
      row = cursor.fetchone()
      if row is None:
          break

      timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
      location = [row['location_x'], row['location_y']]

      datum = normalizer.Datum(
        row['observatory'],
        timestamp,
        location,
        row['temperature'],
        True
      )
      print datum.localized_string(temperature, distance)

#TODO fetchmany, actually write a custom aggregator for this
def compute_distance(db):
  dist = 0
  with db:
    cursor = db.cursor()
    cursor.execute("SELECT location_x, location_y FROM Weather ORDER BY timestamp ASC")

    row = cursor.fetchone()
    if row is None:
      return dist
    prev_x = row[0]
    prev_y = row[1]

    while True:
      row = cursor.fetchone()
      if row is None:
        break

      x_delta = prev_x - row[0]
      y_delta = prev_y - row[1]
      dist += hypot(x_delta, y_delta)

      prev_x = row[0]
      prev_y = row[1]
  return dist



if __name__ == "__main__":
  if len(sys.argv) < 3:
    print """
      Please specify the units for <temperature> and <distance> as arguments.
      available options for <temperature> are:
        C (CELSIUS), F (FAHRENHEIT), K (KELVIN),
      available options for <distance> are:
        M (METER), KM (KILIMETER), Mi (Mile)

      eg:
        ./print_data.py C Mi
    """

  else:
    temperature = sys.argv[1]
    distance = sys.argv[2]
    db = lite.connect('test.db')
    print_data(db, temperature, distance)
