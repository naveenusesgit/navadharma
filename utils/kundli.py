import swisseph as swe
import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

swe.set_ephe_path('/usr/share/ephe')  # Adjust path if needed

def get_julian_day(date_str: str, time_str: str):
    dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

def get_location(place_name: str):
    geolocator = Nominatim(user_agent="kundli-generator")
    location = geolocator.geocode(place_name)
    if not location:
        raise Exception("Location not found")
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    offset_hours = datetime.datetime.now(datetime.timezone.utc).astimezone().utcoffset().total_seconds() / 3600
    return location.latitude, location.longitude, offset_hours

def get_planetary_positions(jd, lat, lon):
    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.TRUE_NODE,
        "Ketu": swe.MEAN_NODE
    }
    positions = {}
    for name, pid in planets.items():
        pos, _ = swe.calc_ut(jd, pid)
        positions[name] = round(pos[0], 2)
    return positions

def get_lagna(jd, lat, lon):
    ascendant = swe.houses(jd, lat, lon)[0][0]
    return round(ascendant, 2)

def get_divisional_chart(planet_positions, division):
    chart = {}
    for planet, deg in planet_positions.items():
        chart[planet] = int((deg * division) / 30) % 12 + 1
    return chart

def get_nakshatra(moon_deg):
    nakshatra_index = int(moon_deg / (360 / 27))
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshta", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    return nakshatras[nakshatra_index]

def generate_kundli_report(name: str, date: str, time: str, place: str):
    lat, lon, tz_offset = get_location(place)
    jd = get_julian_day(date, time)
    positions = get_planetary_positions(jd, lat, lon)
    lagna = get_lagna(jd, lat, lon)
    d1_chart = get_divisional_chart(positions, 1)
    d9_chart = get_divisional_chart(positions, 9)
    moon_deg = positions.get("Moon", 0)
    moon_nakshatra = get_nakshatra(moon_deg)

    return {
        "name": name,
        "date": date,
        "time": time,
        "place": place,
        "julian_day": jd,
        "lagna_degree": lagna,
        "nakshatra": moon_nakshatra,
        "planetary_positions": positions,
        "d1_chart": d1_chart,
        "d9_chart": d9_chart,
        "notes": "Generated with Swiss Ephemeris"
    }
