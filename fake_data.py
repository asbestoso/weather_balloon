#!/usr/bin/python
import os
import sys
import random
import normalizer
from datetime import datetime, timedelta

#seconds
TIME_DELTA_LOWER = 5
TIME_DELTA_UPPER = 300
#meters
MAX_X = MAX_Y = 10 * 1000 * 1000
TRAVEL_DELTA_LOWER = -50
TRAVEL_DELTA_UPPER = 50
#kelvin
TEMP_LOWER = 200
TEMP_UPPER = 350
TEMP_DELTA_LOWER = -5
TEMP_DELTA_UPPER = 5

CHANGE_OBSERVATORY_CHANCE = 0.05
OBSERVATORIES = normalizer.OBSERVATORY_UNITS.keys()

def create_lines(lines):
  timestamp = datetime.utcnow()
  temp = (TEMP_UPPER + TEMP_LOWER) / 2
  observatory = OBSERVATORIES[0]
  location = [0,0]

  for i in range(lines):
    time_delta = random.randrange(TIME_DELTA_LOWER, TIME_DELTA_UPPER)
    temp_delta = random.randrange(TEMP_DELTA_LOWER, TEMP_DELTA_UPPER)
    x_delta = random.randrange(TRAVEL_DELTA_LOWER, TRAVEL_DELTA_UPPER)
    y_delta = random.randrange(TRAVEL_DELTA_LOWER, TRAVEL_DELTA_UPPER)

    timestamp -= timedelta(seconds=time_delta)

    temp += temp_delta
    if temp < TEMP_LOWER:
      temp = TEMP_LOWER

    location[0] += x_delta
    if location[0] < 0:
      location[0] += MAX_X
    location[1] += y_delta
    if location[1] < 0:
      location[1] += MAX_Y

    if random.randrange(0, 100) < (CHANGE_OBSERVATORY_CHANCE * 100):
      observatory = OBSERVATORIES[random.randrange(0, len(OBSERVATORIES))]

    datum = normalizer.Datum(observatory, timestamp, location, temp, True)
    yield datum.localized_string()


def generate_data(out, lines):
  data = create_lines(lines)

  mode = 'a' if os.path.exists(out) else 'w+'
  with open(out, mode) as f:
    for line in data:
      # python will buffer these writes
      f.write(line + '\n')

def scramble_file(out):
  pass

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "Please provide the <output path> and <number of lines> as parameters"
  else:

    filename = sys.argv[1]
    lines = int(sys.argv[2])

    generate_data(filename, lines)
    scramble_file(filename)
