import ephem
import datetime

# Kansas City, MO observer location (matches moon.py)
OBSERVER_LAT = '39.0997'
OBSERVER_LON = '-94.5786'

# Helper function to convert azimuth in degrees to a compass direction
def get_compass_direction(azimuth):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(azimuth / 22.5) % 16
    return directions[index]

class VoyagerProbe:
    def __init__(self, name, launch_date, distance_at_epoch, distance_epoch, speed_mph, ra, dec):
        """
        Initialize a Voyager probe with its specific mission parameters.

        :param name: Name of the probe (Voyager 1 or Voyager 2)
        :param launch_date: Date of launch
        :param distance_at_epoch: Distance from Earth in kilometers, as measured on distance_epoch
        :param distance_epoch: datetime.date the distance_at_epoch measurement was taken
        :param speed_mph: Heliocentric speed in miles per hour
        :param ra: Right ascension of the probe's current sky position (e.g. '17:12:06')
        :param dec: Declination of the probe's current sky position (e.g. '+12:04:00')
        """
        self.name = name
        self.launch_date = launch_date
        self.distance_at_epoch = distance_at_epoch
        self.distance_epoch = distance_epoch

        # Sky position (RA/Dec). The probes are so distant that this direction
        # shifts negligibly over human timescales, so it's treated as fixed.
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
        Estimate the probe's current distance from Earth by extrapolating
        from the distance_at_epoch snapshot using its heliocentric speed.

        :return: Estimated current distance in kilometers
        """
        days_elapsed = (datetime.date.today() - self.distance_epoch).days
        seconds_elapsed = days_elapsed * 24 * 60 * 60
        return self.distance_at_epoch + self.speed_kms * seconds_elapsed

    def calculate_light_time(self):
        """
        Calculate the light travel time from the probe to Earth.

        :return: Light time in hours and minutes
        """
        speed_of_light_kms = 299_792.458  # km/s
        light_time_seconds = self.calculate_current_distance() / speed_of_light_kms
        light_time_hours = light_time_seconds / 3600
        light_time_minutes = (light_time_seconds % 3600) / 60
        
        return light_time_hours, light_time_minutes

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
    hours, minutes = voyager1.calculate_light_time()
    print(f"Light Time from Earth: {int(hours)} hours {int(minutes)} minutes")
    alt, az = voyager1.calculate_alt_az()
    print(f"Current position above Kansas City:")
    print(f"  Altitude: {alt:.2f}° ({alt:.2f} degrees above horizon)")
    print(f"  Azimuth: {az:.2f}° ({get_compass_direction(az)})")

    print("\n")
    
    # Probe 2 calculations
    print(f"{voyager2.name} Probe Details:")
    print(f"Heliocentric Speed: {voyager2.calculate_heliocentric_speed()} mph")
    print(f"Heliocentric Speed: {voyager2.calculate_heliocentric_speed('kms'):.2f} km/s")
    print(f"Years in Space: {voyager2.calculate_years_in_space()}")
    print(f"Estimated Total Distance Traveled: {voyager2.calculate_total_distance_traveled() / 1_000_000_000:.2f} billion km")
    hours, minutes = voyager2.calculate_light_time()
    print(f"Light Time from Earth: {int(hours)} hours {int(minutes)} minutes")
    alt, az = voyager2.calculate_alt_az()
    print(f"Current position above Kansas City:")
    print(f"  Altitude: {alt:.2f}° ({alt:.2f} degrees above horizon)")
    print(f"  Azimuth: {az:.2f}° ({get_compass_direction(az)})")

if __name__ == "__main__":
    main()
