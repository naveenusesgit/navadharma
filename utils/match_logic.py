from utils.astro_logic import get_planet_positions, calculate_dasha, get_nakshatra
import swisseph as swe
import datetime

# Simplified Ashtakoot points system (scale: max 36)
NAKSHATRA_COMPATIBILITY = {
    ("Ashwini", "Bharani"): 5,
    ("Rohini", "Mrigashira"): 5,
    ("Pushya", "Ashlesha"): 4,
    ("Swati", "Chitra"): 5,
    ("Revati", "Uttara Bhadrapada"): 5,
    # Add more nakshatra pair scores
}

def get_jd(date_str, time_str):
    dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

def get_nakshatra_from_chart(jd, lat, lon):
    moon_lon, _, _ = swe.calc_ut(jd, swe.MOON)
    return get_nakshatra(moon_lon)

def calculate_ashtakoot_score(n1, n2):
    if (n1, n2) in NAKSHATRA_COMPATIBILITY:
        return NAKSHATRA_COMPATIBILITY[(n1, n2)]
    elif (n2, n1) in NAKSHATRA_COMPATIBILITY:
        return NAKSHATRA_COMPATIBILITY[(n2, n1)]
    else:
        return 2  # default score if pair not listed

def analyze_compatibility(person1, person2):
    jd1 = get_jd(person1["date"], person1["time"])
    jd2 = get_jd(person2["date"], person2["time"])

    lat1, lon1 = person1["lat"], person1["lon"]
    lat2, lon2 = person2["lat"], person2["lon"]

    # Get Nakshatra
    n1 = get_nakshatra_from_chart(jd1, lat1, lon1)
    n2 = get_nakshatra_from_chart(jd2, lat2, lon2)

    # Ashtakoot score (0–36 scale)
    ashtakoot_score = calculate_ashtakoot_score(n1, n2) * 4  # convert 0–9 to 0–36

    # Dasha analysis
    dasha1 = calculate_dasha(jd1)
    dasha2 = calculate_dasha(jd2)

    dasha_compatibility = (
        dasha1["mahadasha"] == dasha2["mahadasha"] or
        dasha1["antardasha"] == dasha2["antardasha"]
    )

    summary = {
        "ashtakootScore": ashtakoot_score,
        "nakshatra1": n1,
        "nakshatra2": n2,
        "dasha1": dasha1,
        "dasha2": dasha2,
        "dashaMatch": dasha_compatibility,
    }

    # Basic Remedies
    remedies = []
    if ashtakoot_score < 20:
        remedies.append("Consider chanting Parvati-Parameshwara mantras to strengthen bond.")
    if not dasha_compatibility:
        remedies.append("Perform Navagraha puja for better dasha alignment.")

    summary["remedies"] = remedies
    return summary
