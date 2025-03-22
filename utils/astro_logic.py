import swisseph as swe
import datetime
from timezonefinder import TimezoneFinder
import pytz

swe.set_ephe_path('.')  # Use current dir or download Swiss Ephemeris data files

PLANETS = {
    0: 'Sun', 1: 'Moon', 2: 'Mars', 3: 'Mercury', 4: 'Jupiter',
    5: 'Venus', 6: 'Saturn', 7: 'Rahu', 8: 'Ketu'
}

NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashirsha', 'Ardra', 'Punarvasu',
    'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta',
    'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha',
    'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
    'Uttara Bhadrapada', 'Revati'
]

def get_timezone(place_name, lat, lon):
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lat=lat, lng=lon)
    return pytz.timezone(tz_str)

def get_julian_day(dt, timezone):
    local_dt = timezone.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)

def get_planet_positions(jd, lat, lon):
    positions = {}
    for i in PLANETS:
        if i == 7:  # Rahu
            planet_id = swe.MEAN_NODE
        elif i == 8:  # Ketu
            planet_id = swe.MEAN_NODE
        else:
            planet_id = i
        pos, _ = swe.calc_ut(jd, planet_id)
        name = PLANETS[i]
        positions[name] = pos[0] % 360
    return positions

def get_lagna(jd, lat, lon):
    asc, _, _ = swe.houses(jd, lat, lon, b'A')[0:3]
    return int(asc / 30) + 1  # 1 to 12

def get_nakshatra(moon_long):
    index = int(moon_long / (360 / 27))
    return NAKSHATRAS[index]

def detect_yogas(planets):
    yogas = []
    if 'Moon' in planets and 90 <= planets['Moon'] <= 120:
        yogas.append("Gajakesari Yoga")
    if 'Mars' in planets and planets['Mars'] > 200:
        yogas.append("Mangal Dosha")
    return yogas
