import swisseph as swe

# Load Swiss Ephemeris data (you can set path if not using system-wide files)
swe.set_ephe_path('.')  # Assumes ephemeris files are in current directory or installed globally

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,     # Mean Node
    "Ketu": swe.TRUE_NODE      # True Node (Ketu = 180° from Rahu)
}

def get_planet_positions(jd, latitude, longitude):
    planet_positions = {}

    for name, planet_id in PLANETS.items():
        position, _ = swe.calc_ut(jd, planet_id)
        degree = position[0]

        if name == "Ketu":
            # Ketu is always 180° opposite Rahu
            rahu_degree = planet_positions.get("Rahu", {}).get("degree", 0)
            degree = (rahu_degree + 180) % 360

        sign = get_sign_from_degree(degree)

        planet_positions[name] = {
            "sign": sign,
            "degree": round(degree, 2)
        }

    return planet_positions

def get_sign_from_degree(degree):
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    index = int(degree // 30)
    return signs[index]
