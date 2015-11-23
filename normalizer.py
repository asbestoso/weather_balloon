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

# converts temperature in specified unit to kelvin
def standardize_temperature(value, unit):
  if unit is CELSIUS:
    return value + 273.15
  elif unit is FAHRENHEIT:
    return (value + 459.67) * (5.0/9)
  return value

# converts temperature from kelvin to specified unit
def localize_temperature(value, unit):
  if unit is CELSIUS:
    return value - 273.15
  elif unit is FAHRENHEIT:
    return value * (9.0/5) - 459.67
  return value

# converts distance from specified unit to meters
def standardize_distance(value, unit):
  if unit is KM:
    return value / 1000
  elif unit is MILE:
    return value / 0.00062137
  return value

# converts distance from meters specified unit
def localize_distance(value, unit):
  if unit is KM:
    return value * 1000
  elif unit is MILE:
    return value * 0.000652137
  return value

class Datum:
  def __init__(self, observatory, timestamp, location, temperature, normalized=False):
    self.observatory = observatory
    self.timestamp = timestamp
    self.location_x = int(location[0])
    self.location_y = int(location[1])
    self.temperature = int(temperature)

    # default local units to kelvin and km unless we know the observatory's local units
    if self.observatory in OBSERVATORY_UNITS:
      self.local_temperature_unit = OBSERVATORY_UNITS[self.observatory][0]
      self.local_distance_unit = OBSERVATORY_UNITS[self.observatory][1]
    else:
      self.local_temperature_unit = KELVIN
      self.local_distance_unit = KM

    # normalize data to kelvin and km
    if not normalized:
      self.temperature = standardize_temperature(self.temperature, self.local_temperature_unit)
      self.location_x = standardize_distance(self.location_x, self.local_distance_unit)
      self.location_y = standardize_distance(self.location_y, self.local_distance_unit)

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
