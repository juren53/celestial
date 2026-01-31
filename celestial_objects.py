#!/usr/bin/env python3
"""
celestial_objects.py - A Python script to display information about celestial objects

This script uses the PyEphem library to provide astronomical data about various
celestial objects including galaxies, star clusters, constellations, and individual stars.
It displays common attributes like coordinates, magnitude, rise/set times, and 
current position in the sky from an observer's location on Earth.
"""

import ephem
import datetime
import math
import sys

# Set default observer location and time (can be modified by user)
def create_observer(lat='39.7128', lon='-94.0060', elevation=800):   # Kansas City
# def create_observer(lat='40.7128', lon='-74.0060', elevation=0):   # New York

    """
    Create an observer at the specified location.
    Default: New York City coordinates
    
    Args:
        lat (str): Latitude in degrees (negative for South)
        lon (str): Longitude in degrees (negative for West)
        elevation (float): Elevation in meters
        
    Returns:
        ephem.Observer: Observer object at the specified location
    """
    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.elevation = elevation
    observer.date = ephem.now()
    return observer

def degrees_to_dms(degrees):
    """
    Convert decimal degrees to degrees, minutes, seconds format.
    
    Args:
        degrees (float): Angle in decimal degrees
        
    Returns:
        str: Formatted string in DMS notation
    """
    is_negative = degrees < 0
    degrees = abs(degrees)
    d = int(degrees)
    minutes = (degrees - d) * 60
    m = int(minutes)
    s = (minutes - m) * 60
    
    if is_negative:
        sign = '-'
    else:
        sign = '+'
        
    return f"{sign}{d}° {m}' {s:.1f}\""

def hours_to_hms(hours):
    """
    Convert decimal hours to hours, minutes, seconds format.
    
    Args:
        hours (float): Hours in decimal format
        
    Returns:
        str: Formatted string in HMS notation
    """
    h = int(hours)
    minutes = (hours - h) * 60
    m = int(minutes)
    s = (minutes - m) * 60
    
    return f"{h}h {m}m {s:.1f}s"

def display_object_info(celestial_object, observer):
    """
    Display detailed information about a celestial object.
    
    Args:
        celestial_object (ephem object): The celestial object to display information for
        observer (ephem.Observer): The observer's location on Earth
    """
    # Compute the object's position for the current time and observer location
    celestial_object.compute(observer)
    
    # Get the object's name
    name = celestial_object.name
    
    # Create a separator line sized to the name
    separator = "-" * (len(name) + 4)
    
    print(f"\n{separator}")
    print(f"| {name} |")
    print(f"{separator}")
    
    # Display coordinates
    ra_str = hours_to_hms(celestial_object.ra * 12 / math.pi)
    dec_str = degrees_to_dms(celestial_object.dec * 180 / math.pi)
    print(f"Right Ascension: {ra_str}")
    print(f"Declination: {dec_str}")
    
    # Display magnitude if available
    try:
        print(f"Magnitude: {celestial_object.mag:.1f}")
    except AttributeError:
        print("Magnitude: Not available")
    
    # Display size information if available
    try:
        size_arcmin = celestial_object.size / 60  # Convert from arcseconds to arcminutes
        print(f"Angular Size: {size_arcmin:.1f} arcminutes")
    except AttributeError:
        print("Angular Size: Not available")
    
    # Display current position in the sky
    alt_deg = celestial_object.alt * 180 / math.pi
    az_deg = celestial_object.az * 180 / math.pi
    print(f"Current Altitude: {alt_deg:.1f}° ({'below horizon' if alt_deg < 0 else 'above horizon'})")
    print(f"Current Azimuth: {az_deg:.1f}°")
    
    # Display rise, transit, and set times
    try:
        rise_time = observer.next_rising(celestial_object)
        transit_time = observer.next_transit(celestial_object)
        set_time = observer.next_setting(celestial_object)
        
        print(f"Next Rise: {ephem.localtime(rise_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Next Transit: {ephem.localtime(transit_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Next Set: {ephem.localtime(set_time).strftime('%Y-%m-%d %H:%M:%S')}")
    except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
        if isinstance(e, ephem.AlwaysUpError):
            print("This object is always above the horizon from your location.")
        else:
            print("This object never rises above the horizon from your location.")
    except Exception as e:
        print(f"Could not compute rise/set times: {e}")

