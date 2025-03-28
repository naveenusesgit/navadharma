import swisseph as swe
import datetime
import pytz
import math

swe.set_ephe_path('/usr/share/ephe')  # Adjust if needed

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

DASHA_SEQUENCE = [
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
    ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
]

def parse_datetime(datetime_str, timezone_offset):
    dt = datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
    local_dt = dt + datetime.timedelta(hours=timezone_offset)
    jd = swe.julday(local_dt.year, local_dt.month, local_dt.day, local_dt.hour + local_dt.minute / 60.0)
    return jd, local_dt

def get_planet_positions(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    positions = {}
    for name, planet_id in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, planet_id)
        positions[name] = f"{lon:.2f}°"
    return {"planet_positions": positions}

def get_lagna_info(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    lagna_deg = ascmc[0]
    sign_index = int(lagna_deg // 30)
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return {
        "lagna": signs[sign_index],
        "description": f"Lagna is in {signs[sign_index]} at {lagna_deg:.2f}°"
    }

def get_nakshatra_details(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    segment = 360 / 27
    nak_index = int(moon_long // segment)
    padam = int((moon_long % segment) // (segment / 4)) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "padam": f"Pada {padam}"
    }

def get_dasha_periods(datetime_str, latitude, longitude, timezone_offset):
    jd, local_dt = parse_datetime(datetime_str, timezone_offset)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    segment = 360 / 27
    nak_index = int(moon_long // segment)
    nak_fraction = (moon_long % segment) / segment

    start_index = nak_index % 9
    start_name, start_years = DASHA_SEQUENCE[start_index]
    remaining_years = (1 - nak_fraction) * start_years

    current = local_dt
    dashas = []
    dasha_pointer = start_index

    # Initial Mahadasha
    dasha_end = current + datetime.timedelta(days=remaining_years * 365.25)
    dashas.append({
        "mahadasha": start_name,
        "start": current.strftime("%Y-%m-%d"),
        "end": dasha_end.strftime("%Y-%m-%d"),
        "antardashas": get_antardashas(current, remaining_years, start_name)
    })
    current = dasha_end
    years_used = remaining_years

    while years_used < 120:
        dasha_pointer = (dasha_pointer + 1) % 9
        name, years = DASHA_SEQUENCE[dasha_pointer]
        dasha_end = current + datetime.timedelta(days=years * 365.25)
        dashas.append({
            "mahadasha": name,
            "start": current.strftime("%Y-%m-%d"),
            "end": dasha_end.strftime("%Y-%m-%d"),
            "antardashas": get_antardashas(current, years, name)
        })
        current = dasha_end
        years_used += years

    return {
        "dashas": dashas,
        "summary": f"Current Mahadasha: {start_name} (ends {dashas[0]['end']})"
    }

def get_antardashas(start_date, maha_years, maha_lord):
    total_days = maha_years * 365.25
    antar_order = [x[0] for x in DASHA_SEQUENCE]
    current = start_date
    antars = []

    for antar in antar_order:
        antar_years = (dict(DASHA_SEQUENCE)[antar] / 120) * maha_years
        antar_days = antar_years * 365.25
        end = current + datetime.timedelta(days=antar_days)
        antars.append({
            "lord": antar,
            "start": current.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")
        })
        current = end
    return antars

def get_kundli_chart(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    rashis = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    lagna_deg = ascmc[0]
    asc_sign = rashis[int(lagna_deg // 30)]

    house_signs = [rashis[int(deg // 30) % 12] for deg in cusps[1:]]

    planet_longs = {name: swe.calc_ut(jd, pid)[0] for name, pid in PLANET_IDS.items()}
    house_planets = {i + 1: [] for i in range(12)}

    for name, lon in planet_longs.items():
        for i in range(12):
            if i == 11 or (cusps[i + 1] > lon >= cusps[i]):
                house_planets[i + 1].append(f"{name} ({lon:.2f}°)")
                break

    return {
        "ascendant": {"sign": asc_sign, "degree": f"{lagna_deg:.2f}°"},
        "houses": [
            {"house": i + 1, "sign": house_signs[i], "planets": house_planets[i + 1]}
            for i in range(12)
        ]
    }

def get_transit_predictions(datetime_str, latitude, longitude, timezone_offset):
    jd_natal, _ = parse_datetime(datetime_str, timezone_offset)
    cusps, ascmc = swe.houses(jd_natal, latitude, longitude, b'P')
    lagna_sign = int(ascmc[0] // 30)

    natal = {k: swe.calc_ut(jd_natal, v)[0] for k, v in PLANET_IDS.items()}
    now = datetime.datetime.utcnow()
    jd_now = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)
    transit = {k: swe.calc_ut(jd_now, v)[0] for k, v in PLANET_IDS.items()}

    house_transits = {
        k: ((int(lon // 30) - lagna_sign) % 12) + 1 for k, lon in transit.items()
    }

    predictions = []
    remedies = []

    if house_transits.get("Saturn") == 7:
        predictions.append("🔴 Saturn in 7th house — challenges in partnerships.")
        remedies.append("🔹 Read Hanuman Chalisa on Saturdays.")

    if house_transits.get("Jupiter") == 5:
        predictions.append("🟢 Jupiter in 5th — growth in education and children.")
        remedies.append("🔹 Donate turmeric on Thursdays.")

    return {
        "natal_positions": {k: f"{v:.2f}°" for k, v in natal.items()},
        "transit_positions": {k: f"{v:.2f}°" for k, v in transit.items()},
        "house_transits": {k: f"House {v}" for k, v in house_transits.items()},
        "predictions": predictions,
        "remedies": list(set(remedies)),
        "gpt_summary": "\n".join(predictions)
    }

def get_planetary_aspects(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    longs = {k: swe.calc_ut(jd, v)[0] for k, v in PLANET_IDS.items()}
    aspects = {}

    for planet, p_deg in longs.items():
        aspects[planet] = []
        for target, t_deg in longs.items():
            if planet == target: continue
            angle = abs((t_deg - p_deg) % 360)
            house_dist = round(angle / 30)
            if house_dist == 7:
                aspects[planet].append(f"{target} (7th aspect)")
            elif planet == "Mars" and house_dist in [4, 8]:
                aspects[planet].append(f"{target} ({house_dist}th aspect)")
            elif planet == "Jupiter" and house_dist in [5, 9]:
                aspects[planet].append(f"{target} ({house_dist}th aspect)")
            elif planet == "Saturn" and house_dist in [3, 10]:
                aspects[planet].append(f"{target} ({house_dist}th aspect)")
    return {"aspects": aspects}

def get_planetary_strength(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    strength = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        score = round(math.sin(math.radians(lon)) * 10 + 10, 2)
        strength[name] = {
            "score": score,
            "afflictions": ["combust"] if score < 6 else [],
            "house": int(lon // 30) + 1
        }
    return strength

def generate_pdf_report():
    return {
        "pdf_url": "https://navadharma.onrender.com/static/kundli_report.pdf"
    }

def generate_full_summary():
    return {
        "summary": "You are in the Jupiter Mahadasha — a time for wisdom, growth, and higher learning.",
        "gpt_prompt": "Summarize Kundli based on Jupiter Mahadasha, lagna in Cancer, and Moon in Pushya.",
        "dasha_score": 8.1,
        "context": {
            "mahadasha": "Jupiter",
            "nakshatra": "Pushya",
            "lagna": "Cancer"
        }
    }
