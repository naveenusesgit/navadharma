import swisseph as swe
import datetime
from utils.helpers import get_planetary_positions, get_house_lords, get_lagna_lord

def analyze_chart(name, dob, tob, pob):
    chart_data = {
        "name": name,
        "dob": dob,
        "tob": tob,
        "pob": pob,
        "planets": get_planetary_positions(dob, tob, pob),
        "house_lords": get_house_lords(dob, tob, pob),
    }
    chart_data["lagna_lord"] = get_lagna_lord(chart_data)
    return chart_data

def calculate_dasha(chart_data):
    # Mock dasha logic for now
    return {
        "current": {
            "planet": "Saturn",
            "start": "2020-05-01",
            "end": "2039-05-01",
        },
        "next": {
            "planet": "Mercury",
            "start": "2039-05-01",
            "end": "2056-05-01",
        }
    }

def get_nakshatra_details(chart_data):
    moon = chart_data["planets"].get("Moon", {})
    nakshatra_index = int(moon.get("longitude", 0) // (360 / 27))
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    return {
        "nakshatra": nakshatras[nakshatra_index],
        "padam": int(((moon.get("longitude", 0) % (360 / 27)) // 3.33) + 1)
    }

def get_yogas(chart_data):
    yogas = []
    planets = chart_data.get("planets", {})
    lords = chart_data.get("house_lords", {})

    # Gajakesari Yoga
    if 'Moon' in planets and 'Jupiter' in planets:
        moon_house = planets['Moon']['house']
        jupiter_house = planets['Jupiter']['house']
        if moon_house in [1, 4, 7, 10] and jupiter_house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Gajakesari Yoga",
                "description": "Formed when Jupiter and Moon are in kendra (1st, 4th, 7th, or 10th house) from Lagna. Brings wisdom, fame, and prosperity.",
                "type": "Raja Yoga",
                "summary": "Gajakesari Yoga: Jupiter and Moon in Kendra bring wisdom and prosperity."
            })

    # Chandra-Mangal Yoga
    if 'Moon' in planets and 'Mars' in planets:
        moon_sign = planets['Moon']['sign']
        mars_sign = planets['Mars']['sign']
        if moon_sign == mars_sign:
            yogas.append({
                "name": "Chandra-Mangal Yoga",
                "description": "Moon and Mars conjunction or mutual aspect forms this yoga, giving financial acumen and aggressive success.",
                "type": "Dhana Yoga",
                "summary": "Chandra-Mangal Yoga: Moon & Mars in same sign boosts finance and drive."
            })

    return yogas

def get_remedies(chart_data):
    remedies = []
    planets = chart_data.get("planets", {})
    dasha_info = calculate_dasha(chart_data)

    # Afflicted Moon
    moon = planets.get("Moon", {})
    if moon.get("afflicted", False):
        remedies.append({
            "planet": "Moon",
            "issue": "Emotional imbalance, stress",
            "remedy": "Chant Chandra mantra on Mondays, wear white, offer milk to Shiva.",
            "language_variants": {
                "hi": "सोमवार को चंद्र मंत्र का जाप करें, सफेद वस्त्र पहनें, शिव को दूध अर्पित करें।",
                "ta": "திங்கள் அன்று சந்திர மந்திரம் ஜபிக்கவும், வெள்ளை உடை அணியவும், சிவனுக்கு பால் நிவேதனம் செய்யவும்।"
            },
            "summary": "To strengthen Moon: chant mantra on Monday, wear white, offer milk to Shiva."
        })

    # Weak Lagna Lord
    lagna_lord = chart_data.get("lagna_lord", {})
    if lagna_lord and lagna_lord.get("strength", 100) < 50:
        remedies.append({
            "planet": lagna_lord["name"],
            "issue": "Weak Lagna lord affecting health and confidence",
            "remedy": f"Chant {lagna_lord['name']} mantra daily, perform Surya namaskar.",
            "summary": f"To strengthen Lagna Lord {lagna_lord['name']}, chant daily and practice Surya Namaskar."
        })

    # Current Dasha
    current_dasha = dasha_info.get("current", {}).get("planet")
    if current_dasha:
        remedies.append({
            "planet": current_dasha,
            "issue": f"Running {current_dasha} Mahadasha",
            "remedy": f"Worship {current_dasha} on their weekday, recite relevant stotra.",
            "summary": f"For {current_dasha} Dasha: worship on weekday, recite their stotra."
        })

    return remedies
