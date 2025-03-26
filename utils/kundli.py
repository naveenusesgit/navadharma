import swisseph as swe
import datetime
import pytz

swe.set_ephe_path('/usr/share/ephe')

PLANET_IDS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE, "Ketu": swe.TRUE_NODE
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

def parse_datetime(datetime_str, tz_offset):
    dt = datetime.datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
    local_dt = dt + datetime.timedelta(hours=tz_offset)
    jd = swe.julday(local_dt.year, local_dt.month, local_dt.day, local_dt.hour + local_dt.minute / 60.0)
    return jd, local_dt

def get_planet_positions(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    return {
        name: f"{swe.calc_ut(jd, pid)[0]:.2f}°"
        for name, pid in PLANET_IDS.items()
    }

def get_lagna_info(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    lagna_deg = ascmc[0]
    rashis = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return {
        "lagna": rashis[int(lagna_deg // 30)],
        "degree": f"{lagna_deg:.2f}°"
    }

def get_nakshatra_details(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    index = int(moon_long // (360 / 27))
    pada = int((moon_long % (360 / 27)) // 3.33) + 1
    return {
        "nakshatra": NAKSHATRAS[index],
        "padam": f"Padam {pada}"
    }

def get_dasha_periods(datetime_str, lat, lon, tz):
    jd, local_dt = parse_datetime(datetime_str, tz)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nak_index = int(moon_long // (360 / 27))
    nak_fraction = (moon_long % (360 / 27)) / (360 / 27)

    start_index = nak_index % 9
    start_name, start_years = DASHA_SEQUENCE[start_index]
    remaining_years = (1 - nak_fraction) * start_years
    dashas, curr = [], local_dt

    dasha_end = curr + datetime.timedelta(days=remaining_years * 365.25)
    dashas.append({
        "mahadasha": start_name, "start": curr.strftime("%Y-%m-%d"),
        "end": dasha_end.strftime("%Y-%m-%d"),
        "antardashas": get_antardashas(curr, remaining_years, start_name)
    })
    curr = dasha_end
    years_used = remaining_years
    pointer = start_index

    while years_used < 120:
        pointer = (pointer + 1) % 9
        name, years = DASHA_SEQUENCE[pointer]
        end = curr + datetime.timedelta(days=years * 365.25)
        dashas.append({
            "mahadasha": name,
            "start": curr.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
            "antardashas": get_antardashas(curr, years, name)
        })
        curr = end
        years_used += years

    return {
        "summary": f"Current Mahadasha: **{start_name}** until {dasha_end.strftime('%Y-%m-%d')}",
        "dashas": dashas
    }

def get_antardashas(start, years, lord):
    total = years * 365.25
    curr = start
    antars = []

    for antar in [d[0] for d in DASHA_SEQUENCE]:
        dur = (dict(DASHA_SEQUENCE)[antar] / 120) * years
        days = dur * 365.25
        end = curr + datetime.timedelta(days=days)
        antars.append({"lord": antar, "start": curr.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")})
        curr = end
    return antars

def get_kundli_chart(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    rashis = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    lagna_deg = ascmc[0]
    asc_sign = rashis[int(lagna_deg // 30)]
    house_signs = [rashis[int(c // 30) % 12] for c in cusps[1:]]
    planet_pos = {name: swe.calc_ut(jd, pid)[0] for name, pid in PLANET_IDS.items()}
    house_planets = {i+1: [] for i in range(12)}

    for p, lon in planet_pos.items():
        idx = next((i for i in range(11) if cusps[i+1] > lon >= cusps[i]), 11)
        house_planets[idx+1].append(f"{p} ({lon:.2f}°)")

    return {
        "ascendant": {"sign": asc_sign, "degree": f"{lagna_deg:.2f}°"},
        "houses": [{"house": i+1, "sign": house_signs[i], "planets": house_planets[i+1]} for i in range(12)]
    }

def get_transit_predictions(datetime_str, lat, lon, tz):
    jd, _ = parse_datetime(datetime_str, tz)
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    jd_transit = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    lagna_deg = ascmc[0]
    lagna_sign = int(lagna_deg // 30)

    natal = {p: swe.calc_ut(jd, pid)[0] for p, pid in PLANET_IDS.items()}
    transit = {p: swe.calc_ut(jd_transit, pid)[0] for p, pid in PLANET_IDS.items()}

    house_transits = {
        p: ((int(lon // 30) - lagna_sign) % 12) + 1 for p, lon in transit.items()
    }

    predictions = []
    for planet, house in house_transits.items():
        if planet == "Jupiter" and house == 5:
            predictions.append("🟢 Jupiter in 5th — Good for studies, kids, creativity.")
        elif planet == "Saturn" and house == 7:
            predictions.append("🔴 Saturn in 7th — Test of relationships.")
        elif planet == "Rahu" and house == 1:
            predictions.append("🔴 Rahu in Lagna — High ambitions, possible illusions.")

    return {
        "house_transits": house_transits,
        "predictions": predictions,
        "gpt_summary": "\n".join(predictions)
    }

def get_planetary_strength(datetime_str, lat, lon, tz):
    # Stubbed logic — You can plug in Shadbala calc later
    positions = get_planet_positions(datetime_str, lat, lon, tz)
    return {
        planet: {"strength": 20.0, "afflictions": []} for planet in positions
    }

def get_yoga_summary(datetime_str, lat, lon, tz):
    # Minimal sample
    return [
        {"name": "Raja Yoga", "active": True, "summary": "Promotes status and success."},
        {"name": "Daridra Yoga", "active": False}
    ]

def get_remedies(planet_status: dict, house_mapping: dict, lang="en"):
    results = []
    for planet, afflictions in planet_status.items():
        for aff in afflictions:
            if aff == "weak":
                results.append({
                    "reason": f"{planet} is weak",
                    "remedy": f"Chant mantra for {planet}, donate symbolic items."
                })
    return results

def get_kundli_summary(datetime_str, lat, lon, tz):
    lagna = get_lagna_info(datetime_str, lat, lon, tz)
    nakshatra = get_nakshatra_details(datetime_str, lat, lon, tz)
    dasha = get_dasha_periods(datetime_str, lat, lon, tz)
    strengths = get_planetary_strength(datetime_str, lat, lon, tz)
    transits = get_transit_predictions(datetime_str, lat, lon, tz)

    return {
        "lagna": lagna,
        "nakshatra": nakshatra,
        "dasha": dasha["summary"],
        "gpt_summary": transits["gpt_summary"]
    }
