#!/usr/bin/env python3
"""
voyager_from_kc.py - Calculate the position of Voyager 1 and Voyager 2 as viewed from Kansas City

This script uses the astroquery.jplhorizons module to query the JPL Horizons system
and determine the positions of the Voyager spacecraft in the sky when viewed from
Kansas City, Missouri. The script uses the New Horizons Observatory in Eudora, Kansas
(observatory code 735) as a proxy for Kansas City due to JPL Horizons location format requirements.

The script calculates rise, transit, and set times for each spacecraft over a 24-hour period.
It also prominently displays the real-time heliocentric velocity (relative to the Sun) for both spacecraft.
"""

import numpy as np
from astroquery.jplhorizons import Horizons
from datetime import datetime, timedelta
import pytz
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.time import Time

# Constants
AU_TO_KM = 149597870.7  # 1 Astronomical Unit in kilometers

def get_constellation(ra, dec):
    """Determine the constellation based on RA and Dec."""
    try:
        coord = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
        return coord.get_constellation()
    except Exception as e:
        print(f"Could not determine constellation: {e}")
        return "Unknown"

def format_ra_dec(ra, dec):
    """Format right ascension and declination in standard astronomical notation."""
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    ra_str = c.ra.to_string(unit=u.hour, sep='h ', pad=True, precision=1)
    dec_str = c.dec.to_string(sep='° ', pad=True, precision=1)
    return ra_str, dec_str

def find_rise_transit_set(times, altitudes):
    """
    Find rise, transit, and set times based on altitude data.
    
    Rise: Altitude crosses from negative to positive
    Transit: Altitude reaches maximum
    Set: Altitude crosses from positive to negative
    """
    rise_time = None
    transit_time = None
    set_time = None
    
    # Check if object ever rises above horizon
    if max(altitudes) <= 0:
        return None, None, None
    
    # Find rise time (when altitude crosses from negative to positive)
    for i in range(1, len(altitudes)):
        if altitudes[i-1] <= 0 and altitudes[i] > 0:
            # Linear interpolation to get more precise time
            t_diff = (times[i] - times[i-1]).total_seconds()
            alt_diff = altitudes[i] - altitudes[i-1]
            delta_t = t_diff * (0 - altitudes[i-1]) / alt_diff
            rise_time = times[i-1] + timedelta(seconds=delta_t)
            break
    
    # Find transit time (when altitude is maximum)
    if max(altitudes) > 0:
        max_alt_idx = np.argmax(altitudes)
        transit_time = times[max_alt_idx]
    
    # Find set time (when altitude crosses from positive to negative)
    for i in range(1, len(altitudes)):
        if altitudes[i-1] > 0 and altitudes[i] <= 0:
            # Linear interpolation to get more precise time
            t_diff = (times[i] - times[i-1]).total_seconds()
            alt_diff = altitudes[i] - altitudes[i-1]
            delta_t = t_diff * (0 - altitudes[i-1]) / alt_diff
            set_time = times[i-1] + timedelta(seconds=delta_t)
            break
    
    return rise_time, transit_time, set_time

def format_time(dt):
    """Format datetime to a readable local time string."""
    if dt is None:
        return "Not observable"
    
    # Convert to Kansas City time zone (US Central)
    central = pytz.timezone('US/Central')
    dt_central = dt.astimezone(central)
    return dt_central.strftime('%Y-%m-%d %H:%M:%S %Z')


def get_heliocentric_velocity(sc_id, epochs):
    """
    Retrieve the heliocentric velocity for a spacecraft from JPL Horizons.
    
    Args:
        sc_id (str): JPL Horizons spacecraft ID
        epochs (dict): Time specification for the query
        
    Returns:
        tuple: (vx, vy, vz, velocity_magnitude) velocity components and magnitude in km/s,
               or (None, None, None, None) if retrieval fails
    """
    try:
        # Query JPL Horizons for the spacecraft velocity relative to the Sun
        vec_table = Horizons(id=sc_id, location='@sun', epochs=epochs).vectors()
        
        # Extract velocity components
        vx = vec_table['VX'][0]  # X velocity component (km/s)
        vy = vec_table['VY'][0]  # Y velocity component (km/s)
        vz = vec_table['VZ'][0]  # Z velocity component (km/s)
        
        # Calculate velocity magnitude
        velocity_magnitude = np.sqrt(vx**2 + vy**2 + vz**2)
        
        return vx, vy, vz, velocity_magnitude
    except Exception as e:
        print(f"  Warning: Could not retrieve heliocentric velocity: {e}")
        return None, None, None, None

