import swisseph as swe
from datetime import datetime
import pytz

# Nakshatra Names (27 segments of 13°20')
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Graha list for convenience
planets = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN
}

# Set Ephemeris
swe.set_ephe_path('.')


def get_julian_day(date_str, time_str, timezone_str='Asia/Kolkata'):
    """Convert birth date and time into Julian Day"""
    tz = pytz.timezone(timezone_str)
    dt = tz.localize(datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)


def get_nakshatra(longitude):
    """Get Nakshatra from ecliptic longitude"""
    segment = int((longitude % 360) / (360 / 27))
    return nakshatras[segment]


def get_planet_positions(jd, lat, lon):
    """Calculate positions and nakshatras for all planets"""
    positions = {}
    nakshatra_info = {}

    for name, planet_id in planets.items():
        lonlat, _ = swe.calc_ut(jd, planet_id)
        positions[name] = lonlat[0]
        nakshatra_info[name] = get_nakshatra(lonlat[0])

    return positions, nakshatra_info
    # Helper to calculate which house a planet falls in from a given ascendant
def get_house_from_lagna(lagna_deg, planet_deg):
    diff = (planet_deg - lagna_deg) % 360
    house = int(diff // 30) + 1
    return house


def get_planet_houses(lagna_deg, planet_positions):
    """Return planet house numbers from Lagna"""
    houses = {}
    for planet, pos in planet_positions.items():
        houses[planet] = get_house_from_lagna(lagna_deg, pos)
    return houses


def detect_lagna_yogas(planet_houses, asc_sign):
    yogas = []

    # Example: Vipareeta Raja Yoga
    # Lord of 6, 8, 12 in any of those houses
    bad_houses = [6, 8, 12]
    for planet, house in planet_houses.items():
        if house in bad_houses:
            yogas.append(f"Vipareeta Raja Yoga: {planet} in house {house}")

    return yogas


def detect_chandra_lagna_yogas(planet_positions, moon_deg):
    """Detect yogas using Moon as Lagna"""
    yogas = []

    # Gajakesari Yoga: Jupiter in Kendra from Moon
    jupiter_deg = planet_positions.get("Jupiter")
    if jupiter_deg:
        jup_house = get_house_from_lagna(moon_deg, jupiter_deg)
        if jup_house in [1, 4, 7, 10]:
            yogas.append("Gajakesari Yoga: Jupiter in Kendra from Moon")

    # Kemadruma Yoga: No planets in 2nd or 12th from Moon
    moon_house = get_house_from_lagna(moon_deg, moon_deg)
    kemadruma = True
    for planet, deg in planet_positions.items():
        if planet == "Moon":
            continue
        house = get_house_from_lagna(moon_deg, deg)
        if house in [moon_house - 1, moon_house + 1, 12, 2]:
            kemadruma = False
            break
    if kemadruma:
        yogas.append("Kemadruma Yoga: Moon is not flanked by any planet")

    return yogas


def detect_common_yogas(planet_positions, planet_houses):
    yogas = []

    # Budha-Aditya Yoga: Sun and Mercury in same house
    if planet_houses.get("Sun") == planet_houses.get("Mercury"):
        yogas.append("Budha-Aditya Yoga: Sun and Mercury in same house")

    # Neecha Bhanga Raja Yoga - simplified version
    if planet_houses.get("Saturn") == 7 and planet_houses.get("Moon") == 1:
        yogas.append("Neecha Bhanga Raja Yoga: Saturn and Moon balancing debility")

    return yogas
def analyze_chart(date: str, time: str, lat: float, lon: float, timezone='Asia/Kolkata'):
    jd = get_julian_day(date, time, timezone)

    # Get planetary positions and Nakshatras
    planet_positions, nakshatras_info = get_planet_positions(jd, lat, lon)

    # Calculate Ascendant (Lagna)
    asc_info = swe.houses(jd, lat, lon)
    ascendant_deg = asc_info[0][0]  # First cusp = Ascendant

    # Moon's position (for Chandra Lagna)
    moon_deg = planet_positions.get("Moon", 0)

    # Get house positions
    planet_houses = get_planet_houses(ascendant_deg, planet_positions)

    # Detect Yogas
    lagna_yogas = detect_lagna_yogas(planet_houses, ascendant_deg)
    chandra_yogas = detect_chandra_lagna_yogas(planet_positions, moon_deg)
    special_yogas = detect_common_yogas(planet_positions, planet_houses)

    return {
        "nakshatras": nakshatras_info,
        "planetHouses": planet_houses,
        "lagnaDegree": ascendant_deg,
        "moonDegree": moon_deg,
        "lagnaYogas": lagna_yogas,
        "chandraLagnaYogas": chandra_yogas,
        "specialYogas": special_yogas
    }


