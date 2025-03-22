import swisseph as swe
import datetime
import pytz
from typing import Dict

swe.set_ephe_path('.')  # Set to ephemeris directory if needed

def get_julian_day(date_str: str, time_str: str, timezone="Asia/Kolkata"):
    dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    local = pytz.timezone(timezone).localize(dt)
    utc_dt = local.astimezone(pytz.utc)
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                      utc_dt.hour + utc_dt.minute / 60.0)

def get_planet_positions(jd: float, lat: float, lon: float) -> Dict[str, float]:
    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
        "Ketu": swe.TRUE_NODE,  # Ketu = 180° from Rahu
    }

    positions = {}
    for name, pid in planets.items():
        lon, _ = swe.calc_ut(jd, pid)[0:2]
        positions[name] = round(lon % 360, 2)

    # Ketu = Rahu + 180
    positions["Ketu"] = round((positions["Rahu"] + 180) % 360, 2)
    return positions

def get_divisional_chart(planet_positions: Dict[str, float], division: int) -> Dict[str, str]:
    """Returns the sign name for each planet in the specified divisional chart"""
    rasi_names = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    chart = {}
    for planet, lon in planet_positions.items():
        division_size = 30 / division
        division_number = int((lon % 30) / division_size)
        sign_index = (int(lon // 30) + division_number) % 12
        chart[planet] = rasi_names[sign_index]
    return chart

def determine_yogas(planet_positions: Dict[str, float]) -> list:
    yogas = []
    # Example: Gajakesari Yoga — Jupiter + Moon in kendra
    moon = planet_positions.get("Moon", 0)
    jupiter = planet_positions.get("Jupiter", 0)
    moon_house = int(moon // 30)
    jup_house = int(jupiter // 30)

    if abs((moon_house - jup_house) % 12) in [0, 4, 7, 10]:
        yogas.append("Gajakesari Yoga")

    # Mangal Dosha check — Mars in 1st, 4th, 7th, 8th, 12th
    mars_house = int(planet_positions.get("Mars", 0) // 30)
    if mars_house in [0, 3, 6, 7, 11]:
        yogas.append("Mangal Dosha")

    return yogas

def get_remedies(yogas: list, dasha: dict) -> list:
    remedies = []

    if "Mangal Dosha" in yogas:
        remedies.append("Perform Kumbh Vivah or Hanuman puja on Tuesdays.")
    if "Gajakesari Yoga" in yogas:
        remedies.append("Strengthen Jupiter by wearing yellow sapphire or donating books.")

    if dasha.get("mahadasha") == "Saturn":
        remedies.append("Chant Shani mantra on Saturdays to reduce Saturn effects.")

    return remedies

