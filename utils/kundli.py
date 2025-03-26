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

def get_kundli_chart():
    return {
        "chart": "Kundli chart feature under development."
    }

def generate_full_prediction():
    return {
        "report": "Based on your chart, you are analytical, emotionally deep, and destined for transformation. Rahu is influencing your karmic path..."
    }

def generate_pdf_report():
    return {
        "pdf_url": "https://navadharma.onrender.com/static/kundli_report.pdf"
    }
