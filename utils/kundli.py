import swisseph as swe
import datetime
import pytz

swe.set_ephe_path('/usr/share/ephe')  # Update as needed

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
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17)
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
        lon_deg, _ = swe.calc_ut(jd, planet_id)
        positions[name] = f"{lon_deg:.2f}°"
    return {"positions": positions}

def get_lagna_info(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    cusps, ascmc = swe.houses(jd, latitude, longitude.encode(), b'P')
    lagna_deg = ascmc[0]
    lagna_sign_index = int(lagna_deg // 30)
    rashis = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    lagna_sign = rashis[lagna_sign_index]
    return {
        "lagna": lagna_sign,
        "description": f"The ascendant is in {lagna_sign}, at {lagna_deg:.2f}°"
    }

def get_nakshatra_details(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nak_index = int(moon_long // (360 / 27))
    padam = int((moon_long % (360 / 27)) // (3.33)) + 1
    nakshatra = NAKSHATRAS[nak_index]
    return {
        "nakshatra": nakshatra,
        "padam": f"Padam {padam}"
    }

def get_dasha_periods(datetime_str, latitude, longitude, timezone_offset):
    jd, local_dt = parse_datetime(datetime_str, timezone_offset)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)

    nak_index = int(moon_long // (360 / 27))
    nak_fraction = (moon_long % (360 / 27)) / (360 / 27)

    start_index = nak_index % 9
    start_name, start_years = DASHA_SEQUENCE[start_index]
    remaining_years = (1 - nak_fraction) * start_years

    dashas = []
    summary = ""

    current = local_dt
    dasha_pointer = start_index

    # Add first partial Mahadasha
    dasha_end = current + datetime.timedelta(days=remaining_years * 365.25)
    summary += f"Your current Mahadasha is **{start_name}**, lasting from **{current.strftime('%Y-%m-%d')}** to **{dasha_end.strftime('%Y-%m-%d')}**.\n\n"
    dashas.append({
        "mahadasha": start_name,
        "start": current.strftime("%Y-%m-%d"),
        "end": dasha_end.strftime("%Y-%m-%d"),
        "antardashas": get_antardashas(current, remaining_years, start_name)
    })
    current = dasha_end
    years_used = remaining_years

    # Add full Mahadashas
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

    summary += "Upcoming Mahadashas:\n"
    for d in dashas[1:3]:
        summary += f"- **{d['mahadasha']}**: {d['start']} to {d['end']}\n"

    return {
        "dashas": dashas,
        "summary": summary
    }

def get_antardashas(start_date, maha_years, maha_lord):
    antars = []
    total_days = maha_years * 365.25
    antar_order = [name for name, _ in DASHA_SEQUENCE]
    curr = start_date

    for antar_name in antar_order:
        antar_years = (dict(DASHA_SEQUENCE)[antar_name] / 120) * maha_years
        antar_days = antar_years * 365.25
        antar_end = curr + datetime.timedelta(days=antar_days)
        antars.append({
            "lord": antar_name,
            "start": curr.strftime("%Y-%m-%d"),
            "end": antar_end.strftime("%Y-%m-%d")
        })
        curr = antar_end
    return antars

def get_kundli_chart(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)

    rashis = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    # Get house cusps and lagna
    cusps, ascmc = swe.houses(jd, latitude, longitude.encode(), b'P')
    lagna_deg = ascmc[0]
    asc_sign = rashis[int(lagna_deg // 30)]

    # Get sign of each house cusp
    house_signs = []
    for cusp_deg in cusps[1:]:  # 1 to 12 (0 is unused)
        house_sign = rashis[int(cusp_deg // 30) % 12]
        house_signs.append(house_sign)

    # Get positions of all planets
    planet_data = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        planet_data[name] = lon

    # Assign planets to houses
    house_planets = {i+1: [] for i in range(12)}
    for name, lon in planet_data.items():
        house_index = next((i for i in range(11) if cusps[i+1] > lon >= cusps[i]), 11)
        house_planets[house_index + 1].append(f"{name} ({lon:.2f}°)")

    # Combine chart data
    chart = []
    for i in range(12):
        chart.append({
            "house": i + 1,
            "sign": house_signs[i],
            "planets": house_planets[i + 1]
        })

    return {
        "ascendant": {
            "sign": asc_sign,
            "degree": f"{lagna_deg:.2f}°"
        },
        "houses": chart
    }

def generate_full_prediction():
    return {
        "report": "Based on your chart, you are analytical, emotionally deep, and destined for transformation. Rahu is influencing your karmic path..."
    }

def generate_pdf_report():
    return {
        "pdf_url": "https://navadharma.onrender.com/static/kundli_report.pdf"
    }

def get_planetary_aspects(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    planet_longitudes = {}

    for name, planet_id in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, planet_id)
        planet_longitudes[name] = lon

    aspects = {}

    for planet in planet_longitudes:
        aspects[planet] = []

        for target in planet_longitudes:
            if planet == target:
                continue

            angle = (planet_longitudes[target] - planet_longitudes[planet]) % 360
            house_distance = round(angle / 30)

            # Default 7th aspect for all planets
            if house_distance == 7:
                aspects[planet].append(f"{target} (7th aspect)")

            # Mars: 4th and 8th
            if planet == "Mars" and house_distance in [4, 8]:
                aspects[planet].append(f"{target} ({house_distance}th aspect)")

            # Jupiter: 5th and 9th
            if planet == "Jupiter" and house_distance in [5, 9]:
                aspects[planet].append(f"{target} ({house_distance}th aspect)")

            # Saturn: 3rd and 10th
            if planet == "Saturn" and house_distance in [3, 10]:
                aspects[planet].append(f"{target} ({house_distance}th aspect)")

    return {"aspects": aspects}

def get_transit_predictions(datetime_str, latitude, longitude, timezone_offset):
    import pytz
    import math
    from datetime import datetime as dt

    jd_natal, local_dt = parse_datetime(datetime_str, timezone_offset)

    # 1. Get Lagna for proper house mapping
    cusps, ascmc = swe.houses(jd_natal, latitude, longitude.encode(), b'P')
    lagna_deg = ascmc[0]
    lagna_sign = int(lagna_deg // 30)

    # 2. Get Natal Planet Positions
    natal_positions = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd_natal, pid)
        natal_positions[name] = lon

    # 3. Get Transit Planet Positions (Today)
    now = dt.utcnow().replace(tzinfo=pytz.utc)
    jd_transit = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)

    transit_positions = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd_transit, pid)
        transit_positions[name] = lon

    # 4. Compute relative house transit (from Lagna)
    house_transits = {}
    rashis = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    for planet, lon in transit_positions.items():
        sign = int(lon // 30)
        rel_house = ((sign - lagna_sign) % 12) + 1
        house_transits[planet] = rel_house

    # 5. Generate predictions
    predictions = []
    remedies = []

    for planet, house in house_transits.items():
        if planet == "Jupiter":
            if house == 5:
                predictions.append("🟢 Jupiter is transiting your 5th house — Favorable for children, learning, and creative ventures.")
            elif house == 8:
                predictions.append("🔴 Jupiter in 8th — Watch out for spiritual detachment and inheritance matters.")
                remedies.append("🧘 Donate saffron or turmeric on Thursdays.")
        elif planet == "Saturn":
            if house == 7:
                predictions.append("🔴 Saturn in 7th — Test of partnerships and long-term relationships.")
                remedies.append("🧘 Chant Hanuman Chalisa every Tuesday.")
            elif house == 10:
                predictions.append("🟢 Saturn in 10th — Slow but steady career growth.")
        elif planet == "Rahu":
            if house == 1:
                predictions.append("🔴 Rahu in Lagna — Heightened desire and illusion; avoid impulsive decisions.")
                remedies.append("🧘 Chant Om Ram Rahave Namah for clarity.")
        elif planet == "Ketu":
            if house == 7:
                predictions.append("🔴 Ketu in 7th — Spiritualizing relationships or disconnection in marriage.")
                remedies.append("🧘 Meditate daily; avoid isolating yourself.")

    # 6. Aspect overlay (example: Saturn on Moon)
    moon_deg = natal_positions["Moon"]
    saturn_deg = transit_positions["Saturn"]
    angle = abs((saturn_deg - moon_deg) % 360)
    if angle < 10 or abs(angle - 180) < 10:
        predictions.append("🔴 Transit Saturn is strongly influencing your natal Moon — emotional pressure or isolation.")
        remedies.append("🧘 Fasting on Saturdays and lighting sesame oil lamp is advised.")

    if not predictions:
        predictions.append("🟢 Current transits suggest a balanced period with no major malefic influences.")

    return {
        "natal_positions": {k: f"{v:.2f}°" for k, v in natal_positions.items()},
        "transit_positions": {k: f"{v:.2f}°" for k, v in transit_positions.items()},
        "house_transits": {k: f"House {v}" for k, v in house_transits.items()},
        "predictions": predictions,
        "remedies": list(set(remedies)),
        "gpt_summary": "\n".join(predictions)
    }
