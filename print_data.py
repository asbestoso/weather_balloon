#!/usr/bin/python

import os
import sys
import normalizer
from datetime import datetime
import sqlite3 as lite

def print_data(datapath, temperature, distance):
  db = lite.connect(datapath)
  with db:
    db.row_factory = lite.Row
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Weather ORDER BY timestamp ASC")

    while True:
      # might get a performance improvement by fetching in batches with fetchmany
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

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print """
      Please specify the <datafile> and the units for <temperature> and <distance> as arguments.
      available options for <temperature> are:
        {0} (CELSIUS), {1} (FAHRENHEIT), {2} (KELVIN),
      available options for <distance> are:
        {3} (METER), {4} (KILOMETER), {5} (Mile)

      eg:
        ./print_data.py data.db {0} {5}
    """.format(
      normalizer.CELSIUS,
      normalizer.FAHRENHEIT,
      normalizer.KELVIN,
      normalizer.METER,
      normalizer.KM,
      normalizer.MILE)
  else:
    datapath = sys.argv[1]
    temperature = sys.argv[2]
    distance = sys.argv[3]

    print_data(datapath, temperature, distance)
