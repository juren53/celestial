# Celestial

A collection of Python scripts for astronomical observation and tracking, calculated for Kansas City, Missouri using PyEphem and AstroQuery.

## Scripts

### Moon & Planets

| Script | Description |
|--------|-------------|
| `moon.py` | Moon phase, rise/set/transit times, and current altitude/azimuth |
| `moon_24h.py` | Moon altitude & azimuth forecast — hourly for the next 24 hours |
| `planets.py` | Position data for all major planets, Pluto, and the Moon |
| `mars.py` | Mars-specific observation data (rise/set, distance, magnitude, position) |

### Celestial Visibility

| Script | Description |
|--------|-------------|
| `celestial-visibility.py` | Visible celestial objects from KC on a given date |
| `celestial-visibility-1.py` | Alternate visibility calculation |
| `celestial-southern-visibility.py` | Southern sky object visibility |
| `celestial_objects.py` | Library for displaying info on galaxies, star clusters, and stars |

### Voyager Spacecraft Tracking

| Script | Description |
|--------|-------------|
| `voyager.py` | Class-based Voyager probe velocity and distance tracking |
| `Voyager-1.py` | Query Voyager 1 heliocentric position via JPL HORIZONS |
| `Voyager-1_b.py` | Voyager 1 geocentric position using Astropy |
| `voyager_from_kc.py` | Voyager 1 & 2 positions as seen from Kansas City |
| `voyager_from_kc-3.py` | Enhanced KC tracking with heliocentric velocity data |

### Utilities

| Script | Description |
|--------|-------------|
| `ephem_demo.py` | PyEphem library demo and educational reference |
| `celestial_info.py` | Display RA/Dec, physical characteristics, and visibility for objects |
| `query.py` | Command-line tool for querying celestial body information |

## Requirements

- Python 3
- [PyEphem](https://rhodesmill.org/pyephem/)
- [AstroQuery](https://astroquery.readthedocs.io/)
- [Astropy](https://www.astropy.org/)
- pytz

Install dependencies:

```bash
pip install ephem astroquery astropy pytz
```

## Usage

```bash
python3 moon.py          # Current moon info
python3 moon_24h.py      # 24-hour moon position forecast
python3 planets.py       # All planets overview
python3 mars.py          # Mars observation data
```

## Location

All observations default to Kansas City, Missouri (39.0997° N, 94.5786° W).
