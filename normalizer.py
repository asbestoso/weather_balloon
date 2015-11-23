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

def standardize_temperature(value, unit):
  if unit is CELSIUS:
    return value + 273.15
  elif unit is FAHRENHEIT:
    return (value + 459.67) * (5.0/9)
  return value

def localize_temperature(value, unit):
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
  local_temperature_unit = KELVIN
  local_distance_unit = KM

  def __init__(self, observatory, timestamp, location, temperature, normalized=False):
    self.observatory = observatory
    self.timestamp = timestamp
    self.location_x = int(location[0])
    self.location_y = int(location[1])
    self.temperature = int(temperature)

    if self.observatory in OBSERVATORY_UNITS:
      self.local_temperature_unit = OBSERVATORY_UNITS[self.observatory][0]
      self.local_distance_unit = OBSERVATORY_UNITS[self.observatory][1]

    if not normalized:
      self.temperature = standardize_temperature(self.temperature, self.local_temperature_unit)
      self.location_x = standardize_distance(self.location_x, self.local_distance_unit)
      self.location_y = standardize_distance(self.location_y, self.local_distance_unit)

  def to_hash(self):
    return {
      'timestamp': self.timestamp,
      'location_x': int(self.location_x),
      'location_y': int(self.location_y),
      'temperature': int(self.temperature),
      'observatory': self.observatory,
    }

  def localized_string(self, temp_unit=None, dist_unit=None):
    temp_unit = self.local_temperature_unit if temp_unit is None else temp_unit
    dist_unit = self.local_distance_unit if dist_unit is None else dist_unit

    data = {
      'timestamp': self.timestamp.strftime('%Y-%m-%dT%H:%M'),
      'x': int(localize_distance(self.location_x, dist_unit)),
      'y': int(localize_distance(self.location_y, dist_unit)),
      'temperature': int(localize_temperature(self.temperature, temp_unit)),
      'observatory': self.observatory,
    }
    return "{timestamp}|{x},{y}|{temperature}|{observatory}".format(**data)
