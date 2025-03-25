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
    generate_full_kundli_prediction,
)
from utils.daily_predictions import get_daily_prediction

app = FastAPI()


class KundliRequest(BaseModel):
    datetime: str
    place: str
    latitude: float
    longitude: float
    timezone: float


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


@app.post("/daily-prediction")
def daily_prediction(req: KundliRequest):
    return get_daily_prediction(req.datetime, req.place, req.latitude, req.longitude, req.timezone)
