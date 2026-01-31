#!/usr/bin/env python3
# moon_24h.py
#----------------------Ver 0.1------------------------------
"""
Moon_24h.py reports the moon's altitude and azimuth for Kansas City, MO
every hour for the next 24 hours.

Based on moon.py Ver 0.3a
Created Fri 31 Jan 2026 Ver 0.1
"""
import ephem
import datetime
import pytz

# Helper function to convert azimuth in degrees to a compass direction
def get_compass_direction(azimuth):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(azimuth / 22.5) % 16
    return directions[index]

def main():
    cst = pytz.timezone('America/Chicago')
    now_cst = datetime.datetime.now(cst)
    print(f"moon_24h.py 0.1  {now_cst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Moon altitude & azimuth for Kansas City, MO — next 24 hours")
    print(f"{'':->66}")
    print(f"{'Time (CST/CDT)':<24} {'Altitude':>10} {'Azimuth':>10}  {'Dir':<4}")
    print(f"{'':->66}")

    # Start from the next whole hour
    now_utc = datetime.datetime.utcnow()
    start = now_utc.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)

    for hour in range(24):
        calc_time = start + datetime.timedelta(hours=hour)

        observer = ephem.Observer()
        observer.lat = '39.0997'   # Kansas City, MO latitude
        observer.lon = '-94.5786'  # Kansas City, MO longitude
        observer.date = calc_time

        moon = ephem.Moon()
        moon.compute(observer)

        altitude_deg = float(moon.alt) * 180 / 3.1415926
        azimuth_deg = float(moon.az) * 180 / 3.1415926
        compass = get_compass_direction(azimuth_deg)

        # Convert to local time for display
        local_time = calc_time.replace(tzinfo=pytz.utc).astimezone(cst)
        time_str = local_time.strftime('%Y-%m-%d %H:%M %Z')

        above = "*" if altitude_deg > 0 else " "
        print(f"{time_str:<24} {altitude_deg:>+9.2f}° {azimuth_deg:>9.2f}°  {compass:<4} {above}")

    print(f"{'':->66}")
    print("  * = moon above horizon")

if __name__ == "__main__":
    main()
