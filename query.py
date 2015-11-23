#!/usr/bin/python

import collections
import sqlite3 as lite
from math import hypot
from optparse import OptionParser

QUERY_MAP = {
  'max_temp':     ('max(temperature)',                 'Maximum temperature (kelvin)'),
  'min_temp':     ('min(temperature)',                 'Minimum temperature (kelvin)'),
  'avg_temp':     ('avg(temperature)',                 'Average temperature (kelvin)'),
  'distance':     ('distance(location_x, location_y)', 'Distance travelled (Km)'),
  'observations': ('observations(observatory)',        'Records at each observatory'),
}

class AggregateDistance:
  def __init__(self):
    # python will convert this to long automatically
    self.distance = 0
    self.prev_x = None
    self.prev_y = None

  def step(self, x, y):
    if self.prev_x is None or self.prev_y is None:
      self.prev_x = x
      self.prev_y = y
    else:
      delta_x = self.prev_x - x
      delta_y = self.prev_y - y
      self.distance += hypot(delta_x, delta_y)

  # return the distance in Km
  def finalize(self):
    return int(self.distance/1000)

class AggregateObservations:
  def __init__(self):
    self.observations = collections.defaultdict(int)

  def __str__(self):
    out = ""
    for key, val in self.observations.iteritems():
      out += "\n\t{}: {}".format(key, val)
    return out

  def step(self, observatory):
    self.observations[observatory] += 1

  def finalize(self):
    return self.__str__()

# run the query_string
def executeQuery(datafile, query_string):
  connection = lite.connect(datafile)
  with connection:
    connection.create_aggregate("distance", 2, AggregateDistance)
    connection.create_aggregate("observations", 1, AggregateObservations)

    cursor = connection.cursor()
    cursor.execute(query_string)
    return list(cursor.fetchone())

# format and print results
def outputQueryResults(options, results):
  for query, selected in options.iteritems():
    if selected:
      print "{}: {}".format(QUERY_MAP[query][1], results.pop(0))

# parse options and create the sql query
def generateQuery(options):
  queries = []
  for query, selected in options.iteritems():
    if selected:
      queries.append(QUERY_MAP[query][0])

  if not queries:
    return None
  queries = ','.join(queries)
  query_string = "SELECT {} FROM WEATHER".format(queries)
  if options['distance']:
    query_string += ' ORDER BY timestamp ASC'
  return query_string



def main():
  parser = OptionParser(usage="usage: %prog [options] datafile")
  # could do some metaprogramming here with QUERY_MAP
  parser.add_option("--max",
                    action="store_true",
                    dest="max_temp",
                    default=False,
                    help="outputs the maximum temperature in Kelvin")
  parser.add_option("--min",
                    action="store_true",
                    dest="min_temp",
                    default=False,
                    help="outputs the minimum temperature in Kelvin")
  parser.add_option("--mean",
                    action="store_true",
                    dest="avg_temp",
                    default=False,
                    help="outputs the average temperature in Kelvin")
  parser.add_option("--observations",
                    action="store_true",
                    dest="observations",
                    default=False,
                    help="outputs the number of observations from each observatory")
  parser.add_option("--distance",
                    action="store_true",
                    dest="distance",
                    default=False,
                    help="outputs the total distance travelled in Kilometers")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.error("wrong number of arguments, use -h for help")

  datafile = args[0]
  options = options.__dict__
  query_string = generateQuery(options)
  if not query_string:
    parser.error("no queries specified, use -h for available query options")

  result = executeQuery(datafile, query_string)
  outputQueryResults(options, result)

if __name__ == "__main__":
  main()
