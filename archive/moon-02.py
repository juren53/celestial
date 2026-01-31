#!/usr/bin/env python3
# moon.py
#----------------------Ver 0.2------------------------------
"""

Moon.py is a Python script that calculates and displays lunar information, 
including the current moon phase, rise time, set time, transit time,
and current position (altitude and azimuth) for the Kansas City, Missouri location.

Created Wed 12 Mar 2025 05:23:01 PM CDT  Ver 0.1 Rise, set and transit times for KC location
Updated Thu 20 Mar 2025 03:15:11 AM CDT  Ver 0.2 added position in sky - alt / az
#  
#-----------------------------------------------------------
"""
import ephem
import datetime
import pytz
from datetime import timezone

# Set observer location (latitude, longitude, elevation)
observer = ephem.Observer()
observer.lat = '39.0997'  # Kansas City, MO latitude
observer.lon = '-94.5786'  # Kansas City, MO longitude
observer.date = datetime.datetime.utcnow()  # PyEphem expects UTC time

# Moon calculations
moon = ephem.Moon()
moon.compute(observer)

# Get moon phase (0-1 where 0 is new moon and 0.5 is full moon)
phase = moon.phase / 100.0
# print(f"Moon phase: {phase:.2f}")

# Get moon rise, set, and transit times
moon_rise = observer.next_rising(moon)
moon_set = observer.next_setting(moon)
moon_transit = observer.next_transit(moon)  # When the moon is at its highest point (crossing the meridian)

# Function to convert ephem.Date to datetime with timezone info
def ephem_to_datetime(ephem_date):
    date_tuple = ephem_date.tuple()
    dt = datetime.datetime(date_tuple[0], date_tuple[1], date_tuple[2], 
                           date_tuple[3], date_tuple[4], int(date_tuple[5]))
    return dt.replace(tzinfo=timezone.utc)

# Convert to CST time zone
cst = pytz.timezone('America/Chicago')  # CST is America/Chicago in IANA time zone database

rise_cst = ephem_to_datetime(moon_rise).astimezone(cst)
set_cst = ephem_to_datetime(moon_set).astimezone(cst)
transit_cst = ephem_to_datetime(moon_transit).astimezone(cst)

print(f"Moon phase: {phase:.2f}")
print(f"Moon rise (CST): {rise_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"Moon set (CST): {set_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"Moon transit (CST): {transit_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# Helper function to convert azimuth in degrees to a compass direction
def get_compass_direction(azimuth):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(azimuth / 22.5) % 16
    return directions[index]

# Get moon's current position in the sky
# Altitude is the elevation above the horizon in degrees (0° at horizon, 90° directly overhead)
# Azimuth is the compass direction in degrees (0° is North, 90° is East, 180° is South, 270° is West)
altitude_deg = float(moon.alt) * 180 / 3.1415926  # Convert radians to degrees
azimuth_deg = float(moon.az) * 180 / 3.1415926  # Convert radians to degrees

print(f"Current moon position above Kansas City:")
print(f"  Altitude: {altitude_deg:.2f}° ({altitude_deg:.2f} degrees above horizon)")
print(f"  Azimuth: {azimuth_deg:.2f}° ({get_compass_direction(azimuth_deg)})")
