import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

geolocator = Nominatim(user_agent="kundli_app")
tz_finder = TimezoneFinder()

def get_coordinates(place):
    location = geolocator.geocode(place)
    if not location:
        raise ValueError("Place not found")
    return location.latitude, location.longitude

def get_timezone(lat, lon, dt):
    tz_name = tz_finder.timezone_at(lat=lat, lng=lon)
    if not tz_name:
        raise ValueError("Timezone not found")
    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt, tz_name

def get_planet_positions(julian_day):
    swe.set_ephe_path('/usr/share/ephe')  # Adjust path if needed
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,
        'Ketu': swe.TRUE_NODE  # Ketu = 180 deg from Rahu
    }

    positions = {}
    for name, planet in planets.items():
        lon, _ = swe.calc_ut(julian_day, planet)[0:2]
        if name == 'Ketu':
            lon = (lon + 180.0) % 360
        positions[name] = lon
    return positions

def get_nakshatra(lon):
    nakshatra_names = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashirsha',
        'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha',
        'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati',
        'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha',
        'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    nakshatra_index = int(lon / (13 + 1/3))
    return nakshatra_names[nakshatra_index % 27]

def get_lagna(julian_day, lat, lon):
    ascendant = swe.houses(julian_day, lat, lon)[0][0]
    return ascendant

def get_chart_data(name, date_str, time_str, place):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    lat, lon = get_coordinates(place)
    utc_dt, tz_name = get_timezone(lat, lon, dt)

    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)
    planet_positions = get_planet_positions(jd)
    ascendant = get_lagna(jd, lat, lon)
    moon_pos = planet_positions['Moon']
    nakshatra = get_nakshatra(moon_pos)

    return {
        "name": name,
        "date": date_str,
        "time": time_str,
        "place": place,
        "latitude": lat,
        "longitude": lon,
        "timezone": tz_name,
        "ascendant": ascendant,
        "nakshatra": nakshatra,
        "planets": planet_positions
    }

def get_dasha_report(name, date_str, time_str, place):
    # Placeholder for future Dasha logic
    return {
        "name": name,
        "dasha": "Dasha calculation not yet implemented"
    }

def get_nakshatra_info(name, date_str, time_str, place):
    data = get_chart_data(name, date_str, time_str, place)
    return {
        "name": data["name"],
        "nakshatra": data["nakshatra"],
        "moon_longitude": data["planets"]["Moon"]
    }

# Compatibility aliases for main.py imports
generate_kundli_report = get_chart_data
get_kundli_chart = get_chart_data
get_dasha_periods = get_dasha_report
