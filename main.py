from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel
from utils.kundli import (
    get_planet_positions,
    get_lagna_info,
    get_dasha_periods,
    get_nakshatra_details,
    get_planetary_aspects,
    get_transit_predictions,
    get_kundli_chart,
    generate_kundli_report_pdf,
    generate_full_kundli_prediction
)
from utils.monthly_prediction import get_monthly_prediction
from utils.weekly_prediction import get_weekly_prediction
from utils.numerology import get_numerology
from utils.interpretations import get_yogas  # ✅ Import yoga logic
from utils.panchanga_calendar import generate_panchanga_calendar

app = FastAPI()

# Base request model
class KundliRequest(BaseModel):
    datetime: str
    place: str
    latitude: float
    longitude: float
    timezone: float

# Monthly prediction input
class MonthlyRequest(BaseModel):
    rashi: str
    month: str = None

# Weekly prediction input
class WeeklyRequest(BaseModel):
    rashi: str
    week: str = None

# Numerology input
class NumerologyRequest(BaseModel):
    name: str
    dob: str  # Format: YYYY-MM-DD


@app.post("/planet-positions")
def planet_positions(req: KundliRequest):
    result = get_planet_positions(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"planet_positions": result}

@app.post("/lagna-info")
def lagna_info(req: KundliRequest):
    result = get_lagna_info(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"lagna_info": result}

@app.post("/dasha-periods")
def dasha_periods(req: KundliRequest):
    result = get_dasha_periods(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"dasha_periods": result}

@app.post("/nakshatra-details")
def nakshatra_details(req: KundliRequest):
    result = get_nakshatra_details(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"nakshatra_details": result}

@app.post("/planetary-aspects")
def planetary_aspects(req: KundliRequest):
    result = get_planetary_aspects(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"planetary_aspects": result}

@app.post("/transit-predictions")
def transit_predictions(req: KundliRequest):
    result = get_transit_predictions(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"transit_predictions": result}

@app.post("/kundli-chart")
def kundli_chart(req: KundliRequest):
    result = get_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"kundli_chart": result}

@app.post("/generate-pdf-report")
def generate_pdf_report(req: KundliRequest):
    result = generate_kundli_report_pdf(req.datetime, req.place, req.latitude, req.longitude, req.timezone)
    return {"pdf_report": result}

@app.post("/generate-full-prediction")
def generate_full_prediction(req: KundliRequest):
    result = generate_full_kundli_prediction(req.datetime, req.place, req.latitude, req.longitude, req.timezone)
    return {"full_prediction": result}

@app.post("/generate-kundli")
def generate_kundli(req: KundliRequest):
    result = generate_full_kundli_prediction(req.datetime, req.place, req.latitude, req.longitude, req.timezone)
    return {"kundli": result}

@app.post("/monthly-prediction")
def monthly_prediction(req: MonthlyRequest):
    result = get_monthly_prediction(req.rashi, req.month)
    return {"monthly_prediction": result}

@app.post("/weekly-prediction")
def weekly_prediction(req: WeeklyRequest):
    result = get_weekly_prediction(req.rashi, req.week)
    return {"weekly_prediction": result}

@app.post("/numerology")
def numerology(req: NumerologyRequest):
    result = get_numerology(req.name, req.dob)
    return {"numerology": result}

# ✅ NEW Yogas + Dasha-Aware + Remedy-Powered Endpoint
@app.post("/yogas")
def yoga_interpretations(req: KundliRequest):
    result = get_yogas(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"yogas": result}

@app.get("/panchanga-calendar")
def panchanga_calendar(
    start: str = Query(..., description="ISO start date"),
    days: int = Query(7, description="Number of days"),
    lat: float = Query(...),
    lon: float = Query(...),
    tz: float = Query(...),
):
    result = generate_panchanga_calendar(start, days, lat, lon, tz)
    return {"calendar": result}
