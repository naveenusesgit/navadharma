import swisseph as swe
import datetime
import pytz

# Set path to Swiss Ephemeris
swe.set_ephe_path('/usr/share/ephe')

PLANET_IDS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": swe.TRUE_NODE
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

RASHIS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

DASHA_SEQUENCE = [
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10),
    ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
]

# 🌐 Parse timezone-aware datetime and compute Julian Day
def parse_datetime(datetime_str, timezone_offset):
    dt = datetime.datetime.fromisoformat(datetime_str)
    local_dt = dt + datetime.timedelta(hours=timezone_offset)
    jd = swe.julday(local_dt.year, local_dt.month, local_dt.day,
                    local_dt.hour + local_dt.minute / 60.0)
    return jd, local_dt

# 🌙 Get Moon Rāśi, Nakshatra, Padam
def get_nakshatra_details(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    swe.set_topo(longitude, latitude, 0)

    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    rashis_index = int(moon_long // 30)
    nak_index = int(moon_long // (360 / 27))
    padam = int((moon_long % (360 / 27)) // (360 / 108)) + 1

    return {
        "moon_longitude": round(moon_long, 2),
        "rasi": RASHIS[rashis_index],
        "nakshatra": NAKSHATRAS[nak_index],
        "padam": f"Padam {padam}"
    }

# 🔺 Get Lagna sign and degree
def get_lagna_info(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    swe.set_topo(longitude, latitude, 0)

    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    lagna_deg = ascmc[0]
    lagna_sign_index = int(lagna_deg // 30)
    return {
        "lagna": RASHIS[lagna_sign_index],
        "degree": round(lagna_deg, 2)
    }

# 🌞 Get planetary longitudes
def get_planet_positions(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    swe.set_topo(longitude, latitude, 0)

    positions = {}
    for planet, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        positions[planet] = f"{round(lon, 2)}°"
    return {"planet_positions": positions}

# 🔀 Get Dasha periods from Moon position
def get_dasha_periods(datetime_str, latitude, longitude, timezone_offset):
    jd, local_dt = parse_datetime(datetime_str, timezone_offset)
    swe.set_topo(longitude, latitude, 0)

    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nak_index = int(moon_long // (360 / 27))
    nak_fraction = (moon_long % (360 / 27)) / (360 / 27)

    start_index = nak_index % 9
    start_name, start_years = DASHA_SEQUENCE[start_index]
    remaining_years = (1 - nak_fraction) * start_years

    dashas = []
    current = local_dt
    dasha_pointer = start_index

    for i in range(10):  # Max 10 dashas
        name, years = DASHA_SEQUENCE[dasha_pointer % 9]
        duration = years if i != 0 else remaining_years
        end = current + datetime.timedelta(days=duration * 365.25)
        dashas.append({
            "mahadasha": name,
            "start": current.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")
        })
        current = end
        dasha_pointer += 1

    return {"dashas": dashas}

# 🛠️ Combine all into full prediction report
def generate_full_prediction(datetime_str, latitude, longitude, timezone_offset):
    return {
        "lagna": get_lagna_info(datetime_str, latitude, longitude, timezone_offset),
        "nakshatra": get_nakshatra_details(datetime_str, latitude, longitude, timezone_offset),
        "planets": get_planet_positions(datetime_str, latitude, longitude, timezone_offset),
        "dasha": get_dasha_periods(datetime_str, latitude, longitude, timezone_offset)
    }
