#! /usr/bin/python

# Standard library imports
import os
import json
import pdb
import csv
from math import radians, cos, sin, asin, sqrt

DIR = os.path.dirname(os.path.abspath(__file__))

station_coords = {
    'South DeKalb': [33.6906, -84.2731],
    'Confederate Ave': [33.7206, -84.3578],
    'Gwinnett Tech': [33.9636, -84.0664],
    'Yorkville': [33.9283, -85.0453],
    'Newnan': [33.4039, -84.7461],
    'McDonough': [33.4347, -84.1617]
}

grid_centers = [
    [34.0708, -84.6071],
    [34.0708, -84.3379],
    [34.0708, -84.0797],

    [33.8514, -84.6071],
    [33.8514, -84.3379],
    [33.8514, -84.0797],

    [33.60203, -84.6071],
    [33.60203, -84.3379],
    [33.60203, -84.0797]
]

#----------------------
# Define helper functions
#----------------------
def haversine(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points
    """
    # convert decimal degrees to radians
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    # haversine formula
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km
#----------------------
# End helper functions
#----------------------

def get_readings(fpath=os.path.join(DIR, 'atlanta_hourly_14.csv')):
    """
    Create a json file with intensity of air pollution for each grid in
    the city of Atlanta
    """
    reader = csv.DictReader(open(fpath, 'r'))

    readings = []
    for hour in reader: # Each row corresponds to an hourly reading
        grid = []
        for cell in grid_centers:
            station_dists = []

            # Calculate distance to each station
            for name in station_coords:
                # Not all stations report values for every hour
                if hour[name] == '':
                    continue

                args = {
                    'lat1': cell[0],
                    'lng1': cell[1],
                    'lat2': station_coords[name][0],
                    'lng2': station_coords[name][1]
                }
                station_dists.append([name, haversine(**args)])

            # Once all the station dists have been calculated,
            # sort in place
            station_dists.sort(key=lambda x: x[1])
            
            # Find the three closest stations and use inverse distance weighting to 
            # calculate an average reading for PM2.5 (pollution). IDW is a basic
            # algorithm for spatial interpolation https://www.e-education.psu.edu/geog486/node/1877
            numerator = [float(hour[name]) / dist**2 for name, dist in station_dists[-3:]]
            denominator = [1 / dist**2 for name, dist in station_dists[-3:]]

            try:
                avg_reading = sum(numerator) / sum(denominator)
            except:
                pdb.set_trace()

            grid.append(avg_reading)

        time = '{} {}'.format(hour['Date (LST)'], hour['Time (LST)'])
        readings.append({'time': time, 'grid': grid})

    # Write the readings to a JSON file
    with open('aq_readings.json', 'wb') as f:
        f.write(json.dumps(readings, indent=4))

if __name__ == '__main__':
    get_readings()

