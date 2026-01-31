import ephem
import datetime
import argparse
def get_visible_celestial_objects(date=None, latitude=39.0997, longitude=-94.5786):
    """
    Calculate visible celestial objects from Kansas City within specified ranges.
    
    Parameters:
    - date: Date of observation (defaults to current date)
    - latitude: Latitude of Kansas City (39.0997° N)
    - longitude: Longitude of Kansas City (94.5786° W)
    
    Returns:
    - List of visible celestial objects
    """
    # Use current date if not specified
    if date is None:
        date = datetime.datetime.now()
    
    # Set up observer location
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    observer.date = date
    
    # List of bright stars and notable celestial objects
    celestial_objects = [
        # Bright Stars
        ('Sirius', ephem.star('Sirius')),
        ('Betelgeuse', ephem.star('Betelgeuse')),
        ('Rigel', ephem.star('Rigel')),
        ('Antares', ephem.star('Antares')),
        ('Aldebaran', ephem.star('Aldebaran')),
        
        # Planets (when visible)
        ('Venus', ephem.Venus()),
        ('Mars', ephem.Mars()),
        ('Jupiter', ephem.Jupiter()),
        ('Saturn', ephem.Saturn())
    ]
    
    # Constellations visible in the specified range
    constellations = [
        'Orion', 'Taurus', 'Gemini', 'Cancer', 'Leo', 
        'Virgo', 'Hydra', 'Canis Major', 'Canis Minor'
    ]
    
    visible_objects = []
    
    for name, obj in celestial_objects:
        try:
            obj.compute(observer)
            
            # Convert to degrees
            az = float(obj.az) * 180 / ephem.pi
            alt = float(obj.alt) * 180 / ephem.pi
            
            # Check if object is within specified ranges
            if 120 <= az <= 220 and 0 <= alt <= 60:
                visible_objects.append({
                    'name': name,
                    'azimuth': az,
                    'altitude': alt
                })
        except Exception as e:
            print(f"Error computing {name}: {e}")
    
    return visible_objects

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Calculate visible celestial objects from a specified location. "
                    "The script identifies stars and planets visible in the southern sky "
                    "with azimuth between 120° and 220° and altitude between 0° and 60°."
    )
    
    # Add arguments
    parser.add_argument('--date', '-d', 
                        help='Date of observation in YYYY-MM-DD format (default: current date)')
    parser.add_argument('--latitude', '-lat', type=float, default=39.0997,
                        help='Latitude of observation location (default: 39.0997 for Kansas City)')
    parser.add_argument('--longitude', '-lon', type=float, default=-94.5786,
                        help='Longitude of observation location (default: -94.5786 for Kansas City)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert date string to datetime object if provided
    date = None
    if args.date:
        try:
            date = datetime.datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format")
            return
    
    # Get visible objects with provided arguments
    visible = get_visible_celestial_objects(
        date=date,
        latitude=args.latitude,
        longitude=args.longitude
    )
    
    # Print results
    print("Visible Celestial Objects [southern]:")
    print("-" * 40)
    
    if visible:
        for obj in visible:
            print(f"Object: {obj['name']}")
            print(f"  Azimuth: {obj['azimuth']:.2f}°")
            print(f"  Altitude: {obj['altitude']:.2f}°")
            print()
    else:
        print("No objects found in the specified range.")

if __name__ == "__main__":
    main()
