#!/usr/bin/env python3
"""
PyEphem Demonstration Script

This script demonstrates the major features of the PyEphem library,
including examples of different celestial objects, astronomical events,
and various calculations.

PyEphem provides scientific-grade astronomical computations for Python programs.
It can calculate the positions of stars, planets, comets, asteroids,
and Earth satellites, as well as various astronomical events.
"""

import ephem
import math
from datetime import datetime, timedelta

def print_section_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def degrees(rad):
    """Convert radians to degrees for display purposes."""
    return math.degrees(float(rad))

# ------------------------------------------------------------------------
print_section_header("BASIC SETUP AND INTRODUCTION")
# ------------------------------------------------------------------------

print("PyEphem version:", ephem.__version__)
print("\nCurrent date and time:", ephem.now())

# Create a date for calculations (current time)
current_time = ephem.now()
print(f"Current time in PyEphem format: {current_time}")

# Future date
future_date = ephem.Date(datetime.now() + timedelta(days=30))
print(f"Date 30 days from now: {future_date}")
print(f"Date 30 days from now (formatted): {ephem.localtime(future_date)}")

# ------------------------------------------------------------------------
print_section_header("SOLAR SYSTEM OBJECTS")
# ------------------------------------------------------------------------

# Define a dictionary of all solar system bodies available in PyEphem
solar_system_bodies = {
    'Sun': ephem.Sun(),
    'Moon': ephem.Moon(),
    'Mercury': ephem.Mercury(),
    'Venus': ephem.Venus(),
    'Mars': ephem.Mars(),
    'Jupiter': ephem.Jupiter(),
    'Saturn': ephem.Saturn(),
    'Uranus': ephem.Uranus(),
    'Neptune': ephem.Neptune(),
    'Pluto': ephem.Pluto()  # Even though not technically a planet anymore
}

print("Information about Solar System bodies (current positions):")
print("\n{:<10} {:<10} {:<10} {:<15} {:<15} {:<10}".format(
    "Body", "RA", "Dec", "Distance (AU)", "Magnitude", "Phase"
))
print("-" * 75)

for name, body in solar_system_bodies.items():
    body.compute(current_time)  # Compute position for current time
    
    # Format and display information
    ra_formatted = body.ra * 12 / math.pi  # Convert to hours
    dec_formatted = degrees(body.dec)
    
    # Distance in AU if available, otherwise N/A
    distance = getattr(body, 'earth_distance', None)
    if distance is None:
        distance = "N/A"
    else:
        distance = f"{float(distance):.6f}"
    
    # Phase information (only relevant for some objects)
    phase = getattr(body, 'phase', None)
    if phase is None:
        phase = "N/A"
    else:
        phase = f"{float(phase):.1f}%"
    
    print("{:<10} {:<10.2f} {:<10.2f} {:<15} {:<15.2f} {:<10}".format(
        name, ra_formatted, dec_formatted, distance, body.mag, phase
    ))

# ------------------------------------------------------------------------
print_section_header("WORKING WITH STARS")
# ------------------------------------------------------------------------

# Some well-known stars
star_names = ['Polaris', 'Vega', 'Altair', 'Deneb', 'Betelgeuse', 
              'Rigel', 'Sirius', 'Antares', 'Aldebaran', 'Spica']

print("Information about some well-known stars:")
print("\n{:<12} {:<10} {:<10} {:<15}".format(
    "Star", "RA", "Dec", "Magnitude"
))
print("-" * 50)

for name in star_names:
    try:
        star = ephem.star(name)
        star.compute(current_time)
        
        ra_formatted = star.ra * 12 / math.pi  # Convert to hours
        dec_formatted = degrees(star.dec)
        
        print("{:<12} {:<10.2f} {:<10.2f} {:<15.2f}".format(
            name, ra_formatted, dec_formatted, star.mag
        ))
    except KeyError:
        print(f"{name}: Not found in database")

# ------------------------------------------------------------------------
print_section_header("OBSERVER SETUP AND LOCATION-BASED CALCULATIONS")
# ------------------------------------------------------------------------

