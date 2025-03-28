import swisseph as swe
from datetime import datetime, timedelta
from typing import Dict, Any, List
import os

swe.set_ephe_path('.')  # Set ephemeris path
swe.set_ayanamsa_mode(swe.AYANAMSA_KRISHNAMURTI)  # Use KP ayanamsa

NAKSHATRAS = [ ... ]  # Same as before
PLANETS = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.MEAN_NODE]

def get_julian_day(dt_str: str, tz: float) -> float:
    utc_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                      utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600 - tz)

def get_planet_positions(dt_str: str, lat: float, lon: float, tz: float) -> Dict[str, float]:
    jd = get_julian_day(dt_str, tz)
    positions = {}
    for p in PLANETS:
        lon_deg, _ = swe.calc_ut(jd, p)[0:2]
        positions[swe.get_planet_name(p)] = round(lon_deg % 360, 4)
    return positions

def get_nakshatra_and_pada(moon_longitude: float) -> Dict[str, Any]:
    nak_idx = int(moon_longitude // (360 / 27))
    pada = int((moon_longitude % (360 / 27)) // (360 / 108)) + 1
    return {"nakshatra": NAKSHATRAS[nak_idx], "padam": str(pada)}

def get_lagna(jd: float, lat: float, lon: float) -> Dict[str, Any]:
    asc = swe.houses_ex(jd, lat, lon, b'A')[0][0]
    return {"lagna_degree": round(asc, 2), "lagna_sign": get_zodiac_sign(asc)}

def get_zodiac_sign(deg: float) -> str:
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(deg // 30)]

def generate_kundli_chart(dt_str: str, lat: float, lon: float, tz: float) -> Dict[str, Any]:
    jd = get_julian_day(dt_str, tz)
    planet_pos = get_planet_positions(dt_str, lat, lon, tz)
    moon_lon = planet_pos.get("Moon", 0)
    nak = get_nakshatra_and_pada(moon_lon)
    asc = get_lagna(jd, lat, lon)
    return {"ascendant": asc, "planet_positions": planet_pos, "nakshatra_details": nak}

def get_dasha_periods(dt_str: str, tz: float) -> List[Dict[str, Any]]:
    jd = get_julian_day(dt_str, tz)
    dasha_list = []
    mahadasha = swe.dashainfo(jd)[1]
    for i in range(9):
        dasha = swe.dashainfo(jd + i * 365.25)[1]
        dasha_list.append({"mahadasha": dasha, "start": str(datetime.now() + timedelta(days=i*365)), "end": str(datetime.now() + timedelta(days=(i+1)*365))})
    return dasha_list

def get_remedies(grahas: Dict[str, float], lagna_sign: str) -> Dict[str, List[str]]:
    remedies = {
        "spiritual": [],
        "mantra": [],
        "donation": []
    }
    if "Saturn" in grahas and grahas["Saturn"] > 270:
        remedies["mantra"].append("Om Sham Shanicharaya Namaha")
        remedies["donation"].append("Donate black sesame on Saturday")
    if lagna_sign == "Scorpio":
        remedies["spiritual"].append("Practice Mars-related meditations")
    return remedies

def analyze_transits(natal: Dict[str, float]) -> Dict[str, Any]:
    today = datetime.utcnow()
    jd_now = swe.julday(today.year, today.month, today.day, today.hour + today.minute/60)
    transit_pos = {swe.get_planet_name(p): swe.calc_ut(jd_now, p)[0] for p in PLANETS}
    effects = []
    for planet, pos in transit_pos.items():
        if abs(pos[0] - natal.get(planet, 0)) < 5:
            effects.append(f"{planet} is closely transiting its natal position.")
    return {"transit_positions": transit_pos, "effects": effects}

def generate_summary(kundli_data: Dict[str, Any]) -> Dict[str, str]:
    moon_sign = get_zodiac_sign(kundli_data["planet_positions"]["Moon"])
    return {
        "summary": f"Your Moon sign is {moon_sign}. Favorable time for reflection.",
        "gpt_prompt": f"Analyze Kundli with Moon in {moon_sign}.",
        "dasha_score": 7.8
    }
