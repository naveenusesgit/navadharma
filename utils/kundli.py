import swisseph as swe
import datetime
import pytz

swe.set_ephe_path('/usr/share/ephe')  # Adjust if needed for your server

# Mapping of planetary names to Swiss Ephemeris IDs
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
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10),
    ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)
]

def parse_datetime(datetime_str, timezone_offset):
    dt = datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
    local_dt = dt + datetime.timedelta(hours=timezone_offset)
    jd = swe.julday(local_dt.year, local_dt.month, local_dt.day, local_dt.hour + local_dt.minute / 60.0)
    return jd, local_dt

def get_planet_positions(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    positions = {}
    for name, pid in PLANET_IDS.items():
        lon_deg, _ = swe.calc_ut(jd, pid)
        positions[name] = f"{lon_deg:.2f}°"
    return {"positions": positions}

def get_lagna_info(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    lagna_deg = ascmc[0]
    rashis = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign = rashis[int(lagna_deg // 30)]
    return {
        "lagna": sign,
        "degree": f"{lagna_deg:.2f}°",
        "description": f"The Ascendant is in {sign} at {lagna_deg:.2f}°"
    }

def get_nakshatra_details(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nak_index = int(moon_long // (360 / 27))
    padam = int((moon_long % (360 / 27)) // 3.33) + 1
    return {
        "nakshatra": NAKSHATRAS[nak_index],
        "padam": f"Padam {padam}"
    }

def get_dasha_periods(datetime_str, lat, lon, tz):
    jd, local_dt = parse_datetime(datetime_str, tz)
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

    # First partial dasha
    dasha_end = current + datetime.timedelta(days=remaining_years * 365.25)
    dashas.append({
        "mahadasha": start_name,
        "start": current.strftime("%Y-%m-%d"),
        "end": dasha_end.strftime("%Y-%m-%d"),
        "antardashas": get_antardashas(current, remaining_years, start_name)
    })
    summary += f"Current Mahadasha: **{start_name}** ({current.strftime('%Y-%m-%d')} to {dasha_end.strftime('%Y-%m-%d')})\n"
    current = dasha_end
    years_used = remaining_years

    # Remaining dashas
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
        "summary": summary.strip(),
        "dashas": dashas
    }

def get_antardashas(start, years, maha_lord):
    sequence = [d[0] for d in DASHA_SEQUENCE]
    antars = []
    total_days = years * 365.25
    curr = start

    for antar_lord in sequence:
        antar_years = (dict(DASHA_SEQUENCE)[antar_lord] / 120) * years
        antar_days = antar_years * 365.25
        antar_end = curr + datetime.timedelta(days=antar_days)
        antars.append({
            "lord": antar_lord,
            "start": curr.strftime("%Y-%m-%d"),
            "end": antar_end.strftime("%Y-%m-%d")
        })
        curr = antar_end
    return antars

def get_kundli_chart(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    rashis = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    lagna_deg = ascmc[0]
    asc_sign = rashis[int(lagna_deg // 30)]

    house_signs = [rashis[int(deg // 30) % 12] for deg in cusps[1:]]
    planet_data = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        planet_data[name] = lon

    house_planets = {i+1: [] for i in range(12)}
    for name, lon in planet_data.items():
        house_index = next((i for i in range(11) if cusps[i+1] > lon >= cusps[i]), 11)
        house_planets[house_index + 1].append(f"{name} ({lon:.2f}°)")

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

def get_planetary_aspects(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    longs = {name: swe.calc_ut(jd, pid)[0] for name, pid in PLANET_IDS.items()}
    aspects = {}

    for p1 in longs:
        aspects[p1] = []
        for p2 in longs:
            if p1 == p2:
                continue
            angle = (longs[p2] - longs[p1]) % 360
            house_diff = round(angle / 30)

            if house_diff == 7:
                aspects[p1].append(f"{p2} (7th aspect)")
            if p1 == "Mars" and house_diff in [4, 8]:
                aspects[p1].append(f"{p2} ({house_diff}th aspect)")
            if p1 == "Jupiter" and house_diff in [5, 9]:
                aspects[p1].append(f"{p2} ({house_diff}th aspect)")
            if p1 == "Saturn" and house_diff in [3, 10]:
                aspects[p1].append(f"{p2} ({house_diff}th aspect)")
    return {"aspects": aspects}
