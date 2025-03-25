from fastapi import FastAPI
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
    month: str = None  # Optional

# Weekly prediction input
class WeeklyRequest(BaseModel):
    rashi: str
    week: str = None  # Optional

# Numerology input
class NumerologyRequest(BaseModel):
    name: str
    dob: str  # Format: YYYY-MM-DD


@app.post("/planet-positions")
def planet_positions(req: KundliRequest):
    return get_planet_positions(req.datetime, req.latitude, req.longitude, req.timezone)


@app.post("/lagna-info")
def lagna_info(req: KundliRequest):
    return get_lagna_info(req.datetime, req.latitude, req.longitude, req.timezone)


@app.post("/dasha-periods")
def dasha_periods(req: KundliRequest):
    return get_dasha_periods(req.datetime, req.latitude, req.longitude, req.timezone)


@app.post("/nakshatra-details")
def nakshatra_details(req: KundliRequest):
    return get_nakshatra_details(req.datetime, req.latitude, req.longitude, req.timezone)


@app.post("/planetary-aspects")
def planetary_aspects(req: KundliRequest):
    return get_planetary_aspects(req.datetime, req.latitude, req.longitude, req.timezone)


@app.post("/transit-predictions")
def transit_predictions(req: KundliRequest):
    return get_transit_predictions(req.datetime, req.latitude, req.longitude, req.timezone)


@app.post("/kundli-chart")
def kundli_chart(req: KundliRequest):
    return get_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)


@app.post("/generate-pdf-report")
def generate_pdf_report(req: KundliRequest):
    return generate_kundli_report_pdf(req.datetime, req.place, req.latitude, req.longitude, req.timezone)


@app.post("/generate-full-prediction")
def generate_full_prediction(req: KundliRequest):
    return generate_full_kundli_prediction(req.datetime, req.place, req.latitude, req.longitude, req.timezone)


@app.post("/monthly-prediction")
def monthly_prediction(req: MonthlyRequest):
    return get_monthly_prediction(req.rashi, req.month)


@app.post("/weekly-prediction")
def weekly_prediction(req: WeeklyRequest):
    return get_weekly_prediction(req.rashi, req.week)


@app.post("/numerology")
def numerology(req: NumerologyRequest):
    return get_numerology(req.name, req.dob)
