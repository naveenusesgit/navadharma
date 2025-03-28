from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.kundli import generate_kundli_chart

app = FastAPI(title="Navadharma Jyotish API", version="1.0")

class KundliRequest(BaseModel):
    datetime: str  # Format: "YYYY-MM-DD HH:MM:SS"
    latitude: float
    longitude: float
    timezone: float


@app.post("/get-kundli-chart")
def get_kundli_chart(req: KundliRequest):
    return generate_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)


@app.post("/nakshatra-details")
def get_nakshatra(req: KundliRequest):
    chart = generate_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)
    return chart["nakshatra_details"]


@app.post("/planet-positions")
def get_planet_positions_route(req: KundliRequest):
    chart = generate_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)
    return {"planet_positions": chart["planet_positions"]}


@app.get("/")
def root():
    return {"message": "🕉️ Navadharma Jyotish API is running (KP Ayanamsa)"}
