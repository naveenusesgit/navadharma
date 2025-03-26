import swisseph as swe
from datetime import datetime
from pytz import timezone, utc
from utils.panchanga import get_timezone_name

# Basic exaltation sign mapping for demonstration
EXALTATION_SIGNS = {
    'Sun': 'Aries',
    'Moon': 'Taurus',
    'Mars': 'Capricorn',
    'Mercury': 'Virgo',
    'Jupiter': 'Cancer',
    'Venus': 'Pisces',
    'Saturn': 'Libra',
    'Rahu': 'Taurus',
    'Ketu': 'Scorpio',
}

PLANET_CODES = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
    'Ketu': swe.MEAN_NODE,
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_planetary_strength_swiss(datetime_str, lat, lon, tz_offset):
    dt = datetime.fromisoformat(datetime_str)
    tz = timezone(get_timezone_name(lat, lon))
    dt_local = tz.localize(dt).astimezone(utc)
    jd = swe.julday(dt_local.year, dt_local.month, dt_local.day, dt_local.hour + dt_local.minute / 60)

    results = {}
    for planet, code in PLANET_CODES.items():
        lon, _ = swe.calc_ut(jd, code)

        if planet == 'Ketu':
            # Ketu is 180° opposite to Rahu
            lon[0] = (lon[0] + 180) % 360

        sign_index = int(lon[0] // 30)
        sign = SIGNS[sign_index]

        # Example strength logic
        exalted = sign == EXALTATION_SIGNS.get(planet)
        score = 40 if exalted else 25 if sign_index % 2 == 0 else 20  # placeholder scoring

        results[planet] = {
            "longitude": round(lon[0], 2),
            "sign": sign,
            "score": score,
            "exalted": exalted
        }

    return results
