from astroquery.jplhorizons import Horizons
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
                  location='@sun',  # Observer at Sun (heliocentric)
                  epochs={'start':'2025-03-20', 
                          'stop':'2025-03-27', 
                          'step':'1d'})  # Daily positions for a week

# Get ephemerides data (positional information)
data = voyager1.ephemerides()

# Print selected columns
print(data['datetime_str', 'r', 'delta', 'lighttime', 'RA', 'DEC', 'EclLon', 'EclLat'])
