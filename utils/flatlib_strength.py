from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.const import SUN, MOON, MARS, MERCURY, JUPITER, VENUS, SATURN, RAHU, KETU
from flatlib import aspects, ephem
import pytz

PLANETS = [SUN, MOON, MARS, MERCURY, JUPITER, VENUS, SATURN]

def get_flatlib_chart(datetime_str, latitude, longitude, timezone_offset):
    dt = Datetime(datetime_str, 'UTC')
    dt.setOffset(timezone_offset)
    return Chart(dt, location=(latitude, longitude))

def get_planetary_strength_flatlib(datetime_str, latitude, longitude, timezone_offset):
    chart = get_flatlib_chart(datetime_str, latitude, longitude, timezone_offset)

    strength_scores = {}
    for planet in PLANETS:
        obj = chart.get(planet)

        # Calculate essential dignity strength
        dignity = obj.dignity()
        dig_score = {
            'EXALT': 30,
            'DOMICILE': 25,
            'DETRIMENT': 10,
            'FALL': 5,
            'NEUTRAL': 15
        }.get(dignity, 15)

        # Check if retrograde
        retro_score = 10 if obj.isRetrograde() and planet in [MARS, SATURN, JUPITER] else 5

        # Approximate total strength
        total = (dig_score + retro_score)  # Out of ~40
        strength_scores[planet] = round(total, 2)

    return strength_scores
