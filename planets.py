#!/usr/bin/env python3
# planets.py
#----------------------Ver 1.1------------------------------
"""

planets.py is a Python script that calculates and displays information about
various celestial bodies in our solar system (Mercury, Venus, Mars, Jupiter, 
Saturn, Uranus, Neptune, Pluto, and the Moon), including rise time, set time, 
transit time, distance from Earth, apparent magnitude, angular size, 
and current position (altitude and azimuth) for the Kansas City, Missouri location.

Created Thu 20 Mar 2025 09:30:00 AM CDT Ver 1.0 Initial version based on moon.py
Updated Fri 03 Oct 20225 01:21;11 AM CDT Ver 1.1 fix -deg Alt to report below horizon
#  
#-----------------------------------------------------------
"""
import ephem
import datetime
import pytz
import argparse
import sys
from datetime import timezone

# Speed of light in km/s
SPEED_OF_LIGHT = 299792.458

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

# Helper function to format distance in km to human-readable format
def format_distance_km(distance_km):
    if distance_km >= 1_000_000_000:
        return f"{distance_km/1_000_000_000:.3f} billion km"
    elif distance_km >= 1_000_000:
        return f"{distance_km/1_000_000:.3f} million km"
    elif distance_km >= 1_000:
        return f"{distance_km/1_000:.3f} thousand km"
    else:
        return f"{distance_km:,.0f} km"

def show_planet_info(planet_name):
    # Set observer location (latitude, longitude, elevation)
    observer = ephem.Observer()
    observer.lat = '39.0997'  # Kansas City, MO latitude
    observer.lon = '-94.5786'  # Kansas City, MO longitude
    current_time = datetime.datetime.utcnow()  # Store current UTC time
    observer.date = current_time  # PyEphem expects UTC time
    
    # Map planet name to PyEphem object
    planet_map = {
        'mercury': ephem.Mercury(),
        'venus': ephem.Venus(),
        'mars': ephem.Mars(),
        'jupiter': ephem.Jupiter(),
        'saturn': ephem.Saturn(),
        'uranus': ephem.Uranus(),
        'neptune': ephem.Neptune(),
        'pluto': ephem.Pluto(),
        'moon': ephem.Moon()
    }
    
    # Check if the provided planet name is valid
    planet_name = planet_name.lower()
    if planet_name not in planet_map:
        print(f"Error: '{planet_name}' is not a valid celestial body.")
        print("Valid options are: mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto, moon")
        sys.exit(1)
    
    # Get the celestial body object
    body = planet_map[planet_name]
    body.compute(observer)
    
    # Format the planet name for display (capitalize first letter)
    display_name = planet_name.capitalize()
    
    # Store current position data
    current_alt = body.alt
    current_az = body.az
    
    # Get rise, set, and transit times
    try:
        body_rise = observer.next_rising(body)
        rise_cst = ephem_to_datetime(body_rise).astimezone(pytz.timezone('America/Chicago'))
    except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
        rise_cst = "Not available"
    
    try:
        body_set = observer.next_setting(body)
        set_cst = ephem_to_datetime(body_set).astimezone(pytz.timezone('America/Chicago'))
    except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
        set_cst = "Not available"
    
    try:
        body_transit = observer.next_transit(body)
        transit_cst = ephem_to_datetime(body_transit).astimezone(pytz.timezone('America/Chicago'))
    except (ephem.CircumpolarError) as e:
        transit_cst = "Not available"
    
    # Convert to CST time zone for display
    cst = pytz.timezone('America/Chicago')
    
    # Display common information for all celestial bodies
    if planet_name != 'moon':
        # Get distance from Earth (in AU and km)
        distance_au = body.earth_distance
        distance_km = distance_au * 149597870.7  # 1 AU = 149,597,870.7 km
        
        print(f"{display_name} distance from Earth: {distance_au:.4f} AU ({format_distance_km(distance_km)})")
        # Calculate and display one-way light time
        light_time_seconds = distance_km / SPEED_OF_LIGHT
        light_time_minutes = light_time_seconds / 60
        print(f"{display_name} light time: {light_time_minutes:.2f} minutes")
        print(f"{display_name} apparent magnitude: {body.mag:.2f}")
        print(f"{display_name} angular size: {body.size:.2f} arcseconds")
    else:
        # Moon-specific information
        moon_phase = body.phase
        print(f"{display_name} phase: {moon_phase:.1f}%")
        # Calculate distance in kilometers (Moon doesn't have earth_distance attribute)
        distance_km = body.earth_distance * 149597870.7 if hasattr(body, 'earth_distance') else body.distance * 149597870.7
        print(f"{display_name} distance from Earth: {format_distance_km(distance_km)}")
        # Calculate and display one-way light time for Moon (in seconds)
        light_time_seconds = distance_km / SPEED_OF_LIGHT
        print(f"{display_name} light time: {light_time_seconds:.2f} seconds")
        print(f"{display_name} angular size: {body.size:.2f} arcseconds")
    
    # Display rise, transit, and set times
    if isinstance(rise_cst, str):
        print(f"{display_name} rise (CST): {rise_cst}")
    else:
        print(f"{display_name} rise (CST): {rise_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    if isinstance(transit_cst, str):
        print(f"{display_name} transit (CST): {transit_cst}")
    else:
        print(f"{display_name} transit (CST): {transit_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    if isinstance(set_cst, str):
        print(f"{display_name} set (CST): {set_cst}")
    else:
        print(f"{display_name} set (CST): {set_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Get current position in the sky
    altitude_deg = float(current_alt) * 180 / 3.1415926  # Convert radians to degrees
    azimuth_deg = float(current_az) * 180 / 3.1415926  # Convert radians to degrees
    
    print(f"Current {display_name} position above Kansas City:")
    if altitude_deg >= 0:
        print(f"  Altitude: {altitude_deg:.2f}° ({altitude_deg:.2f} degrees above horizon)")
    else:
        print(f"  Altitude: {altitude_deg:.2f}° ({abs(altitude_deg):.2f} degrees below horizon)")
    print(f"  Azimuth: {azimuth_deg:.2f}° ({get_compass_direction(azimuth_deg)})")

def main():
    # Display current datetime at beginning of program execution
    cst = pytz.timezone('America/Chicago')
    current_time = datetime.datetime.now(cst)
    print(f"planets.py 1.1 {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    parser = argparse.ArgumentParser(
        description="planets.py - Display celestial body information for Kansas City, MO"
    )
    parser.add_argument('planet', nargs='?', 
                      help='specify celestial body (mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto, moon)')
    parser.add_argument('-v', '--version', action='store_true', 
                      help='show version information and exit')
    
    args = parser.parse_args()
    
    if args.version:
        print("planets.py - Version 1.0")
        print("Created Thu 20 Mar 2025 09:30:00 AM CDT")
        print("Displays information about celestial bodies for Kansas City, MO")
        print("\nUsage example: python3 planets.py mars")
        print("Supported bodies: mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto, moon")
    elif args.planet:
        show_planet_info(args.planet)
    else:
        parser.print_help()
        print("\nError: You must specify a celestial body. Run with --help for more information.")
        sys.exit(1)

if __name__ == "__main__":
    main()

