import ephem
import datetime
import math

AU_KM = 149_597_870.7

# Kansas City, MO observer location (matches moon.py)
OBSERVER_LAT = '39.0997'
OBSERVER_LON = '-94.5786'

# Helper function to convert azimuth in degrees to a compass direction
def get_compass_direction(azimuth):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(azimuth / 22.5) % 16
    return directions[index]

def _equatorial_vector(ra, dec, distance):
    """Convert RA/Dec (radians) and distance into an equatorial x, y, z vector."""
    ra, dec = float(ra), float(dec)
    return [distance * math.cos(dec) * math.cos(ra),
            distance * math.cos(dec) * math.sin(ra),
            distance * math.sin(dec)]

def _earth_position_km(when):
    """Earth's heliocentric equatorial (J2000) position in km at a UTC datetime."""
    sun = ephem.Sun()
    sun.compute(ephem.Date(when))
    # Earth is opposite the geocentric Sun direction
    return [-c for c in _equatorial_vector(sun.a_ra, sun.a_dec, sun.earth_distance * AU_KM)]

class VoyagerProbe:
    def __init__(self, name, launch_date, distance_at_epoch, distance_epoch, speed_mph, ra, dec):
        """
        Initialize a Voyager probe with its specific mission parameters.

        :param name: Name of the probe (Voyager 1 or Voyager 2)
        :param launch_date: Date of launch
        :param distance_at_epoch: Distance from Earth in kilometers, as measured on distance_epoch
        :param distance_epoch: datetime.date the distance_at_epoch measurement was taken
            (and the date the ra/dec snapshot is for)
        :param speed_mph: Heliocentric speed in miles per hour
        :param ra: Right ascension of the probe's current sky position (e.g. '17:12:06')
        :param dec: Declination of the probe's current sky position (e.g. '+12:04:00')
        """
        self.name = name
        self.launch_date = launch_date
        self.distance_at_epoch = distance_at_epoch
        self.distance_epoch = distance_epoch

        # Sky position (RA/Dec), treated as fixed since it shifts slowly.
        # NOTE: this is a snapshot, not a live value (PyEphem's FixedBody
        # won't advance it) - drifted ~0.8 deg/year for Voyager 1 as of
        # 2026, and Voyager 2 drifts enough to matter over a year too.
        # Distance/light time is projected geometrically (see
        # calculate_current_distance), which tracks Earth's orbital motion,
        # so it stays accurate for much longer than the old constant
        # range-rate extrapolation did. Still re-check ra/dec/distance
        # against JPL Horizons about once a year.
        self.ra = ra
        self.dec = dec

        # Specific velocities for each probe
        self.speed_mph = speed_mph
        self.speed_kms = speed_mph * 0.44704 / 1000  # Convert mph to km/s
    
    def calculate_heliocentric_speed(self, unit='mph'):
        """
        Calculate the probe's speed relative to the Sun.
        
        :param unit: Unit of speed measurement (mph or kms)
        :return: Speed in specified units
        """
        if unit == 'mph':
            return self.speed_mph
        elif unit == 'kms':
            return self.speed_kms
        else:
            raise ValueError("Invalid speed unit. Choose 'mph' or 'kms'.")
    
    def calculate_years_in_space(self):
        """
        Calculate the number of years the probe has been in space.

        :return: Years in space
        """
        from datetime import datetime
        return datetime.now().year - self.launch_date
    
    def calculate_total_distance_traveled(self):
        """
        Estimate total distance traveled based on heliocentric speed.
        
        :return: Total distance in kilometers
        """
        years_in_space = self.calculate_years_in_space()
        seconds_in_year = 365.25 * 24 * 60 * 60
        
        return self.speed_kms * seconds_in_year * years_in_space
    
    def calculate_current_distance(self):
        """
        Estimate the probe's current distance from Earth.

        Earth's orbital motion makes the Earth-probe range rate swing by
        tens of km/s over a year, so a constant-rate extrapolation drifts
        by minutes of light time within a few months. Instead:
          1. Convert the epoch snapshot (RA/Dec + distance from Earth) into
             a heliocentric position by adding Earth's position on that date.
          2. Move the probe radially outward from the Sun at its
             heliocentric speed (its trajectory is essentially radial now).
          3. Take the distance from Earth's actual position today.

        :return: Estimated current distance in kilometers
        """
        epoch = datetime.datetime.combine(self.distance_epoch, datetime.time())
        now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)

        geo = _equatorial_vector(ephem.hours(self.ra), ephem.degrees(self.dec),
                                 self.distance_at_epoch)
        helio = [g + e for g, e in zip(geo, _earth_position_km(epoch))]
        r = math.hypot(*helio)
        seconds_elapsed = (now - epoch).total_seconds()
        helio_now = [p * (1 + self.speed_kms * seconds_elapsed / r) for p in helio]

        return math.dist(helio_now, _earth_position_km(now))

    def calculate_light_time(self):
        """
        Calculate the light travel time from the probe to Earth.

        :return: Light time as (hours, minutes, seconds)
        """
        speed_of_light_kms = 299_792.458  # km/s
        light_time_seconds = self.calculate_current_distance() / speed_of_light_kms
        hours = int(light_time_seconds // 3600)
        minutes = int((light_time_seconds % 3600) // 60)
        seconds = int(light_time_seconds % 60)

        return hours, minutes, seconds

    def calculate_alt_az(self, lat=OBSERVER_LAT, lon=OBSERVER_LON):
        """
        Calculate the probe's current altitude and azimuth as seen from an
        observer location on Earth.

        :param lat: Observer latitude (default Kansas City, MO)
        :param lon: Observer longitude (default Kansas City, MO)
        :return: (altitude_deg, azimuth_deg)
        """
        observer = ephem.Observer()
        observer.lat = lat
        observer.lon = lon
        observer.date = datetime.datetime.now(datetime.UTC)  # PyEphem expects UTC time

        probe = ephem.FixedBody()
        probe._ra = ephem.hours(self.ra)
        probe._dec = ephem.degrees(self.dec)
        probe._epoch = ephem.J2000
        probe.compute(observer)

        altitude_deg = float(probe.alt) * 180 / 3.1415926
        azimuth_deg = float(probe.az) * 180 / 3.1415926

        return altitude_deg, azimuth_deg

    def calculate_constellation(self):
        """
        Determine which constellation contains the probe's current sky
        position. Based on RA/Dec (fixed on the celestial sphere), not
        alt/az, since alt/az changes with observer time and location.

        :return: Full constellation name
        """
        _, full_name = ephem.constellation((ephem.hours(self.ra), ephem.degrees(self.dec)))
        return full_name

def main():
    # Create Voyager probe instances with their specific speeds
    # Voyager 1 is traveling slightly faster than Voyager 2
    voyager1 = VoyagerProbe(
        name="Voyager 1",
        launch_date=1977,
        # 170.563053 AU from Earth per JPL Horizons ephemeris (ssd.jpl.nasa.gov)
        distance_at_epoch=25_515_869_488,  # kilometers, as of distance_epoch
        distance_epoch=datetime.date(2026, 7, 20),
        speed_mph=38_210,  # miles per hour
        # RA/Dec per JPL Horizons for 2026-07-20 (heading toward Ophiuchus)
        ra='17:14:57.0',
        dec='+12:23:36.3'
    )

    voyager2 = VoyagerProbe(
        name="Voyager 2",
        launch_date=1977,
        # 142.654588 AU from Earth per JPL Horizons ephemeris (ssd.jpl.nasa.gov)
        distance_at_epoch=21_340_822_626,  # kilometers, as of distance_epoch
        distance_epoch=datetime.date(2026, 7, 20),
        speed_mph=35_000,  # miles per hour
        # RA/Dec per JPL Horizons for 2026-07-20 (heading toward Telescopium/Ara)
        ra='20:12:38.1',
        dec='-59:47:55.3'
    )
    
    # Probe 1 calculations
    print(f"{voyager1.name} Probe Details:")
    print(f"Heliocentric Speed: {voyager1.calculate_heliocentric_speed()} mph")
    print(f"Heliocentric Speed: {voyager1.calculate_heliocentric_speed('kms'):.2f} km/s")
    print(f"Years in Space: {voyager1.calculate_years_in_space()}")
    print(f"Estimated Total Distance Traveled: {voyager1.calculate_total_distance_traveled() / 1_000_000_000:.2f} billion km")
    hours, minutes, seconds = voyager1.calculate_light_time()
    print(f"Light Time from Earth: {hours} hours {minutes} minutes {seconds} seconds")
    alt, az = voyager1.calculate_alt_az()
    print(f"Current position above Kansas City:")
    print(f"  Altitude: {alt:.2f}° ({alt:.2f} degrees above horizon)")
    print(f"  Azimuth: {az:.2f}° ({get_compass_direction(az)})")
    print(f"  Constellation: {voyager1.calculate_constellation()}")

    print("\n")
    
    # Probe 2 calculations
    print(f"{voyager2.name} Probe Details:")
    print(f"Heliocentric Speed: {voyager2.calculate_heliocentric_speed()} mph")
    print(f"Heliocentric Speed: {voyager2.calculate_heliocentric_speed('kms'):.2f} km/s")
    print(f"Years in Space: {voyager2.calculate_years_in_space()}")
    print(f"Estimated Total Distance Traveled: {voyager2.calculate_total_distance_traveled() / 1_000_000_000:.2f} billion km")
    hours, minutes, seconds = voyager2.calculate_light_time()
    print(f"Light Time from Earth: {hours} hours {minutes} minutes {seconds} seconds")
    alt, az = voyager2.calculate_alt_az()
    print(f"Current position above Kansas City:")
    print(f"  Altitude: {alt:.2f}° ({alt:.2f} degrees above horizon)")
    print(f"  Azimuth: {az:.2f}° ({get_compass_direction(az)})")
    print(f"  Constellation: {voyager2.calculate_constellation()}")

if __name__ == "__main__":
    main()
