#!/usr/bin/python

import os
import sys
import normalizer
from datetime import datetime
import sqlite3 as lite

def print_data(db, temperature, distance):
  with db:
    db.row_factory = lite.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Weather ORDER BY timestamp ASC")

    while True:
      row = cursor.fetchone()
      if row == None:
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
