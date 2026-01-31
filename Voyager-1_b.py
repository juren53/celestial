from astroquery.jplhorizons import Horizons
import astropy.coordinates as coord
from astropy.units import Quantity
import astropy.units as u
import warnings
import urllib3

# Disable SSL warnings and verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

# Monkey patch the session to disable SSL verification
import astroquery.query
original_get = astroquery.query.BaseQuery._request
def patched_request(self, *args, **kwargs):
    kwargs['verify'] = False
    return original_get(self, *args, **kwargs)
astroquery.query.BaseQuery._request = patched_request


# Query Voyager 1 positions relative to the Sun
# -31 is the HORIZONS ID for Voyager 1
voyager1 = Horizons(id='-31', 
                  location='@399',  # Observer at Earth (geocentric)
                  epochs={'start':'2025-03-20', 
                          'stop':'2025-03-27', 
                          'step':'1d'})  # Daily positions for a week

# Get ephemerides data (positional information)
data = voyager1.ephemerides()

# Print selected columns
print(data['datetime_str', 'r', 'delta', 'lighttime', 'RA', 'DEC', 'EclLon', 'EclLat'])
# Get altitude and azimuth
alt, az = data['EL'], data['AZ']  # Column names are uppercase in the returned data

# Determine constellation for each position
constellations = []
for i in range(len(data)):
    # Create SkyCoord object from RA and DEC
    c = coord.SkyCoord(ra=data['RA'][i]*u.deg, dec=data['DEC'][i]*u.deg, frame='icrs')
    # Get constellation
    constellation = coord.get_constellation(c)
    constellations.append(constellation)

# Print each date's altitude, azimuth, and constellation
print("\nDate\t\tAltitude\tAzimuth\t\tConstellation")
print("-" * 70)
for i in range(len(alt)):
    print(f"{data['datetime_str'][i]}\t{float(alt[i]):.2f}°\t\t{float(az[i]):.2f}°\t\t{constellations[i]}")

# Alternative approach - print just the first date's values
# print(f'Altitude: {float(alt[0]):.2f}, Azimuth: {float(az[0]):.2f}')


"""
import astropy.coordinates as coord
from astropy.units import Quantity  

# ... (rest of your code) 

alt, az = data['EL'], data['AZ']  # Column names are uppercase
# Use float() to convert MaskedColumn values to regular Python floats before formatting
for i in range(len(alt)):
    print(f'Date: {data["datetime_str"][i]}, Altitude: {float(alt[i]):.2f}, Azimuth: {float(az[i]):.2f}')
"""
