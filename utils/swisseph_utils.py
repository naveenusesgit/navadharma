import swisseph as swe
from datetime import datetime
import pytz

swe.set_ephe_path("/usr/share/ephe")  # Optional: Set path to Swiss Ephemeris files

PLANETS = {
    0: "Sun", 1: "Moon", 2: "Mercury", 3: "Venus", 4: "Mars",
    5: "Jupiter", 6: "Saturn", 7: "Uranus", 8: "Neptune", 9: "Pluto"
}

def calculate_planet_positions(date_str, time_str, lat, lon):
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    utc_dt = pytz.timezone("Asia/Kolkata").localize(dt).astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60)

    planet_data = {}
    for i in PLANETS.keys():
        pos, _ = swe.calc_ut(jd, i)
        sign = int(pos[0] // 30)
        degree = round(pos[0] % 30, 2)
        planet_data[PLANETS[i]] = {"sign": sign + 1, "degree": degree}

    return planet_data
