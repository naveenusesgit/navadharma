import swisseph as swe
import datetime
import pytz

swe.set_ephe_path('/usr/share/ephe')  # Adjust path if needed

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
    jd = swe.julday(local_dt.year, local_dt.month, local_dt.day,
                    local_dt.hour + local_dt.minute / 60.0)
    return jd, local_dt

def get_planet_positions(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    swe.set_topo(longitude, latitude, 0)
    positions = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        positions[name] = f"{lon:.2f}°"
    return {"planet_positions": positions}

def get_lagna_info(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    lagna_deg = ascmc[0]
    rashis = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    lagna_sign = rashis[int(lagna_deg // 30)]
    return {
        "lagna": lagna_sign,
        "description": f"Lagna is in {lagna_sign} at {lagna_deg:.2f}°"
    }

def get_nakshatra_details(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nak_len = 13 + 20/60  # 13.333...
    nak_index = int(moon_long // nak_len)
    nakshatra = NAKSHATRAS[nak_index]
    pada = int((moon_long % nak_len) // (nak_len / 4)) + 1
    return {
        "nakshatra": nakshatra,
        "padam": f"Pada {pada}"
    }

def get_dasha_periods(datetime_str, latitude, longitude, timezone_offset):
    jd, local_dt = parse_datetime(datetime_str, timezone_offset)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    nak_len = 13 + 20/60
    nak_index = int(moon_long // nak_len)
    nak_fraction = (moon_long % nak_len) / nak_len

    start_index = nak_index % 9
    start_name, start_years = DASHA_SEQUENCE[start_index]
    remaining_years = (1 - nak_fraction) * start_years

    dashas = []
    summary = ""

    current = local_dt
    dasha_pointer = start_index

    dasha_end = current + datetime.timedelta(days=remaining_years * 365.25)
    summary += f"Current Mahadasha: **{start_name}** from {current.strftime('%Y-%m-%d')} to {dasha_end.strftime('%Y-%m-%d')}\n\n"
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
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    lagna_deg = ascmc[0]
    asc_sign = rashis[int(lagna_deg // 30)]

    house_signs = []
    for cusp_deg in cusps[1:]:
        house_sign = rashis[int(cusp_deg // 30) % 12]
        house_signs.append(house_sign)

    planet_data = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        planet_data[name] = lon

    house_planets = {i+1: [] for i in range(12)}
    for name, lon in planet_data.items():
        for i in range(11):
            if cusps[i] <= lon < cusps[i+1]:
                house_planets[i+1].append(f"{name} ({lon:.2f}°)")
                break
        else:
            house_planets[12].append(f"{name} ({lon:.2f}°)")

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

def get_planetary_strength(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    results = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        house = int(lon // 30) + 1
        afflictions = []
        if name in ["Moon", "Mars"] and house == 8:
            afflictions.append("Debilitated or under stress")
        results[name] = {
            "score": round((100 - abs(180 - lon) % 180) / 10, 2),
            "afflictions": afflictions,
            "house": house
        }
    return {"strengths": results}

def get_yogas(datetime_str, latitude, longitude, timezone_offset):
    jd, _ = parse_datetime(datetime_str, timezone_offset)
    planets = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd, pid)
        planets[name] = lon

    yogas = []

    # Example: Chandra-Mangal Yoga (Moon + Mars)
    if 0 < abs(planets["Moon"] - planets["Mars"]) < 30:
        yogas.append({
            "name": "Chandra-Mangal Yoga",
            "summary": "Moon and Mars are close, indicating business acumen and energy.",
            "active": True,
            "score": 8.5
        })

    # Example: Gajakesari Yoga (Moon + Jupiter in Kendra)
    moon_sign = int(planets["Moon"] // 30)
    jupiter_sign = int(planets["Jupiter"] // 30)
    if abs(moon_sign - jupiter_sign) in [0, 3, 6, 9]:
        yogas.append({
            "name": "Gajakesari Yoga",
            "summary": "Moon and Jupiter in Kendra creates wisdom and intelligence.",
            "active": True,
            "score": 9.0
        })

    return {
        "yogas": yogas
    }

def get_remedies(data):
    # Expects dict input: planetaryStatus, houseMapping, lang
    lang = data.get("lang", "en")
    planetary_status = data.get("planetaryStatus", {})
    house_mapping = data.get("houseMapping", {})

    spiritual = []
    mantras = []
    donations = []

    if "Saturn" in planetary_status and "afflicted" in planetary_status["Saturn"]:
        spiritual.append("Visit Hanuman temple on Saturdays")
        mantras.append("Om Sham Shanicharaya Namah")
        donations.append("Donate black sesame seeds")

    if house_mapping.get("8") == "Mars":
        spiritual.append("Perform Mangal Shanti Puja")
        mantras.append("Om Mangalaya Namah")
        donations.append("Donate red lentils on Tuesdays")

    return {
        "spiritual": spiritual,
        "mantra": mantras,
        "donation": donations
    }

def get_transits(datetime_str, latitude, longitude, timezone_offset):
    jd_now, _ = parse_datetime(datetime_str, timezone_offset)
    # natal positions from birth chart (reuse `get_planet_positions`)
    natal = get_planet_positions(datetime_str, latitude, longitude, timezone_offset)["planet_positions"]

    # current transit positions
    swe.set_topo(longitude, latitude, 0)
    transit = {}
    for name, pid in PLANET_IDS.items():
        lon, _ = swe.calc_ut(jd_now, pid)
        transit[name] = f"{lon:.2f}°"

    predictions = []
    remedies = []

    # Simple example rule: Saturn transit over natal Moon
    natal_moon = float(natal["Moon"].replace("°", ""))
    saturn_transit = float(transit["Saturn"].replace("°", ""))

    if abs(saturn_transit - natal_moon) < 15:
        predictions.append("You are under Sade Sati. Emotional turbulence possible.")
        remedies.append("Chant Hanuman Chalisa on Saturdays.")

    return {
        "natal_positions": natal,
        "transit_positions": transit,
        "house_transits": {},  # Can be added using `swe.houses`
        "predictions": predictions,
        "remedies": remedies,
        "gpt_summary": "Sade Sati is active. Emotional introspection and discipline are advised."
    }
