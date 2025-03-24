import swisseph as swe
import datetime
import pytz
from fpdf import FPDF
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import os

swe.set_ephe_path(".")  # Or your actual ephemeris path

geolocator = Nominatim(user_agent="kundli")
tz_finder = TimezoneFinder()

PLANETS = {
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


def get_julian_day(date_str, time_str, place):
    dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    location = geolocator.geocode(place)
    if not location:
        raise ValueError("Place not found")

    tz_name = tz_finder.timezone_at(lng=location.longitude, lat=location.latitude)
    if not tz_name:
        raise ValueError("Timezone not found")

    local_dt = pytz.timezone(tz_name).localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)

    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)
    return jd, location.latitude, location.longitude


def get_planetary_positions(date, time, place):
    jd, lat, lon = get_julian_day(date, time, place)
    positions = {}
    for planet_name, planet_id in PLANETS.items():
        pos, _ = swe.calc_ut(jd, planet_id)
        positions[planet_name] = round(pos[0], 2)
    return positions


def get_lagna_info(date, time, place):
    jd, lat, lon = get_julian_day(date, time, place)
    ascendant = swe.houses(jd, lat, lon)[0][0]
    return {"ascendant_degree": round(ascendant, 2)}


def get_dasha_periods(date, time, place):
    return {
        "current_dasha": "Sun → Moon",
        "next_dasha": "Moon → Mars",
        "notes": "Dasha logic can be extended with Vimshottari Dasha using sweph"
    }


def get_kundli_chart(date, time, place):
    return get_planetary_positions(date, time, place)


def get_navamsa_chart(date, time, place):
    # Placeholder for D9 chart
    return {"note": "Navamsa chart requires divisional chart logic. Coming soon."}


def get_nakshatra_info(date, time, place):
    jd, lat, lon = get_julian_day(date, time, place)
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    nakshatra_index = int(moon_pos[0] / (360 / 27))
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
        "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
        "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshta", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
        "Uttara Bhadrapada", "Revati"
    ]
    return {"nakshatra": nakshatras[nakshatra_index]}


def get_transit_analysis(date, time, place):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    jd, lat, lon = get_julian_day(*today.split(), place)
    positions = {}
    for planet_name, planet_id in PLANETS.items():
        pos, _ = swe.calc_ut(jd, planet_id)
        positions[planet_name] = round(pos[0], 2)
    return {"transit_positions": positions}


def generate_kundli_report(name, date, time, place):
    positions = get_planetary_positions(date, time, place)
    lagna = get_lagna_info(date, time, place)
    nakshatra = get_nakshatra_info(date, time, place)
    dasha = get_dasha_periods(date, time, place)
    return {
        "name": name,
        "place": place,
        "planet_positions": positions,
        "lagna": lagna,
        "nakshatra": nakshatra,
        "dasha": dasha
    }


def generate_pdf_report(name, date, time, place):
    report = generate_kundli_report(name, date, time, place)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Kundli Report for {name}", ln=True, align="C")
    pdf.ln(10)
    for key, section in report.items():
        if isinstance(section, dict):
            pdf.cell(200, 10, txt=key.upper(), ln=True, align="L")
            for k, v in section.items():
                pdf.cell(200, 10, txt=f"{k}: {v}", ln=True, align="L")
        else:
            pdf.cell(200, 10, txt=f"{key}: {section}", ln=True, align="L")
        pdf.ln(5)
    filename = f"{name}_kundli.pdf".replace(" ", "_")
    filepath = f"/tmp/{filename}"
    pdf.output(filepath)
    return filepath
