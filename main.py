from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from utils.kundli import (
    get_planet_positions,
    get_ascendant_info,
    get_house_mapping,
    get_moon_info,
    get_yogas,
    get_remedies,
    get_transit_analysis,
    get_dasha_periods,
    get_kundli_chart,
    get_numerology,
    get_lagna_info,
    get_nakshatra_info,
    get_pdf_report,
    get_summary,
    get_weekly_prediction,
    get_monthly_prediction,
    get_muhurats,
    get_panchanga_calendar,
    get_planetary_aspects
)

app = FastAPI(title="Navadharma Jyotish API")

class KundliRequest(BaseModel):
    datetime: str
    latitude: float
    longitude: float
    timezone: float
    place: Optional[str] = None
    goal: Optional[str] = None
    lang: Optional[str] = "en"

# 🪐 Base planetary positions
@app.post("/planet-positions")
def planet_positions(data: KundliRequest):
    return get_planet_positions(data.datetime, data.latitude, data.longitude, data.timezone)

# 🪔 Kundli chart with houses and ascendant
@app.post("/get-kundli-chart")
def kundli_chart(data: KundliRequest):
    return get_kundli_chart(data.datetime, data.latitude, data.longitude, data.timezone)

# 📈 Full Kundli predictions (composite)
@app.post("/generate-kundli")
def generate_kundli(data: KundliRequest):
    return {
        "planet_positions": get_planet_positions(data.datetime, data.latitude, data.longitude, data.timezone),
        "ascendant": get_ascendant_info(data.datetime, data.latitude, data.longitude, data.timezone),
        "moon": get_moon_info(data.datetime, data.latitude, data.longitude, data.timezone),
        "house_mapping": get_house_mapping(data.datetime, data.latitude, data.longitude, data.timezone),
        "yogas": get_yogas(data.datetime, data.latitude, data.longitude, data.timezone),
        "remedies": get_remedies(
            planetary_status=get_planet_positions(data.datetime, data.latitude, data.longitude, data.timezone),
            house_mapping=get_house_mapping(data.datetime, data.latitude, data.longitude, data.timezone),
            lang=data.lang
        )
    }

# 📄 Generate PDF Kundli Report
@app.post("/generate-pdf-report")
def pdf_report(data: KundliRequest):
    return get_pdf_report(data)

# 🔭 Dasha periods (Mahadasha, Antardasha)
@app.post("/dasha-periods")
def dasha(data: KundliRequest):
    return get_dasha_periods(data.datetime, data.latitude, data.longitude, data.timezone)

# 🧘 Remedies
@app.post("/remedies")
def remedies(data: KundliRequest):
    planetary_status = get_planet_positions(data.datetime, data.latitude, data.longitude, data.timezone)
    house_mapping = get_house_mapping(data.datetime, data.latitude, data.longitude, data.timezone)
    return get_remedies(planetary_status=planetary_status, house_mapping=house_mapping, lang=data.lang)

# 🧩 Yogas
@app.post("/yogas")
def yogas(data: KundliRequest):
    return {"yogas": get_yogas(data.datetime, data.latitude, data.longitude, data.timezone)}

# 🌠 Transits
@app.post("/transits")
def transits(data: KundliRequest):
    return get_transit_analysis(data.datetime, data.latitude, data.longitude, data.timezone)

# 🪐 Lagna Sign
@app.post("/lagna-info")
def lagna(data: KundliRequest):
    return get_lagna_info(data.datetime, data.latitude, data.longitude, data.timezone)

# 🌙 Nakshatra
@app.post("/nakshatra-details")
def nakshatra(data: KundliRequest):
    return get_nakshatra_info(data.datetime, data.latitude, data.longitude, data.timezone)

# 📊 Numerology
@app.post("/numerology")
def numerology(name: str, dob: str):
    return get_numerology(name, dob)

# 🧠 Summary GPT-friendly
@app.post("/generate-summary")
def summary(data: KundliRequest):
    return get_summary(data)

# 📅 Weekly Prediction
@app.post("/weekly-prediction")
def weekly(data: dict):
    return get_weekly_prediction(data["rashi"], data["week"])

# 📆 Monthly Prediction
@app.post("/monthly-prediction")
def monthly(data: dict):
    return get_monthly_prediction(data["rashi"], data["month"])

# 🕉 Muhurats
@app.get("/muhurats")
def muhurats(date: str, lat: float, lon: float, tz: float, type: Optional[str] = None):
    return get_muhurats(date, lat, lon, tz, type)

# 📿 Panchanga Calendar
@app.get("/panchanga-calendar")
def panchanga(start: str, days: int, lat: float, lon: float, tz: float):
    return get_panchanga_calendar(start, days, lat, lon, tz)

# 🔭 Planetary aspects
@app.post("/planetary-aspects")
def aspects(data: KundliRequest):
    return get_planetary_aspects(data.datetime, data.latitude, data.longitude, data.timezone)

# 💖 Root check
@app.get("/")
def root():
    return {"message": "🕉️ Navadharma Jyotish API is live."}

# ✅ Health check
@app.get("/health")
def health():
    return {"status": "healthy", "uptime": "running"}