# Create an observer (New York City as an example)
observer = ephem.Observer()
observer.lat = '40.7128'  # Latitude in degrees (N is +, S is -)
observer.lon = '-74.0060'  # Longitude in degrees (E is +, W is -)
observer.elevation = 10  # Elevation in meters
observer.date = current_time

print(f"Observer location: New York City")
print(f"Latitude: {observer.lat}")
print(f"Longitude: {observer.lon}")
print(f"Elevation: {observer.elevation} meters")
print(f"Date/Time: {observer.date}\n")

# Calculate next rising and setting times for some objects
print("Rising and setting times for celestial objects:")
print("\n{:<8} {:<25} {:<25} {:<15}".format(
    "Object", "Next Rising", "Next Setting", "Currently Up?"
))
print("-" * 75)

for name, body in list(solar_system_bodies.items())[:5]:  # Just show first 5 for brevity
    try:
        # Try to compute next rising and setting
        rising = observer.next_rising(body)
        setting = observer.next_setting(body)
        
        # Compute if currently above horizon
        observer.date = current_time
        body.compute(observer)
        is_up = "Yes" if body.alt > 0 else "No"
        
        print("{:<8} {:<25} {:<25} {:<15}".format(
            name, 
            ephem.localtime(rising).strftime('%Y-%m-%d %H:%M:%S'),
            ephem.localtime(setting).strftime('%Y-%m-%d %H:%M:%S'),
            is_up
        ))
    except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
        print("{:<8} {:<60}".format(name, f"Special case: {str(e)}"))

# ------------------------------------------------------------------------
print_section_header("ASTRONOMICAL EVENTS")
# ------------------------------------------------------------------------

# Calculate equinoxes and solstices for the current year
year = ephem.now().datetime().year
print(f"Equinoxes and Solstices for {year}:")

vernal_equinox = ephem.next_vernal_equinox(f"{year}/01/01")
summer_solstice = ephem.next_summer_solstice(f"{year}/01/01")
autumnal_equinox = ephem.next_autumnal_equinox(f"{year}/01/01")
winter_solstice = ephem.next_winter_solstice(f"{year}/01/01")

print(f"Vernal Equinox:   {ephem.localtime(vernal_equinox).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Summer Solstice:   {ephem.localtime(summer_solstice).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Autumnal Equinox: {ephem.localtime(autumnal_equinox).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Winter Solstice:   {ephem.localtime(winter_solstice).strftime('%Y-%m-%d %H:%M:%S')}")

# Calculate moon phases
print("\nUpcoming Moon Phases:")
next_new_moon = ephem.next_new_moon(current_time)
next_first_quarter = ephem.next_first_quarter_moon(current_time)
next_full_moon = ephem.next_full_moon(current_time)
next_last_quarter = ephem.next_last_quarter_moon(current_time)

print(f"Next New Moon:        {ephem.localtime(next_new_moon).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Next First Quarter:   {ephem.localtime(next_first_quarter).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Next Full Moon:       {ephem.localtime(next_full_moon).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Next Last Quarter:    {ephem.localtime(next_last_quarter).strftime('%Y-%m-%d %H:%M:%S')}")

# ------------------------------------------------------------------------
print_section_header("ADVANCED CALCULATIONS")
# ------------------------------------------------------------------------

# Calculate angular separation between objects
print("Angular Separations between selected pairs:")
print("\n{:<20} {:<20} {:<15}".format("Object 1", "Object 2", "Separation (°)"))
print("-" * 55)

pairs = [
    (solar_system_bodies['Sun'], solar_system_bodies['Moon']),
    (solar_system_bodies['Venus'], solar_system_bodies['Jupiter']),
    (ephem.star('Sirius'), ephem.star('Procyon')),
]

for obj1, obj2 in pairs:
    obj1.compute(current_time)
    obj2.compute(current_time)
    
    # Get names (a bit of a hack but works for this demo)
    name1 = obj1.__class__.__name__
    name2 = obj2.__class__.__name__
    
    # Calculate separation
    separation = degrees(ephem.separation(obj1, obj2))
    
    print("{:<20} {:<20} {:<15.2f}".format(name1, name2, separation))

