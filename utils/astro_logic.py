import swisseph as swe
import datetime

def get_planet_positions(jd):
    planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    planet_ids = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN, swe.MEAN_NODE]

    results = {}
    for i, pid in enumerate(planet_ids):
        lon, _ = swe.calc_ut(jd, pid)
        results[planets[i]] = round(lon[0], 2)

    # Ketu = opposite of Rahu
    if 'Rahu' in results:
        results['Ketu'] = (results['Rahu'] + 180) % 360

    return results

def calculate_dasha(jd):
    # Dummy Dasha calculation for now
    return {"dasha_period": "Venus Mahadasha - Mercury Antardasha"}

def get_nakshatra(jd):
    moon_lon, _ = swe.calc_ut(jd, swe.MOON)
    nakshatra_index = int((moon_lon[0] % 360) / (360 / 27))
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    return nakshatras[nakshatra_index]
