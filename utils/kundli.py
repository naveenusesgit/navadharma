import swisseph as swe
from datetime import datetime, timedelta

# KP Ayanamsa offset in degrees for 1987; refine if needed per year
KP_AYANAMSA_OFFSET = 23.856

# Set the ephemeris path and KP ayanamsa
swe.set_ephe_path('/usr/share/ephe')
swe.set_sid_mode(swe.SIDM_USER, 0, KP_AYANAMSA_OFFSET)

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

def compute_julian_day(year, month, day, hour, minute, tz_offset):
    dt_local = datetime(year, month, day, hour, minute)
    dt_utc = dt_local - timedelta(hours=tz_offset)
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                      dt_utc.hour + dt_utc.minute / 60.0)

def get_planet_positions(jd):
    positions = {}
    for name, pid in PLANETS.items():
        lon, _, _ = swe.calc_ut(jd, pid)
        positions[name] = round(lon % 360, 4)
    return positions

def get_lagna(jd, latitude, longitude):
    _, ascmc = swe.houses(jd, latitude, longitude, b'P')
    return round(ascmc[0] % 360, 4)

def get_nakshatra_and_pada(moon_long):
    seg = 13.333333
    moon_long %= 360
    nak_index = int(moon_long // seg)
    pada = int((moon_long % seg) // (seg / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": pada
    }

def get_house_cusps(jd, latitude, longitude):
    cusps, _ = swe.houses(jd, latitude, longitude, b'P')
    return {f"House_{i+1}": round(cusp, 4) for i, cusp in enumerate(cusps)}

def generate_kundli_chart(jd, latitude, longitude, tz=5.5):
    planet_positions = get_planet_positions(jd)
    lagna = get_lagna(jd, latitude, longitude)
    moon_long = planet_positions["Moon"]
    nak_details = get_nakshatra_and_pada(moon_long)
    house_cusps = get_house_cusps(jd, latitude, longitude)
    ayanamsa = swe.get_ayanamsa_ut(jd)

    return {
        "chart": {
            "planet_positions": planet_positions,
            "ascendant": lagna,
            "nakshatra_details": nak_details,
            "house_cusps": house_cusps
        },
        "meta": {
            "system": "kp",
            "julian_day": jd,
            "ayanamsa": round(ayanamsa, 6),
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "timezone": tz,
            "generated_at": datetime.utcnow().isoformat()
        }
    }
