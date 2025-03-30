import swisseph as swe
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

# Set ephemeris path (update as needed)
swe.set_ephe_path('/usr/share/ephe')

# Use KP Ayanamsa
swe.set_sid_mode(swe.SIDM_USER, 0, 23.85675)  # True KP value

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
    'Ketu': swe.TRUE_NODE,
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_timezone_offset(lat, lon, year, month, day, hour, minute):
    tf = TimezoneFinder()
    tz_str = tf.timezone_at(lng=lon, lat=lat)
    tz = pytz.timezone(tz_str)
    dt = datetime(year, month, day, hour, minute)
    offset_sec = tz.utcoffset(dt).total_seconds()
    return offset_sec / 3600.0

def get_planet_positions(jd):
    positions = {}
    for name, pid in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, pid)
        positions[name] = round(lon, 4)
    return positions

def get_house_cusps(jd, lat, lon):
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    houses = {f'House_{i+1}': round(cusp, 4) for i, cusp in enumerate(cusps)}
    houses['Ascendant'] = round(ascmc[0], 4)
    return houses

def get_nakshatra_info(moon_long):
    segment = 13.333333
    idx = int(moon_long // segment)
    pada = int((moon_long % segment) // (segment / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[idx],
        "pada": pada
    }

def get_sub_lords(jd):
    sequence = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    years = [7, 20, 6, 10, 7, 18, 16, 19, 17]
    spans = [(p, 360 * y / 120) for p, y in zip(sequence, years)]

    sublords = {}
    for name, pid in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, pid)
        deg = lon % 360
        for i, (_, span) in enumerate(spans):
            deg -= span
            if deg <= 0:
                sublords[name] = sequence[i]
                break
    return sublords

def generate_kundli_chart(year, month, day, hour, minute, lat, lon):
    tz = get_timezone_offset(lat, lon, year, month, day, hour, minute)
    local_time = hour + (minute / 60)
    utc_time = local_time - tz
    jd = swe.julday(year, month, day, utc_time)

    positions = get_planet_positions(jd)
    moon_long = positions["Moon"]
    chart = {
        "ascendant": get_house_cusps(jd, lat, lon)["Ascendant"],
        "planet_positions": positions,
        "nakshatra": get_nakshatra_info(moon_long),
        "house_cusps": get_house_cusps(jd, lat, lon),
        "sub_lords": get_sub_lords(jd),
    }

    return {
        "chart": chart,
        "meta": {
            "julian_day": jd,
            "ayanamsa": round(swe.get_ayanamsa(jd), 6),
            "location": {
                "latitude": lat,
                "longitude": lon,
                "timezone": tz
            },
            "generated_at": datetime.utcnow().isoformat()
        }
    }
