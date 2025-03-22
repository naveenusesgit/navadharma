import swisseph as swe
from datetime import datetime
import pytz

PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,
    'Ketu': 'Ketu',  # computed manually below
}

def get_transits(date: datetime, lat: float, lon: float, timezone_str='UTC'):
    """Get real-time planetary transits for given date and location."""

    # Convert date to UTC timestamp
    tz = pytz.timezone(timezone_str)
    local_dt = tz.localize(date)
    utc_dt = local_dt.astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)

    swe.set_topo(lon, lat, 0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    transits = {}

    for planet_name, planet_id in PLANETS.items():
        if planet_name == "Ketu":
            rahu = swe.calc_ut(jd, swe.MEAN_NODE)[0]
            ketu = (rahu[0] + 180) % 360
            transits["Ketu"] = {"longitude": round(ketu, 2)}
            continue

        lon_data = swe.calc_ut(jd, planet_id)
        degree = lon_data[0]
        sign = get_rashi(degree)
        nakshatra = get_nakshatra(degree)

        transits[planet_name] = {
            "longitude": round(degree, 2),
            "sign": sign,
            "nakshatra": nakshatra
        }

    return transits


def get_rashi(degree):
    rashis = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return rashis[int(degree // 30)]


def get_nakshatra(degree):
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    return nakshatras[int(degree // (360 / 27))]


if __name__ == "__main__":
    # 🔁 Example test run
    now = datetime.now()
    sample_transit = get_transits(now, lat=12.9716, lon=77.5946, timezone_str="Asia/Kolkata")
    for planet, details in sample_transit.items():
        print(f"{planet}: {details}")
