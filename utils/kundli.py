import swisseph as swe
import datetime
import pytz

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
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

RASHIS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

DASHA_SEQUENCE = [
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
    ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
]

# ---------- Utilities ----------
def parse_datetime(datetime_str, tz_offset):
    dt = datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
    local_dt = dt + datetime.timedelta(hours=tz_offset)
    jd = swe.julday(local_dt.year, local_dt.month, local_dt.day, local_dt.hour + local_dt.minute / 60.0)
    return jd, local_dt

# ---------- Core Functions ----------
def get_planet_positions(datetime_str, latitude, longitude, timezone):
    jd, _ = parse_datetime(datetime_str, timezone)
    positions = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        positions[name] = f"{lon:.2f}°"
    return {"planet_positions": positions}

def get_lagna_info(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    lagna_deg = ascmc[0]
    lagna_sign = RASHIS[int(lagna_deg // 30)]
    return {
        "lagna": lagna_sign,
        "description": f"Lagna is in {lagna_sign} at {lagna_deg:.2f}°"
    }

def get_nakshatra_details(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nak_index = int(moon_long // (360 / 27))
    pada = int((moon_long % (360 / 27)) // (3.33)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "padam": f"Padam {pada}"
    }

# ---------- Dasha ----------
def get_dasha_periods(datetime_str, lat, lon, tz):
    jd, local_dt = parse_datetime(datetime_str, tz)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nak_index = int(moon_long // (360 / 27))
    fraction = (moon_long % (360 / 27)) / (360 / 27)

    pointer = nak_index % 9
    start_name, start_years = DASHA_SEQUENCE[pointer]
    rem_years = (1 - fraction) * start_years

    dashas = []
    current = local_dt
    summary = f"🌟 Current Mahadasha: **{start_name}**\n\n"

    for _ in range(9):
        name, years = DASHA_SEQUENCE[pointer]
        end = current + datetime.timedelta(days=years * 365.25)
        dashas.append({
            "mahadasha": name,
            "start": current.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
            "antardashas": get_antardashas(current, years, name)
        })
        current = end
        pointer = (pointer + 1) % 9

    summary += f"📅 Upcoming: {dashas[1]['mahadasha']} → {dashas[1]['start']} to {dashas[1]['end']}"
    return {"dashas": dashas, "summary": summary}

def get_antardashas(start_date, maha_years, maha_lord):
    antars = []
    total_days = maha_years * 365.25
    order = [name for name, _ in DASHA_SEQUENCE]
    curr = start_date
    for antar in order:
        antar_days = (dict(DASHA_SEQUENCE)[antar] / 120) * total_days
        end = curr + datetime.timedelta(days=antar_days)
        antars.append({
            "lord": antar,
            "start": curr.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")
        })
        curr = end
    return antars

# ---------- Aspects ----------
def get_planetary_aspects(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    longitudes = {}
    for name, pid in PLANET_IDS.items():
        lon_deg, _ = swe.calc_ut(jd, pid)
        longitudes[name] = lon_deg

    aspects = {}
    for planet in longitudes:
        aspects[planet] = []
        for target in longitudes:
            if planet == target: continue
            angle = (longitudes[target] - longitudes[planet]) % 360
            house_distance = round(angle / 30)

            if house_distance == 7:
                aspects[planet].append(f"{target} (7th aspect)")
            elif planet == "Mars" and house_distance in [4, 8]:
                aspects[planet].append(f"{target} ({house_distance}th aspect)")
            elif planet == "Jupiter" and house_distance in [5, 9]:
                aspects[planet].append(f"{target} ({house_distance}th aspect)")
            elif planet == "Saturn" and house_distance in [3, 10]:
                aspects[planet].append(f"{target} ({house_distance}th aspect)")
    return {"aspects": aspects}

# ---------- Planetary Strength ----------
def get_planetary_strength(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    strengths = {}
    for name, pid in PLANET_IDS.items():
        lon_deg, _ = swe.calc_ut(jd, pid)
        strength = round((lon_deg % 30) / 30, 2)
        strengths[name] = {
            "score": strength * 10,
            "house": int(lon_deg // 30) + 1,
            "afflictions": ["Combustion"] if strength < 2 else []
        }
    return strengths

# ---------- Transits ----------
def get_transit_predictions(datetime_str, lat, lon, tz):
    from datetime import datetime as dt
    jd_birth, _ = parse_datetime(datetime_str, tz)

    natal = {}
    for name, pid in PLANET_IDS.items():
        lon_deg, _ = swe.calc_ut(jd_birth, pid)
        natal[name] = lon_deg

    now = dt.utcnow().replace(tzinfo=pytz.utc)
    jd_now = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)

    transit = {}
    for name, pid in PLANET_IDS.items():
        lon_deg, _ = swe.calc_ut(jd_now, pid)
        transit[name] = lon_deg

    house_transits = {}
    lagna_sign = int(swe.houses(jd_birth, lat, lon, b'P')[1][0] // 30)
    for name, lon in transit.items():
        sign = int(lon // 30)
        rel_house = ((sign - lagna_sign) % 12) + 1
        house_transits[name] = rel_house

    # Mock prediction logic
    predictions = [f"{p} in house {h}" for p, h in house_transits.items()]
    return {
        "natal_positions": {k: f"{v:.2f}°" for k, v in natal.items()},
        "transit_positions": {k: f"{v:.2f}°" for k, v in transit.items()},
        "house_transits": {k: f"House {v}" for k, v in house_transits.items()},
        "predictions": predictions,
        "remedies": ["Chant Hanuman Chalisa", "Donate wheat"],
        "gpt_summary": "⚠️ Saturn's transit may test patience. Favorable time for education & research."
    }

# ---------- Yogas ----------
def get_yogas(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    sun_long, _ = swe.calc_ut(jd, swe.SUN)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)

    yogas = []
    if abs(sun_long - moon_long) < 12:
        yogas.append({"name": "Amavasya Yoga", "active": True, "summary": "New Moon influence", "score": 8.5})

    return {"yogas": yogas}

# ---------- Remedies ----------
def get_remedies(planetaryStatus, houseMapping, lang="en"):
    return {
        "spiritual": ["Meditate daily", "Perform Surya Namaskar"],
        "mantra": ["Om Namah Shivaya", "Om Namo Narayanaya"],
        "donation": ["Donate rice on Mondays", "Feed cows on Fridays"]
    }

# ---------- Summary Generator ----------
def generate_summary(datetime_str, lat, lon, tz, goal="general"):
    lagna = get_lagna_info(datetime_str, lat, lon, tz)["lagna"]
    nakshatra = get_nakshatra_details(datetime_str, lat, lon, tz)["nakshatra"]
    dasha = get_dasha_periods(datetime_str, lat, lon, tz)["dashas"][0]["mahadasha"]

    prompt = f"The user is under {dasha} Mahadasha with Lagna in {lagna} and Nakshatra {nakshatra}. Goal is {goal}."
    return {
        "summary": f"Lagna in {lagna}, under {dasha} Mahadasha. Good period for {goal}.",
        "gpt_prompt": prompt,
        "dasha_score": 7.5,
        "context": {
            "nakshatra": nakshatra,
            "mahadasha": dasha,
            "lagna": lagna
        }
    }