def create_celestial_objects():
    """
    Create a dictionary of celestial objects to observe.
    
    Returns:
        dict: Dictionary of celestial objects with their names as keys
    """
    celestial_objects = {}
    
    # Deep Sky Objects (Galaxies, Nebulae, Clusters)
    andromeda = ephem.FixedBody()
    andromeda.name = "Andromeda Galaxy (M31)"
    andromeda._ra = '00:42:44.3'
    andromeda._dec = '41:16:09'
    andromeda.mag = 3.4
    celestial_objects["andromeda"] = andromeda
    
    pleiades = ephem.FixedBody()
    pleiades.name = "The Pleiades (M45)"
    pleiades._ra = '03:47:24'
    pleiades._dec = '24:07:00'
    pleiades.mag = 1.6
    celestial_objects["pleiades"] = pleiades
    
    orion_nebula = ephem.FixedBody()
    orion_nebula.name = "Orion Nebula (M42)"
    orion_nebula._ra = '05:35:17.3'
    orion_nebula._dec = '-05:23:28'
    orion_nebula.mag = 4.0
    celestial_objects["orion_nebula"] = orion_nebula
    
    # Bright Stars
    betelgeuse = ephem.star("Betelgeuse")
    celestial_objects["betelgeuse"] = betelgeuse
    
    sirius = ephem.star("Sirius")
    celestial_objects["sirius"] = sirius
    
    antares = ephem.star("Antares")  # Brightest star in Scorpius
    celestial_objects["antares"] = antares
    
    # Stars in Sagittarius
    kaus_australis = ephem.FixedBody()
    kaus_australis.name = "Kaus Australis (ε Sagittarii)"
    kaus_australis._ra = '18:24:10.3'
    kaus_australis._dec = '-34:23:04.6'
    kaus_australis.mag = 1.85
    celestial_objects["kaus_australis"] = kaus_australis
    
    nunki = ephem.FixedBody()
    nunki.name = "Nunki (σ Sagittarii)"
    nunki._ra = '18:55:15.9'
    nunki._dec = '-26:17:48.2'
    nunki.mag = 2.05
    celestial_objects["nunki"] = nunki
    
    # Planets (using built-in ephem objects)
    celestial_objects["jupiter"] = ephem.Jupiter()
    celestial_objects["saturn"] = ephem.Saturn()
    celestial_objects["mars"] = ephem.Mars()
    celestial_objects["venus"] = ephem.Venus()
    
    # Example: Adding a new deep sky object
    # -----------------------------------------
    # whirlpool_galaxy = ephem.FixedBody()                # Create a FixedBody object
    # whirlpool_galaxy.name = "Whirlpool Galaxy (M51)"    # Set a descriptive name
    # whirlpool_galaxy._ra = '13:29:52.7'                 # Right Ascension in HH:MM:SS.S format
    # whirlpool_galaxy._dec = '47:11:43'                  # Declination in DD:MM:SS format
    # whirlpool_galaxy.mag = 8.4                          # Visual magnitude
    # celestial_objects["whirlpool"] = whirlpool_galaxy   # Add to dictionary with a unique key
    #
    # For stars in built-in catalog: star = ephem.star("Star Name")
    # For planets: Use built-in objects like ephem.Jupiter(), ephem.Mars(), etc.
    
    return celestial_objects

def display_all_objects(observer):
    """
    Display a summary of all available celestial objects.
    
    Args:
        observer (ephem.Observer): The observer's location on Earth
    """
    celestial_objects = create_celestial_objects()
    
    print("\n=== Available Celestial Objects ===")
    print(f"{'Object Name':<30} {'RA':<15} {'Dec':<15} {'Mag':<8} {'Alt':<8}")
    print("-" * 80)
    
    for key, obj in sorted(celestial_objects.items()):
        obj.compute(observer)
        
        # Format the coordinates for display
        ra_str = f"{obj.ra * 12 / math.pi:.2f}h"
        dec_str = f"{obj.dec * 180 / math.pi:.2f}°"
        
        # Get magnitude if available
        try:
            mag_str = f"{obj.mag:.1f}"
        except AttributeError:
            mag_str = "N/A"
        
        # Current altitude
        alt_str = f"{obj.alt * 180 / math.pi:.1f}°"
        
        print(f"{obj.name:<30} {ra_str:<15} {dec_str:<15} {mag_str:<8} {alt_str:<8}")

def main():
    """
    Main function to run the celestial objects information script.
    """
    print("=== Celestial Objects Information ===")
    
    # Create the observer at the default location (New York City)
    observer = create_observer()
    
    # Display the current observer information
    local_time = ephem.localtime(observer.date)
    print(f"\nObserver Location: Latitude {observer.lat}, Longitude {observer.lon}")
    print(f"Date and Time: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create all celestial objects
    celestial_objects = create_celestial_objects()
    
    while True:
        print("\nOptions:")
        print("1. Display all available celestial objects")
        print("2. Display detailed information for a specific object")
        print("3. Change observer location")
        print("4. Update date/time")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            display_all_objects(observer)
        
        elif choice == '2':
            # Display all object keys for selection
            display_all_objects(observer)
            
            print("\nAvailable objects for detailed view:")
            for i, key in enumerate(sorted(celestial_objects.keys()), 1):
                print(f"{i}. {key} ({celestial_objects[key].name})")
            
            try:
                obj_choice = int(input("\nEnter the number of the object to view (or 0 to cancel): "))
                if 0 < obj_choice <= len(celestial_objects):
                    selected_key = sorted(celestial_objects.keys())[obj_choice - 1]
                    display_object_info(celestial_objects[selected_key], observer)
                elif obj_choice != 0:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == '3':
            try:
                lat = input("Enter latitude in degrees (negative for South, e.g., 40.7128): ")
                lon = input("Enter longitude in degrees (negative for West, e.g., -74.0060): ")
                elevation = float(input("Enter elevation in meters (e.g., 10): "))
                observer = create_observer(lat, lon, elevation)
                print(f"Observer location updated to: Latitude {observer.lat}, Longitude {observer.lon}, Elevation {observer.elevation}m")
            except ValueError:
                print("Invalid input. Using default location.")
                observer = create_observer()
        
        elif choice == '4':
            try:
                date_str = input("Enter date and time (YYYY/MM/DD HH:MM:SS) or press Enter for current time: ")
                if date_str.strip():
                    observer.date = date_str
                else:
                    observer.date = ephem.now()
                local_time = ephem.localtime(observer.date)
                print(f"Date and time updated to: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
            except ValueError:
                print("Invalid date format. Using current time.")
                observer.date = ephem.now()
        
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

