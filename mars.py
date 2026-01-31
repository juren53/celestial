#!/usr/bin/env python3
# mars.py
#----------------------Ver 1.0------------------------------
"""

Mars.py is a Python script that calculates and displays Mars information, 
including rise time, set time, transit time, distance from Earth,
apparent magnitude, angular size, and current position (altitude and azimuth)
for the Kansas City, Missouri location.

Created Thu 20 Mar 2025 10:04:39 AM CDT Ver 1.0 Initial version based on moon.py
#  
#-----------------------------------------------------------
"""
import ephem
import datetime
import pytz
import argparse
from datetime import timezone

# Function to convert ephem.Date to datetime with timezone info
def ephem_to_datetime(ephem_date):
    date_tuple = ephem_date.tuple()
    dt = datetime.datetime(date_tuple[0], date_tuple[1], date_tuple[2], 
                           date_tuple[3], date_tuple[4], int(date_tuple[5]))
    return dt.replace(tzinfo=timezone.utc)

# Helper function to convert azimuth in degrees to a compass direction
def get_compass_direction(azimuth):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(azimuth / 22.5) % 16
    return directions[index]

def show_mars_info():
    # Set observer location (latitude, longitude, elevation)
    observer = ephem.Observer()
    observer.lat = '39.0997'  # Kansas City, MO latitude
    observer.lon = '-94.5786'  # Kansas City, MO longitude
    current_time = datetime.datetime.utcnow()  # Store current UTC time
    observer.date = current_time  # PyEphem expects UTC time

    # Mars calculations for current position
    mars = ephem.Mars()
    mars.compute(observer)
    
    # Store current mars position data
    current_alt = mars.alt
    current_az = mars.az

    # Get distance from Earth (in AU and km)
    distance_au = mars.earth_distance
    distance_km = distance_au * 149597870.7  # 1 AU = 149,597,870.7 km

    # Get mars rise, set, and transit times
    mars_rise = observer.next_rising(mars)
    mars_set = observer.next_setting(mars)
    mars_transit = observer.next_transit(mars)  # When mars is at its highest point (crossing the meridian)
    # Convert to CST time zone
    cst = pytz.timezone('America/Chicago')  # CST is America/Chicago in IANA time zone database

    rise_cst = ephem_to_datetime(mars_rise).astimezone(cst)
    set_cst = ephem_to_datetime(mars_set).astimezone(cst)
    transit_cst = ephem_to_datetime(mars_transit).astimezone(cst)

    print(f"Mars distance from Earth: {distance_au:.4f} AU ({distance_km:.0f} km)")
    print(f"Mars apparent magnitude: {mars.mag:.2f}")
    print(f"Mars angular diameter: {mars.size:.2f} arcseconds")
    print(f"Mars rise (CST): {rise_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Mars transit (CST): {transit_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Mars set (CST): {set_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Get mars's current position in the sky
    # Altitude is the elevation above the horizon in degrees (0° at horizon, 90° directly overhead)
    # Azimuth is the compass direction in degrees (0° is North, 90° is East, 180° is South, 270° is West)
    altitude_deg = float(current_alt) * 180 / 3.1415926  # Convert radians to degrees
    azimuth_deg = float(current_az) * 180 / 3.1415926  # Convert radians to degrees

    print(f"Current Mars position above Kansas City:")
    print(f"  Altitude: {altitude_deg:.2f}° ({altitude_deg:.2f} degrees above horizon)")
    print(f"  Azimuth: {azimuth_deg:.2f}° ({get_compass_direction(azimuth_deg)})")

def main():
    # Display current datetime at beginning of program execution
    cst = pytz.timezone('America/Chicago')
    current_time = datetime.datetime.now(cst)
    print(f"mars.py 1.0 {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    parser = argparse.ArgumentParser(
        description="Mars.py - Display Mars information for Kansas City, MO"
    )
    parser.add_argument('-v', '--version', action='store_true', 
                        help='show version information and exit')
    
    args = parser.parse_args()
    
    if args.version:
        print("mars.py - Version 1.0")
        print("Created Thu 20 Mar 2025 10:04:39 AM CDT")
        print("Displays Mars information for Kansas City, MO")
    else:
        show_mars_info()

if __name__ == "__main__":
    main()

