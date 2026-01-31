#!/usr/bin/env python3
import ephem
from datetime import datetime

# Function to display all relevant attributes of a celestial object
def print_celestial_info(obj, obj_type):
    print(f"\n{'=' * 30}")
    try:
        print(f"Information for {obj.name} ({obj_type})")
    except AttributeError:
        print(f"Information for Unknown Object ({obj_type})")
    print(f"{'=' * 30}")
    
    # Basic positional information
    print(f"\n-- Basic Information --")
    try:
        print(f"Name: {obj.name}")
    except AttributeError:
        print(f"Name: Not available")
    
    # Coordinates
    print(f"\n-- Coordinates --")
    try:
        print(f"Right Ascension: {obj.ra} (Hours:Minutes:Seconds)")
    except AttributeError:
        print(f"Right Ascension: Not available")
    
    try:
        print(f"Declination: {obj.dec} (Degrees:Minutes:Seconds)")
    except AttributeError:
        print(f"Declination: Not available")
    
    try:
        print(f"Azimuth: {obj.az} (Altitude above horizon)")
    except AttributeError:
        print(f"Azimuth: Not available")
    
    try:
        print(f"Altitude: {obj.alt} (Direction along horizon)")
    except AttributeError:
        print(f"Altitude: Not available")
    
    # Magnitude and distance
    print(f"\n-- Appearance and Distance --")
    try:
        print(f"Magnitude: {obj.mag} (Apparent brightness - lower is brighter)")
    except AttributeError:
        print(f"Magnitude: Not available")
    
    try:
        print(f"Size: {obj.size} (Angular diameter in arcseconds)")
    except AttributeError:
        print(f"Size: Not available")
    if hasattr(obj, 'earth_distance'):
        print(f"Distance from Earth: {obj.earth_distance} (AU)")
    if hasattr(obj, 'sun_distance'):
        print(f"Distance from Sun: {obj.sun_distance} (AU)")
    
    # Phase information (mainly for solar system objects)
    if hasattr(obj, 'phase'):
        print(f"\n-- Phase Information --")
        print(f"Phase: {obj.phase} (Percentage illuminated)")
    
    # Orbital information (mainly for solar system objects)
    # Always print the orbital information section header, but include "Not available" messages if needed
    print(f"\n-- Orbital Information --")
    try:
        if hasattr(obj, 'elong'):
            print(f"Elongation: {obj.elong} (Angular distance from Sun)")
        else:
            print(f"Elongation: Not available")
            
        if hasattr(obj, 'hlong'):
            print(f"Heliocentric Longitude: {obj.hlong} (Longitude relative to Sun)")
        else:
            print(f"Heliocentric Longitude: Not available")
            
        if hasattr(obj, 'hlat'):
            print(f"Heliocentric Latitude: {obj.hlat} (Latitude relative to Sun)")
        else:
            print(f"Heliocentric Latitude: Not available")
    except Exception as e:
        print(f"Error retrieving orbital information: {e}")
    
    # Rising, transit, and setting times
    print(f"\n-- Rising and Setting --")
    try:
        rising_time = observer.next_rising(obj)
        print(f"Next Rising: {rising_time.datetime()} (local time)")
    except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
        print(f"Next Rising: {e}")
    except Exception as e:
        print(f"Next Rising: Error - {e}")
        
    try:
        transit_time = observer.next_transit(obj)
        print(f"Next Transit: {transit_time.datetime()} (local time)")
    except Exception as e:
        print(f"Next Transit: Error - {e}")
        
    try:
        setting_time = observer.next_setting(obj)
        print(f"Next Setting: {setting_time.datetime()} (local time)")
    except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
        print(f"Next Setting: {e}")
    except Exception as e:
        print(f"Next Setting: Error - {e}")

# Setup observer location (using New York as an example)
observer = ephem.Observer()
observer.lon = '-74.0060'  # Longitude for New York City
observer.lat = '40.7128'   # Latitude for New York City
observer.elevation = 10    # Elevation in meters
observer.date = datetime.utcnow()

print(f"Observer location: New York City")
print(f"Date and time of calculation: {observer.date}")

# Create and compute Jupiter (a solar system object)
jupiter = ephem.Jupiter()
jupiter.compute(observer)

# Create and compute Polaris (a star)
polaris = ephem.star("Polaris")
polaris.compute(observer)

# Display information for both objects
print_celestial_info(jupiter, "Solar System Object")
print_celestial_info(polaris, "Star")

print("\nNote: Not all attributes are available for all celestial objects.")
print("Solar system objects typically have more information about phase,")
print("distance, and orbital elements compared to stars.")

