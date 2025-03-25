from fastapi import FastAPI
from pydantic import BaseModel
from utils.kundli import (
    get_planet_positions,
    get_lagna_info,
    get_dasha_periods,
    get_nakshatra_details,
    get_planetary_aspects,
    get_transit_predictions,
    generate_kundli_report_pdf,
    generate_full_kundli_prediction
)

app = FastAPI()


class KundliRequest(BaseModel):
    name: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    place: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the Navadharma Kundli API"}


@app.post("/planet-positions")
def planet_positions(req: KundliRequest):
    return get_planet_positions(req.name, req.date, req.time, req.place)


@app.post("/lagna-info")
def lagna_info(req: KundliRequest):
    return get_lagna_info(req.name, req.date, req.time, req.place)


@app.post("/dasha-periods")
def dasha_periods(req: KundliRequest):
    return get_dasha_periods(req.name, req.date, req.time, req.place)


@app.post("/nakshatra-details")
def nakshatra_details(req: KundliRequest):
    return get_nakshatra_details(req.name, req.date, req.time, req.place)


@app.post("/planetary-aspects")
def planetary_aspects(req: KundliRequest):
    return get_planetary_aspects(req.name, req.date, req.time, req.place)


@app.post("/transit-predictions")
def transit_predictions(req: KundliRequest):
    return get_transit_predictions(req.name, req.date, req.time, req.place)


@app.post("/generate-kundli-pdf")
def generate_pdf(req: KundliRequest):
    return generate_kundli_report_pdf(req.name, req.date, req.time, req.place)


@app.post("/generate-full-prediction")
def generate_prediction(req: KundliRequest):
    return generate_full_kundli_prediction(req.name, req.date, req.time, req.place)
