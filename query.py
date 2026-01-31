import ephem
import argparse

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Query information about a celestial body')
parser.add_argument('--target', default='Polaris', help='Name of the celestial body to query (default: Polaris)')
args = parser.parse_args()
# Create an observer (optional, if you want position from a specific location)
observer = ephem.Observer()
observer.lat = '40.7128'  # Example: New York latitude
observer.lon = '-74.0060'  # Example: New York longitude
observer.date = ephem.now()

# Access a built-in celestial body
# Handle both solar system objects and stars
solar_system_objects = {
    'Sun': ephem.Sun,
    'Moon': ephem.Moon,
    'Mercury': ephem.Mercury,
    'Venus': ephem.Venus,
    'Mars': ephem.Mars,
    'Jupiter': ephem.Jupiter,
    'Saturn': ephem.Saturn,
    'Uranus': ephem.Uranus,
    'Neptune': ephem.Neptune,
    'Pluto': ephem.Pluto
}

# Set the target based on input
if args.target in solar_system_objects:
    # Create the appropriate solar system object
    target = solar_system_objects[args.target]()
else:
    # For stars, use the star catalog
    try:
        target = ephem.star(args.target)
    except KeyError:
        print("Error: '{}' is not a recognized star or solar system object".format(args.target))
        exit(1)

# Compute the body's position for the current time or observer
target.compute()  # Current time
# OR
target.compute(observer)  # From the observer's perspective

# Get information about the body
print("Target: {}".format(args.target))
print("Right Ascension: {}".format(target.ra))
print("Declination: {}".format(target.dec))
print("Magnitude: {}".format(target.mag))

# Add Alt/Az coordinates
print("\nPosition from Observer:")
print("Altitude: {:.2f}°".format(float(target.alt) * 180 / 3.14159))
print("Azimuth: {:.2f}°".format(float(target.az) * 180 / 3.14159))

# Add rise, transit, and set times
try:
    rise_time = observer.next_rising(target).datetime()
    transit_time = observer.next_transit(target).datetime()
    set_time = observer.next_setting(target).datetime()
    
    print("\nTimes (Local):")
    print("Next Rise: {}".format(rise_time))
    print("Next Transit: {}".format(transit_time))
    print("Next Set: {}".format(set_time))
except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
    print("\nNote: {}".format(e))

# Add distance from Earth and light time (when available)
if hasattr(target, 'earth_distance'):
    # Convert from AU to kilometers
    distance_km = target.earth_distance * 149597870.7
    light_time_minutes = target.earth_distance * 8.316746  # Light time in minutes (1 AU = 8.316746 minutes)
    
    print("\nDistance Information:")
    print("Distance from Earth: {:.2f} AU ({:.2f} km)".format(target.earth_distance, distance_km))
    print("Light Time: {:.2f} minutes".format(light_time_minutes))
