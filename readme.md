# googleizer

Yet another python library for the google api's

Stating with the Google MAPs api, more to come soon.

## Example

```
>>> import googleizer
>>> g = googleizer.Googleizer()
>>> g.maps.geocode.forward('200 Crown St., Darlinghurst, 2010, Australia')
[{'geometry': {'location': {'lat': -33.8769333, 'lng': 151.215796}, 'viewport': {'northeast': {'lat': -33.87558431970849, 'lng': 151.2171449802915}, 'southwest': {'lat': -33.87828228029149, 'lng': 151.2144470197085}}, 'location_type': 'ROOFTOP'}, 'address_components': [{'long_name': '200', 'types': ['street_number'], 'short_name': '200'}, {'long_name': 'Crown Street', 'types': ['route'], 'short_name': 'Crown St'}, {'long_name': 'East Sydney', 'types': ['locality', 'political'], 'short_name': 'East Sydney'}, {'long_name': 'New South Wales', 'types': ['administrative_area_level_1', 'political'], 'short_name': 'NSW'}, {'long_name': 'Australia', 'types': ['country', 'political'], 'short_name': 'AU'}, {'long_name': '2010', 'types': ['postal_code'], 'short_name': '2010'}], 'formatted_address': '200 Crown Street, East Sydney NSW 2010, Australia', 'types': ['street_address']}]

```
