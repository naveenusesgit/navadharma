import swisseph as swe
from datetime import datetime, timedelta

# Set ephemeris path (or remove to use default)
swe.set_ephe_path('/usr/share/ephe')  # optional

# ✅ KP Ayanamsa: Use fixed value ~23.85675° (or updated to exact for date)
swe.set_sid_mode(swe.SIDM_USER, 0, 23.85675)

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

def get_julian_day(year, month, day, hour, minute, tz_offset):
    dt_local = datetime(year, month, day, hour, minute)
    dt_utc = dt_local - timedelta(hours=tz_offset)
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                      dt_utc.hour + dt_utc.minute / 60.0)

def get_planet_positions(jd):
    positions = {}
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    for name, pid in PLANETS.items():
        lon, lat, dist = swe.calc_ut(jd, pid, flags)[0]
        positions[name] = round(lon % 360, 4)
    return positions

def get_house_cusps(jd, latitude, longitude):
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    house_data = {f"House_{i+1}": round(cusp, 4) for i, cusp in enumerate(cusps)}
    house_data["Ascendant"] = round(ascmc[0], 4)
    return house_data

def get_nakshatra(moon_long):
    segment = 13.3333333333  # 13°20'
    nak_index = int((moon_long % 360) / segment)
    pada = int(((moon_long % segment) / (segment / 4)) + 1)
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": pada
    }

def generate_kundli_chart(jd, latitude, longitude, tz=5.5):
    planet_positions = get_planet_positions(jd)
    moon_long = planet_positions.get("Moon", 0.0)

    chart = {
        "planet_positions": planet_positions,
        "house_cusps": get_house_cusps(jd, latitude, longitude),
        "ascendant": get_house_cusps(jd, latitude, longitude).get("Ascendant"),
        "nakshatra_details": get_nakshatra(moon_long)
    }

    return {
        "chart": chart,
        "meta": {
            "system": "kp",
            "julian_day": jd,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "timezone": tz,
            "ayanamsa": round(swe.get_ayanamsa(jd), 6),
            "generated_at": datetime.utcnow().isoformat()
        }
    }
