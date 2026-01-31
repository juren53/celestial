#!/usr/bin/env python3
# moon.py
#----------------------Ver 0.1------------------------------
"""

Moon.py is a Python script that calculates and displays lunar information, 
including the current moon phase, rise time, set time, and transit time 
for the Kansas City, Missouri location.

Wed 12 Mar 2025 05:23:01 PM CDT 
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

