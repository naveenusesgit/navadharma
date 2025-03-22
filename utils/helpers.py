import swisseph as swe

def get_planetary_positions(chart):
    positions = {}
    planets = chart.get("planets", {})
    for planet, data in planets.items():
        positions[planet] = data.get("sign", "")
    return positions

def get_house_lords(chart):
    house_lords = {}
    asc_sign = chart.get("ascendant", {}).get("sign", "")
    sign_lords = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }

    if not asc_sign:
        return house_lords

    signs = list(sign_lords.keys())
    start_index = signs.index(asc_sign)
    rotated_signs = signs[start_index:] + signs[:start_index]

    for i, sign in enumerate(rotated_signs):
        house_lords[f"House {i+1}"] = sign_lords[sign]

    return house_lords

def get_lagna_lord(chart):
    asc_sign = chart.get("ascendant", {}).get("sign", "")
    sign_lords = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    return sign_lords.get(asc_sign, "")
