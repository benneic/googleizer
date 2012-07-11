import logging; log = logging.getLogger(__name__)
try:
    import simplejson as json
except ImportError:
    import json
import poster
import time
import urllib
import httplib2
import urlparse
import base64
import hmac
import hashlib

import maps

__author__ = 'beichhor'
__version__ = "3.0.0"

NUM_REQUEST_RETRIES = 3

DEFAULT_OUTPUT = 'json'

class OK: pass
class GoogleizerException(Exception): pass
class InvalidRequest(GoogleizerException): pass
class OverQueryLimit(GoogleizerException): pass
class RequestDenied(GoogleizerException): pass
class ZeroResults(GoogleizerException): pass

error_types = {
    'OK': OK,
    'INVALID_REQUEST': InvalidRequest,
    'OVER_QUERY_LIMIT': OverQueryLimit,
    'REQUEST_DENIED': RequestDenied,
    'ZERO_RESULTS': ZeroResults,
    }

class Googleizer(object):
    """ Google API wrapper
    """
    def __init__(self, api_key=None, secret_key=None):
      self.maps = maps.Maps(api_key=api_key, secret_key=secret_key)


class Requester(object):
    """Api requesting object"""
    def __init__(self, endpoint, api_key=None, secret_key=None, headers=None):
        """Sets up the api object"""
        self.endpoint = endpoint
        self.api_key = api_key
        self.secret_key = secret_key
        self.headers = headers or {}

    def GET(self, path, params={}):
        """GET request that returns processed data"""
        params = self._enrich_params(params)
        url = '{endpoint}{path}?{params}'.format(
            endpoint=self.endpoint ,
            path=path,
            params=urllib.urlencode(params)
        )
        return self._request(url)

    def POST(self, path, params={}):
        """POST request that returns processed data"""
        params = self._enrich_params(params)
        url = '{endpoint}{path}'.format(
            endpoint=self.endpoint ,
            path=path
        )
        return self._request(url, params)

    def _enrich_params(self, params):
        """Enrich the params dict"""
        for key, value in params.items():
          if isinstance(value, unicode):
            params[key] = value.encode("utf-8")
        if self.api_key:
            params['key'] = self.api_key
        return params

    def _request(self, url, data=None):
        """Performs the passed request and returns meaningful data"""
        log.debug(u'{method} url: {url}{data}'.format(
            method='POST' if data else 'GET',
            url=url,
            data=u'* {0}'.format(data) if data else u''))
        return self._request_with_retry(url, data)['results']


    def _request_with_retry(self, url, data=None):
        """Tries to load data from an endpoint using retries"""
        for i in xrange(NUM_REQUEST_RETRIES):
            try:
                return self._process_request_with_httplib2(url, data)
            except GoogleizerException, e:
                # Some errors don't bear repeating
                if e.__class__ in [InvalidRequest, OverQueryLimit, RequestDenied, ZeroResults]: raise
                if (i + 1) == NUM_REQUEST_RETRIES: raise
            time.sleep(1)

    def _process_request_with_httplib2(self, url, data=None):
        """Make the request and handle exception processing"""
        h = httplib2.Http()
        try:
            if data:
                datagen, headers = poster.encode.multipart_encode(data)
                data = ''.join(datagen)
                method = 'POST'
            else:
                headers = self.headers
                method = 'GET'

            if self.secret_key:
                url = self._sign_request(url)

            response, body = h.request(url, method, headers=headers, body=data)
        except httplib2.HttpLib2Error, e:
            log.error(e)
            raise GoogleizerException(u'Error connecting with API')
        data = _json_to_data(body)
        status = data.get('status')
        if status:
            exc = error_types.get(status)
            if exc is OK:
                return data
            elif exc:
                raise exc()
            else:
                log.error(u'Unknown error occured: %s' % body)
                raise GoogleizerException(body)
        else:
            log.error(u'Response format invalid: %s' % body)
            raise GoogleizerException('Invlaid resonse format, got: %s' % body)

    def _sign_request(self, url):
        url_parsed = urlparse.urlparse(url)
        url_to_sign = url_parsed.path + "?" + url_parsed.query
        secret_key = base64.urlsafe_b64decode(self.secret_key)
        signature = hmac.new(secret_key, url_to_sign, hashlib.sha1)
        encoded_signature = base64.urlsafe_b64encode(signature.digest())
        new_url = url_parsed.scheme + "://" + url_parsed.netloc + url_parsed.path + "?" + url_parsed.query + "&signature=" + encoded_signature
        return new_url

    

class Endpoint(object):
    """Generic endpoint class"""
    def __init__(self, requester):
        """Stores the request function for retrieving data"""
        self.requester = requester
        self.endpoint = ''

    def _expanded_path(self, path=None):
        """Gets the expanded path, given this endpoint"""
        return '/{expanded_path}/{output}'.format(
            expanded_path='/'.join(p for p in (self.endpoint, path) if p),
            output=DEFAULT_OUTPUT
        )

    def GET(self, path=None, params={}):
        """Use the requester to get the data"""
        return self.requester.GET(self._expanded_path(path), params)

    def POST(self, path=None, params={}):
        """Use the requester to post the data"""
        return self.requester.POST(self._expanded_path(path), params)



def _json_to_data(s):
    """Convert a response string to data"""
    try:
        return json.loads(s)
    except ValueError, e:
        log.error('Invalid response: {0}'.format(e))
        raise GoogleizerException(e)
