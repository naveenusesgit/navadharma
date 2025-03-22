import swisseph as swe
import datetime

PLANETS = {
    0: "Sun", 1: "Moon", 2: "Mars", 3: "Mercury", 4: "Jupiter",
    5: "Venus", 6: "Saturn", 7: "Rahu", 8: "Ketu"
}

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula",
    "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_nakshatra(longitude):
    nakshatra_index = int((longitude % 360) / (360 / 27))
    return NAKSHATRAS[nakshatra_index]

def get_planet_positions(jd, lat, lon):
    swe.set_topo(lon, lat, 0)
    planet_data = {}
    for i in PLANETS:
        lon, _, _ = swe.calc_ut(jd, i)
        nakshatra = get_nakshatra(lon)
        planet_data[PLANETS[i]] = {
            "degree": round(lon, 2),
            "nakshatra": nakshatra
        }
    return planet_data

def detect_yogas(planet_positions):
    yogas = []

    moon = planet_positions.get("Moon", {})
    jupiter = planet_positions.get("Jupiter", {})
    sun = planet_positions.get("Sun", {})
    mercury = planet_positions.get("Mercury", {})
    mars = planet_positions.get("Mars", {})
    saturn = planet_positions.get("Saturn", {})

    # Gajakesari Yoga
    if abs(jupiter["degree"] - moon["degree"]) <= 90:
        yogas.append("Gajakesari Yoga")

    # Budha-Aditya Yoga
    if abs(mercury["degree"] - sun["degree"]) <= 15:
        yogas.append("Budha-Aditya Yoga")

    # Kemadruma Yoga
    if "Mercury" not in planet_positions or "Venus" not in planet_positions:
        yogas.append("Kemadruma Yoga")

    # Neecha Bhanga Raj Yoga (simplified)
    if mars["degree"] > 180 and saturn["degree"] < 30:
        yogas.append("Neecha Bhanga Raj Yoga")

    return yogas

def calculate_dasha(jd):
    # Placeholder logic — swap with actual Vimshottari logic using swisseph
    return {
        "mahadasha": "Moon",
        "antardasha": "Saturn",
        "period": "2024-2034"
    }

def get_remedies(yogas, dasha):
    remedies = []

    if "Kemadruma Yoga" in yogas:
        remedies.append("Chant Chandra mantra daily")

    if dasha["mahadasha"] == "Saturn":
        remedies.append("Light sesame oil lamp on Saturdays")

    if dasha["antardasha"] == "Rahu":
        remedies.append("Feed dogs and donate blue/black clothes on Saturdays")

    return remedies

def analyze_chart(jd, lat, lon):
    planets = get_planet_positions(jd, lat, lon)
    yogas = detect_yogas(planets)
    dasha = calculate_dasha(jd)
    remedies = get_remedies(yogas, dasha)

    return {
        "planets": planets,
        "yogas": yogas,
        "dasha": dasha,
        "remedies": remedies
    }
