import datetime
import swisseph as swe
from utils.geolocation import get_lat_lon_timezone

swe.set_ephe_path('.')  # Optional: path to Swiss Ephemeris data

def get_transits(dob: str, tob: str, pob: str):
    lat, lon, timezone = get_lat_lon_timezone(pob)

    dt = datetime.datetime.strptime(f"{dob} {tob}", "%d-%m-%Y %H:%M")
    utc_dt = dt - datetime.timedelta(hours=datetime.datetime.now().astimezone().utcoffset().total_seconds() / 3600)

    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)

    planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    planet_ids = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN, swe.MEAN_NODE]

    results = {}

    for i, pid in enumerate(planet_ids):
        lon, _ = swe.calc_ut(jd, pid)
        results[planets[i]] = round(lon[0], 2)

    # Ketu = 180 deg opposite Rahu
    if 'Rahu' in results:
        results['Ketu'] = (results['Rahu'] + 180) % 360

    return results

def get_daily_global_transits():
    today = datetime.datetime.utcnow()
    jd = swe.julday(today.year, today.month, today.day, today.hour + today.minute / 60.0)

    planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    planet_ids = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN, swe.MEAN_NODE]

    results = {}
    for i, pid in enumerate(planet_ids):
        lon, _ = swe.calc_ut(jd, pid)
        results[planets[i]] = round(lon[0], 2)

    if 'Rahu' in results:
        results['Ketu'] = (results['Rahu'] + 180) % 360

    return results
