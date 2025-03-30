import swisseph as swe
from datetime import datetime
from timezonefinder import TimezoneFinder
from pytz import timezone
import pytz

# Set Swiss Ephemeris path (adjust if needed)
swe.set_ephe_path('/usr/share/ephe')

# Planet mapping
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

# Vimshottari Dasha Years for KP (used for Sub Lord spans)
DASHA_YEARS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
}

NAKSHATRA_LORDS = [
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
] * 3  # 27 nakshatras

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_timezone_offset(year, month, day, hour, minute, lat, lng):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lng)
    local_tz = timezone(tz_name)
    dt = datetime(year, month, day, hour, minute)
    localized = local_tz.localize(dt, is_dst=None)
    offset = localized.utcoffset().total_seconds() / 3600
    return offset, tz_name

def get_ayanamsa(jd):
    return swe.get_ayanamsa(jd)

def get_planet_positions(jd):
    positions = {}
    for name, pid in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, pid)[0]
        positions[name] = round(lon % 360, 4)
    return positions

def get_house_cusps(jd, lat, lon):
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')  # Placidus
    return {
        f"House_{i+1}": round(cusp, 4)
        for i, cusp in enumerate(cusps)
    } | {
        "Ascendant": round(ascmc[0], 4)
    }

def get_nakshatra_and_pada(moon_longitude):
    segment = 13.333333
    total = moon_longitude % 360
    nak_index = int(total // segment)
    pada = int((total % segment) // (segment / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "nakshatra_lord": NAKSHATRA_LORDS[nak_index],
        "pada": pada
    }

def get_sublord_chain(degree):
    # Divide full zodiac proportionally based on Dasha spans
    total = 360
    chain = []
    def get_lord(pos, lords, levels=3):
        spans = [(lord, (DASHA_YEARS[lord] / 120) * total) for lord in lords]
        for _ in range(levels):
            for i, (lord, span) in enumerate(spans):
                if pos < span:
                    chain.append(lord)
                    # Now go deeper (divide this span)
                    pos = pos * 120 / DASHA_YEARS[lord]
                    spans = [(l, (DASHA_YEARS[l] / 120) * span) for l in lords]
                    break
        return chain

    return get_lord(degree % 360, list(DASHA_YEARS.keys()))

def get_kp_sub_lords(jd):
    sublords = {}
    for name, pid in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, pid)[0]
        chain = get_sublord_chain(lon)
        sublords[name] = {
            "star_lord": chain[0],
            "sub_lord": chain[1],
            "sub_sub_lord": chain[2]
        }
    return sublords

def generate_kundli_chart(year, month, day, hour, minute, lat, lon, system="kp"):
    # Auto-calculate timezone offset
    tz_offset, tz_name = get_timezone_offset(year, month, day, hour, minute, lat, lon)

    # Convert to UTC decimal hours
    decimal_hour = hour + (minute / 60.0) - tz_offset

    # Julian Day
    jd = swe.julday(year, month, day, decimal_hour)

    # Set KP Ayanamsa
    swe.set_sid_mode(swe.SIDM_USER, 0, 23.999)

    planet_positions = get_planet_positions(jd)
    moon_long = planet_positions["Moon"]

    return {
        "chart": {
            "planet_positions": planet_positions,
            "house_cusps": get_house_cusps(jd, lat, lon),
            "ascendant": round(swe.houses(jd, lat, lon, b'P')[1][0], 4),
            "nakshatra_details": get_nakshatra_and_pada(moon_long),
            "sub_lords": get_kp_sub_lords(jd)
        },
        "meta": {
            "system": system,
            "julian_day": jd,
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "timezone": tz_offset,
            "timezone_name": tz_name,
            "ayanamsa": round(get_ayanamsa(jd), 6),
            "generated_at": datetime.utcnow().isoformat()
        }
    }
