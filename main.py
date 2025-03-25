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

@app.post("/daily-prediction")
def daily_prediction(req: KundliRequest):
    return get_daily_prediction(req.datetime, req.place, req.latitude, req.longitude, req.timezone)
