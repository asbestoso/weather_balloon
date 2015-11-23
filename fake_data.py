#!/usr/bin/python
import os
import sys
import random
import normalizer
from datetime import datetime, timedelta

#seconds
TIME_DELTA_LOWER = 5
TIME_DELTA_UPPER = 30
#meters
MAX_X = MAX_Y = 10 * 1000 * 1000
TRAVEL_DELTA_LOWER = -200
TRAVEL_DELTA_UPPER = 600
#kelvin
TEMP_LOWER = 200
TEMP_UPPER = 350
TEMP_DELTA_LOWER = -5
TEMP_DELTA_UPPER = 5

CHANGE_OBSERVATORY_CHANCE = 0.05
OBSERVATORIES = normalizer.OBSERVATORY_UNITS.keys()

def createLines(lines):
  timestamp = datetime.utcnow()
  temp = (TEMP_UPPER + TEMP_LOWER) / 2
  observatory = OBSERVATORIES[0]
  location = [0,0]

  for i in range(lines):
    # random simulate the movement of the balloon, adjustable via constants
    time_delta = random.randrange(TIME_DELTA_LOWER, TIME_DELTA_UPPER)
    temp_delta = random.randrange(TEMP_DELTA_LOWER, TEMP_DELTA_UPPER)
    x_delta = random.randrange(TRAVEL_DELTA_LOWER, TRAVEL_DELTA_UPPER)
    y_delta = random.randrange(TRAVEL_DELTA_LOWER, TRAVEL_DELTA_UPPER)

    timestamp -= timedelta(seconds=time_delta)

    new_temp = temp + temp_delta
    if new_temp > TEMP_LOWER and new_temp < TEMP_UPPER:
      temp = new_temp

    location[0] += x_delta
    if location[0] < 0: #wrap around globe
      location[0] += MAX_X
    location[1] += y_delta
    if location[1] < 0:
      location[1] += MAX_Y

    if random.randrange(0, 100) < (CHANGE_OBSERVATORY_CHANCE * 100):
      observatory = OBSERVATORIES[random.randrange(0, len(OBSERVATORIES))]

    datum = normalizer.Datum(observatory, timestamp, location, temp, True)
    yield datum.localized_string()


def generateData(out, lines):
  data = createLines(lines)

  mode = 'a' if os.path.exists(out) else 'w+'
  with open(out, mode) as f:
    for line in data:
      # python will buffer these writes
      f.write(line + '\n')

def scrambleFile(out):
  """TODO
  - read file from start to end
  - generate a random number and jump that many lines
  - swap current line with previous line
  - use random number for chance of garbling the data on the line
  """
  pass

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "Please provide the <output path> and <number of lines> as parameters"
  else:
    filename = sys.argv[1]
    lines = int(sys.argv[2])

    generateData(filename, lines)
    scrambleFile(filename)
