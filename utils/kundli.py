import swisseph as swe
from datetime import datetime
import pytz
import math

# Set Ayanamsa to Krishnamurti (KP)
swe.set_ephe_path('/path/to/ephemeris')  # <-- 🔧 Replace with correct path
swe.set_ayanamsa_mode(swe.SIDM_KRISHNAMURTI)

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
    'Ketu': swe.TRUE_NODE  # or compute Ketu as 180° opposite Rahu
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def compute_julian_day(dt_str: str, tz_offset: float):
    dt = datetime.fromisoformat(dt_str)
    utc_dt = dt.astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                    utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600)
    return jd

def get_planet_positions(jd, lat, lon):
    positions = {}
    for name, pid in PLANETS.items():
        lon_deg, _ = swe.calc_ut(jd, pid)
        positions[name] = round(lon_deg[0], 4)
    return positions

def get_nakshatra(moon_long):
    nak_num = int(moon_long // (13 + 1/3))  # Each nakshatra = 13°20'
    pada = int((moon_long % (13 + 1/3)) // (13 + 1/3) * 4) + 1
    nakshatra = NAKSHATRAS[nak_num % 27]
    return nakshatra, pada

def get_lagna(jd, lat, lon):
    ascendant = swe.houses(jd, lat, lon)[0][0]  # Ascendant degree
    sign = int(ascendant // 30)
    sign_names = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
                  "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"]
    return {
        "degree": round(ascendant, 2),
        "sign": sign_names[sign % 12]
    }

def generate_kundli(datetime_str, latitude, longitude, timezone, place=''):
    jd = compute_julian_day(datetime_str, timezone)
    planet_positions = get_planet_positions(jd, latitude, longitude)
    lagna_info = get_lagna(jd, latitude, longitude)
    moon_long = planet_positions['Moon']
    nakshatra, pada = get_nakshatra(moon_long)

    return {
        "input": {
            "datetime": datetime_str,
            "lat": latitude,
            "lon": longitude,
            "tz": timezone,
            "place": place
        },
        "lagna": lagna_info,
        "moon": {
            "longitude": moon_long,
            "nakshatra": nakshatra,
            "pada": pada
        },
        "planet_positions": planet_positions
    }

# Example usage:
if __name__ == "__main__":
    birth_data = generate_kundli(
        datetime_str="1987-11-12T19:55:00",
        latitude=13.0827,
        longitude=80.2707,
        timezone=5.5,
        place="Chennai"
    )
    import json
    print(json.dumps(birth_data, indent=2))
