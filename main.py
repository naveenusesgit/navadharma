from fastapi import FastAPI
from pydantic import BaseModel
from utils.kundli import *

app = FastAPI(title="Navadharma Jyotish API", version="2.0")

class KundliRequest(BaseModel):
    datetime: str
    latitude: float
    longitude: float
    timezone: float

@app.post("/get-kundli-chart")
def get_kundli(req: KundliRequest):
    return generate_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)

@app.post("/planet-positions")
def get_positions(req: KundliRequest):
    return {"planet_positions": get_planet_positions(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.post("/nakshatra-details")
def nakshatra(req: KundliRequest):
    pos = get_planet_positions(req.datetime, req.latitude, req.longitude, req.timezone)
    return get_nakshatra_and_pada(pos["Moon"])

@app.post("/dasha-periods")
def dashas(req: KundliRequest):
    return {"dashas": get_dasha_periods(req.datetime, req.timezone)}

@app.post("/remedies")
def remedies(req: KundliRequest):
    chart = generate_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)
    return get_remedies(chart["planet_positions"], chart["ascendant"]["lagna_sign"])

@app.post("/transits")
def transits(req: KundliRequest):
    natal = get_planet_positions(req.datetime, req.latitude, req.longitude, req.timezone)
    return analyze_transits(natal)

@app.post("/generate-summary")
def summary(req: KundliRequest):
    chart = generate_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)
    return generate_summary(chart)

@app.get("/")
def root():
    return {"message": "🌐🕉️ Navadharma Jyotish API is Live!"}
