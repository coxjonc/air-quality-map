Mapping the effect of November wildfires on air quality in Atlanta
---

This project uses the [AirNow api](https://docs.airnowapi.org/HistoricalObservationsByLatLon/docs) (signup required) to generate a 9x9 tile grid that can be superimposed over Atlanta and color-coded to show air quality in different areas of the city. Could be edited for higher resolution, but the user should bear in mind that AirNow has some pretty strict rate limits.

Installation
---
Install node dependencies

`npm install`

Run dev server

`npm run serve-dev`

Usage
---
The TKTK python script automatically pings the AirNow API for a set of points surrounding Atlanta, downloads the CSV files with information about particulate levels and ozone, and generates a JSON file with cleaned data that is ready to be consumed by the app. 

If you want to change the resolution of the map, focus just on particulate emissions, or make any other changes, see the [AirNow docs](https://docs.airnowapi.org/HistoricalObservationsByLatLon/docs).


