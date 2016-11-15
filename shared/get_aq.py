#! /usr/bin/python

# Standard library imports
import os
import shutil
import cgi
import pdb

# Third party imports
import requests

# Constants
API_KEY = os.environ.get('AQ_KEY')
DIST = 8 # The range of the air quality average

# A three-by-three grid of latitude and longitude points, each the center of a
# grid cell roughly 15 mi sq
latlngs = [
    [34.0708, -84.6071],
    [34.0708, -84.3379],
    [34.0708, -84.0797],

    [33.8514, -84.6071],
    [33.8514, -84.3379],
    [33.8514, -84.0797],

    [33.60203, -84.6071],
    [33.60203, -84.3379],
    [33.60203, -84.0797],
]

def get_aq(directory='/tmp/'):
    url_template = 'http://www.airnowapi.org/aq/observation/latLong/historical/?format=application/xml&latitude={lat}&longitude={lng}&date={date}&distance={dist}&API_KEY={key}'
    date = '2016-11-{}T00-0000' # The API only allows you to make a request for readings at midnight

    for coords in latlngs:
        # Loop through a list of dates to get air quality history
        for day in [12, 13, 14, 15]:
            context = {
                'lat': coords[0],
                'lng': coords[1],
                'date': date.format(day),
                'dist': 25,
                'key': API_KEY
            }
            url = url_template.format(**context)

            res = requests.get(url)

            if res.status_code != 200:
                raise ValueError('Failed to download')

            params = cgi.parse_header(
                res.headers.get('Content-Disposition', ''))[-1]

            pdb.set_trace()

            # The API returns a CSV so we need to write it to a file
            fname = params['filename'] # Should be Output.csv but we don't want to take any chances
            abs_path = os.path.join(directory, fname)
            pdb.set_trace()
            with open(abs_path, 'wb') as f:
                res.raw.decode_content = True
                shutil.copyfileobj(res.raw, f)

            pdb.set_trace()

if __name__ == "__main__":
    get_aq()