def main():
    # Using New Horizons Observatory (735) in Eudora, Kansas as proxy for Kansas City
    # This is close to Kansas City and is recognized by JPL Horizons
    location = "735"  # New Horizons Observatory code
    
    # Get current date and time
    now = datetime.now(pytz.utc)
    
    # Calculate positions over a 24-hour period at 15-minute intervals
    start_time = now
    stop_time = now + timedelta(days=1)
    
    # Create a time array for the 24-hour period
    step_minutes = 15
    num_steps = int(24 * 60 / step_minutes)
    times = [start_time + timedelta(minutes=i*step_minutes) for i in range(num_steps+1)]
    
    # Format dates for JPL Horizons
    epochs = {"start": start_time.strftime("%Y-%m-%d %H:%M"),
              "stop": stop_time.strftime("%Y-%m-%d %H:%M"),
              "step": f"{step_minutes}m"}
    
    # Spacecraft IDs for JPL Horizons
    spacecraft = {
        "Voyager 1": "-31",
        "Voyager 2": "-32"
    }
    
    print(f"Voyager Spacecraft Position and Velocity")
    print(f"Location: Kansas City area (New Horizons Observatory, Eudora, KS)")
    print(f"Date range: {start_time.strftime('%Y-%m-%d %H:%M')} to {stop_time.strftime('%Y-%m-%d %H:%M')} UTC")
    print("-" * 80)
    
    # Process each spacecraft
    for name, sc_id in spacecraft.items():
        print(f"\n{name}:")
        # For highlighting in the console output
        print(f"{'-' * 40}")
        
        try:
            # Query JPL Horizons for the spacecraft
            obj = Horizons(id=sc_id, location=location, epochs=epochs)
            eph = obj.ephemerides()
            
            # Get heliocentric velocity using the dedicated function
            vx, vy, vz, velocity_magnitude = get_heliocentric_velocity(sc_id, epochs)
            
            # Altitude data for rise/transit/set calculation
            altitudes = eph['EL'].data.data  # Elevation data
            
            # Convert JD dates to datetime objects
            jd_times = eph['datetime_jd']
            utc_times = Time(jd_times, format='jd').datetime
            utc_times = [t.replace(tzinfo=pytz.UTC) for t in utc_times]
            
            # Get the current position
            current_ra = eph['RA'][0]
            current_dec = eph['DEC'][0]
            current_alt = eph['EL'][0]
            current_az = eph['AZ'][0]
            
            # Get distance and light time information
            current_distance_au = eph['delta'][0]  # Distance in AU
            current_distance_km = current_distance_au * AU_TO_KM  # Distance in km
            current_light_time_min = eph['lighttime'][0]  # Light time in minutes
            current_light_time_hr = current_light_time_min / 60.0  # Light time in hours
            
            # Existing velocity calculation
            current_velocity_kms = eph['delta_rate'][0]  # Velocity in km/s
            moving_direction = "away from" if current_velocity_kms > 0 else "toward"
            ra_str, dec_str = format_ra_dec(current_ra, current_dec)
            
            # Get constellation
            constellation = get_constellation(current_ra, current_dec)
            
            # Calculate rise, transit, and set times
            rise_time, transit_time, set_time = find_rise_transit_set(utc_times, altitudes)
            
            # Display current position
            print(f"  Current position (at {format_time(utc_times[0])}):") 
            print(f"    Right Ascension: {ra_str}")
            print(f"    Declination: {dec_str}")
            print(f"    Constellation: {constellation}")
            print(f"    Altitude: {current_alt:.2f}°")
            print(f"    Azimuth: {current_az:.2f}°")
            print(f"    Distance: {current_distance_au:.2f} AU ({current_distance_km:.2f} km)")
            print(f"    Light time: {current_light_time_min:.2f} minutes ({current_light_time_hr:.2f} hours)")
            print(f"    Velocity relative to Earth: {abs(current_velocity_kms):.2f} km/s ({moving_direction} Earth)")
            
            # Velocity relative to Sun (if available)
            print(f"\n  HELIOCENTRIC VELOCITY (relative to Sun):")
            if velocity_magnitude is not None:
                print(f"    X component: {vx:.2f} km/s")
                print(f"    Y component: {vy:.2f} km/s")
                print(f"    Z component: {vz:.2f} km/s")
                print(f"    Total magnitude: {velocity_magnitude:.2f} km/s")
            else:
                print(f"    Could not retrieve heliocentric velocity data from JPL Horizons")
            
            # Display rise, transit, and set information
            print(f"\n  Viewing events in the next 24 hours:")
            
            if rise_time is None and transit_time is None and set_time is None:
                print(f"    {name} remains below the horizon during the entire period.")
            else:
                if rise_time:
                    print(f"    Rise: {format_time(rise_time)}")
                else:
                    print(f"    Rise: Not observed in this time period")
                    
                if transit_time:
                    # Find the maximum altitude at transit
                    max_alt_idx = np.argmax(altitudes)
                    transit_alt = altitudes[max_alt_idx]
                    print(f"    Transit: {format_time(transit_time)} (altitude: {transit_alt:.2f}°)")
                else:
                    print(f"    Transit: Not observed in this time period")
                    
                if set_time:
                    print(f"    Set: {format_time(set_time)}")
                else:
                    print(f"    Set: Not observed in this time period")
            
        except Exception as e:
            print(f"  Error retrieving data: {str(e)}")
    
    print("\nNote: Voyager spacecraft are extremely faint and would not be visible without very powerful telescope equipment,")
    print("      even when they are above the horizon. This calculation shows theoretical visibility only.")

if __name__ == "__main__":
    main()