# Planetary elongations from the Sun
print("\nElongations from the Sun:")
print("\n{:<10} {:<15} {:<20}".format("Planet", "Elongation (°)", "Configuration"))
print("-" * 45)

sun = solar_system_bodies['Sun']
sun.compute(current_time)

for name in ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
    planet = solar_system_bodies[name]
    planet.compute(current_time)
    
    elongation = degrees(ephem.separation(sun, planet))
    
    # Determine if planet is at opposition, conjunction, etc.
    if elongation < 20:
        config = "Near conjunction"
    elif abs(elongation - 90) < 10:
        config = "Near quadrature"
    elif elongation > 170:
        config = "Near opposition"
    else:
        config = "Intermediate"
    
    print("{:<10} {:<15.2f} {:<20}".format(name, elongation, config))

# ------------------------------------------------------------------------
print_section_header("CREATING CUSTOM OBJECTS")
# ------------------------------------------------------------------------

# Create a custom comet
print("Defining a custom comet (Halley's Comet):")
halley = ephem.EllipticalBody()
halley._inc = 162.3 * ephem.degree  # Inclination
halley._Om = 58.42 * ephem.degree   # Longitude of ascending node
halley._om = 111.33 * ephem.degree  # Argument of perihelion
halley._a = 17.834                  # Mean distance (semi-major axis)
halley._e = 0.967                   # Eccentricity
halley._epoch_M = 2446470.5         # Epoch of mean anomaly
halley._M = 38.38 * ephem.degree    # Mean anomaly
halley._epoch = 2446470.5           # Epoch of orbital elements
halley._H = 5.5                     # Absolute magnitude
halley._G = 0.15                    # Slope parameter

# Compute the position
halley.compute(current_time)
print(f"Halley's comet position (RA): {halley.ra}")
print(f"Halley's comet position (Dec): {halley.dec}")
print(f"Halley's comet magnitude: {halley.mag}")

# Create a custom asteroid
print("\nDefining a custom asteroid (Ceres):")
ceres = ephem.EllipticalBody()
ceres._inc = 10.593 * ephem.degree
ceres._Om = 80.399 * ephem.degree
ceres._om = 73.597 * ephem.degree
ceres._a = 2.766
ceres._e = 0.079
ceres._epoch = 2451545.0  # J2000
ceres._M = 77.372 * ephem.degree
ceres._H = 3.34
ceres._G = 0.12

# Compute the position
ceres.compute(current_time)
print(f"Ceres position (RA): {ceres.ra}")
print(f"Ceres position (Dec): {ceres.dec}")
print(f"Ceres magnitude: {ceres.mag}")

# ------------------------------------------------------------------------
print_section_header("ADDITIONAL FEATURES AND UTILITIES")
# ------------------------------------------------------------------------

# Demonstrate coordinate conversion
print("Coordinate Conversion Examples:")
observer.date = current_time

# Convert altitude/azimuth to right ascension/declination
alt = 45 * ephem.degree  # 45 degrees altitude
az = 180 * ephem.degree  # South azimuth
ra, dec = observer.radec_of(az, alt)
print(f"Alt/Az (45°, 180°) → RA/Dec: {degrees(ra)/15:.2f}h, {degrees(dec):.2f}°")

# Convert right ascension/declination to altitude/azimuth
vega = ephem.star("Vega")
vega.compute(observer)
print(f"Vega RA/Dec → Alt/Az: {degrees(vega.alt):.2f}°, {degrees(vega.az):.2f}°")

# Atmospheric refraction section removed (function not available in this PyEphem version)

# Note: Precession calculations have been removed as they're not supported in this PyEphem version
# ------------------------------------------------------------------------
print_section_header("CONCLUSION")
# ------------------------------------------------------------------------

print("This demonstration shows the major capabilities of the PyEphem library for astronomical calculations.")
print("PyEphem can be used for a wide range of astronomical computations including:")
print("  - Calculating positions of solar system objects and stars")
print("  - Determining rise, transit, and set times")
print("  - Finding dates of astronomical events like equinoxes and moon phases")
print("  - Converting between coordinate systems")
print("  - Creating custom celestial objects")
print("  - And much more!")
print("\nFor more information, visit: https://rhodesmill.org/pyephem/")
