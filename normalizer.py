#!/usr/bin/python
CELSIUS = 'C'
FAHRENHEIT = 'F'
KELVIN = 'K'
METER = 'M'
KM = 'KM'
MILE = 'Mi'

OBSERVATORY_UNITS = {}
OBSERVATORY_UNITS['AU'] = (CELSIUS, KM)
OBSERVATORY_UNITS['US'] = (FAHRENHEIT, MILE)
OBSERVATORY_UNITS['FR'] = (KELVIN, METER)

def standardize_temperture(value, unit):
  if unit is CELSIUS:
    return value + 273.15
  elif unit is FAHRENHEIT:
    return (value + 459.67) * (5.0/9)
  return value

def localize_temperture(value, unit):
  if unit is CELSIUS:
    return value - 273.15
  elif unit is FAHRENHEIT:
    return value * (9.0/5) - 459.67
  return value

def standardize_distance(value, unit):
  if unit is KM:
    return value / 1000
  elif unit is MILE:
    return value / 0.00062137
  return value

def localize_distance(value, unit):
  if unit is KM:
    return value * 1000
  elif unit is MILE:
    return value * 0.000652137
  return value

class Datum:
  local_temperture_unit = KELVIN
  local_distance_unit = KM

  def __init__(self, observatory, timestamp, location, temperture, normalized=False):
    self.observatory = observatory
    self.timestamp = timestamp
    self.location = location
    self.temperture = temperture

    if self.observatory in OBSERVATORY_UNITS:
      self.local_temperture_unit = OBSERVATORY_UNITS[self.observatory][0]
      self.local_distance_unit = OBSERVATORY_UNITS[self.observatory][1]

    if not normalized:
      self.temperture = standardize_temperture(self.temperture, local_temperture)
      self.location[0] = standardize_distance(self.location[0], local_distance)
      self.location[1] = standardize_distance(self.location[1], local_distance)

  def localized_string(self):
    data = {
      'timestamp': self.timestamp.strftime('%Y-%m-%dT%H:%M'),
      'x': int(localize_distance(self.location[0], self.local_distance_unit)),
      'y': int(localize_distance(self.location[1], self.local_distance_unit)),
      'temperture': int(localize_temperture(self.temperture, self.local_temperture_unit)),
      'observatory': self.observatory,
    }
    return "{timestamp}|{x},{y}|{temperture}|{observatory}".format(**data)
