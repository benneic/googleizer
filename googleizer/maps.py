import logging; log = logging.getLogger(__name__)
try:
  import simplejson as json
except ImportError:
  import json

from __init__ import Endpoint, Requester

__author__ = 'beichhor'

API_ENDPOINT = 'http://maps.googleapis.com/maps/api'

class Maps(object):
  """Google Maps V3 Handler"""

  def __init__(self, api_key=None, secret_key=None):
    """Sets up the api object"""
    # set up base requester
    self._base_requester = Requester(API_ENDPOINT, api_key)
    # add each endpoint
    self.geocode = self.Geocode(self._base_requester)

  class Geocode(Endpoint):
    """The Google Geocoding API"""
    endpoint = 'geocode'

    def forward(self, address, sensor=False, bounds=None, region=None, language=None):
      params = {
        'address' : address,
        'sensor' : str(sensor).lower()
      }
      if bounds:
        params['bounds'] = bounds
      if region:
        params['region'] = region
      if language:
        params['language'] = language
      return self.GET(params=params)

    def reverse(self, latitude, longitude, sensor=False, bounds=None, region=None, language=None):
      params = {
        'latlng' : '%s,%s' % (latitude, longitude),
        'sensor' : str(sensor).lower()
      }
      if bounds:
        params['bounds'] = bounds
      if region:
        params['region'] = region
      if language:
        params['language'] = language
      return self.GET(params=params)


  class Places(Endpoint):
    """ The Google Places API
    """
    endpoint = 'place'

    def search(self, latitude, longitude, radius, sensor=False, keyword=None, language=None, name=None, types=None):
      MAX_RADIUS = 50000
      params = {
        'location' : '%s,%s' % (latitude, longitude),
        'radius' : radius if radius < MAX_RADIUS else MAX_RADIUS,
        'sensor' : str(sensor).lower()
      }
      if keyword:
        params['keyword'] = keyword
      if language:
        params['language'] = language
      if name:
        params['name'] = name
      if types:
        params['types'] = types
      return self.GET('search', params)

    def details(self, reference, sensor=False, language=None):
      params = {
        'reference' : reference,
        'sensor' : str(sensor).lower()
      }
      if language:
        params['language'] = language
      return self.GET('search', params)

