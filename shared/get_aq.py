#! /usr/bin/python

# Standard library imports
from os.path import dirname, abspath, join
import math
import json
import time
import pdb
import csv

# Third party imports
from haversine import haversine # Used to calculate  the dist between two lat long points
import numpy as np
from scipy import interpolate

DIR = dirname(abspath(__file__))
OUTFILE = join(dirname(DIR), 'public', 'aq_readings.json')

station_coords = {
    'South DeKalb': [33.6906, -84.2731],
    'Confederate Ave': [33.7206, -84.3578],
    'Gwinnett Tech': [33.9636, -84.0664],
    'Yorkville': [33.9283, -85.0453],
    'Newnan': [33.4039, -84.7461],
    'McDonough': [33.4347, -84.1617]
}

# The number of minutes of latitude and longitude that the grid will span
dist = 0.58

lat_start = 33.5447
lng_start = -84.6394
num_squares = 30
side_length = dist / num_squares # Length of a grid side in degrees latitude. Very small number

# Create a 30x30 grid. A better implementation would be to use numpy
grid_centers = []
for i in range(num_squares):
    for j in range(num_squares):
        dlat = side_length * i + (.5 * side_length)
        dlng = side_length * j + (.5 * side_length)

        lat = lat_start + dlat
        lng = lng_start + dlng

        grid_centers.append([math.ceil(lat*10000)/10000, math.ceil(lng*10000)/10000])

def get_readings(outfile=OUTFILE, fpath=join(DIR, 'atlanta_hourly_14.csv')):
    """
    Create a json file with intensity of air pollution for each grid in
    the city of Atlanta
    """
    reader = csv.DictReader(open(fpath, 'r'))

    readings = []
    for hour in reader: # Each row corresponds to an hourly reading
        grid = []
        for i, cell in enumerate(grid_centers):
            station_dists = []

            # Calculate distance to each station
            for name in station_coords:
                # Not all stations report values for every hour
                if hour[name] == '':
                    continue

                grid_loc = (cell[0], cell[1])
                station_loc = (station_coords[name][0], station_coords[name][1])

                station_dists.append([name, haversine(grid_loc, station_loc, miles=True)])

            # Once all the station dists have been calculated, sort in place
            station_dists.sort(key=lambda x: x[1])

            # A naive model for calculating air quality at a given point. Will switch
            # for inverse distance weighting or some other form of spatial interpolation
            # when I get the chance.
            nearest_neighbor = station_dists[0]
            next_neighbor = station_dists[1]
            if nearest_neighbor[1] < 10:
                if next_neighbor[1] < 30:
                    sum_ = float(hour[next_neighbor[0]]) + float(hour[nearest_neighbor[0]])
                    avg_reading = sum_ / 2
                else:
                    float(hour[nearest_neighbor[0]])
            else:
                sum_ = float(hour[next_neighbor[0]]) + float(hour[nearest_neighbor[0]])
                avg_reading = sum_ / 2

            grid.append(avg_reading)

        day = time.strptime(hour['Date (LST)'] + ' ' + hour['Time (LST)'], '%m/%d/%y %H:00')

        # Break grid into a list of rows
        new_grid = []
        for i in range(30):
            start = (i*30)
            new_grid.append(grid[start:start+30])

        day = time.strftime('%A, %b %d %-I:00%p', day)
        readings.append({'time': day, 'grid': new_grid})

    # Write the readings to a JSON file
    with open(outfile, 'wb') as f:
        f.write(json.dumps(readings, indent=4))

if __name__ == '__main__':
    get_readings()

