



OBSERVATORIES = ['AU', 'US', 'FR', 'XX']

OBSERVATORY_UNITS = {}

# TODO: make these classes
OBSERVATORY_UNITS['AU'] = {
  'temp_unit': 'celsius'
  'temp_symbol': 'C'
  'localize_temperture': kelvin_to_celsius
  'standardize_temperture': celsius_to_kelvin
  'localize_distance': m_to_km
  'standardize_distance': km_to_m
}
OBSERVATORY_UNITS['US'] = {
  'temp_unit': 'fahrenheit'
  'temp_symbol': 'F'
  'localize_temperture': kelvin_to_fahrenheit
  'standardize_temperture': fahrenheit_to_kelvin
  'localize_distance': m_to_miles
  'standardize_distance': miles_to_m
}
OBSERVATORY_UNITS['FR'] = {
  'temp_unit': 'kelvin'
  'temp_symbol': 'K'
  'localize_temperture': noop
  'standardize_temperture': noop
  'localize_distance': m_to_km
  'standardize_distance': km_to_m
}
OBSERVATORY_UNITS['XX'] = {
  'temp_unit': 'kelvin'
  'temp_symbol': 'K'
  'localize_temperture': kelvin_to_celsius
  'standardize_temperture': celsius_to_kelvin
  'localize_distance': m_to_km
  'standardize_distance': km_to_m
}


def kelvin_to_celsius(kelvin):

def kelvin_to_fahrenheit(kelvin):

def celsius_to_kelvin(celsius):

def fahrenheit_to_kelvin(fahrenheit):


def noop(original):
  return original


class normalizer(Object):

  def __init__(self, observatory, timestamp, location, temperture, normalized=False):
    self.observatory = observatory
    self.timestamp = timestamp
    self.location = location
    self.temperture = temperture
    self.normalized = normalized

    if not self.normalized:
      #normalize

  def normalize_to()





def denormalize(observatory, timestamp, location, temperture):

