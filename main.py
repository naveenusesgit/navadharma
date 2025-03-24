from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils.kundli import (
    generate_kundli_report,
    get_kundli_chart,
    get_dasha_periods,
    get_nakshatra_info,
    get_lagna_info,
    get_navamsa_chart,
    get_planetary_positions,
    get_transit_analysis,
    generate_pdf_report
)
from utils.matchmaking import get_matchmaking_report
from utils.numerology import get_numerology_report
from utils.remedies import get_remedies
from utils.predictions import get_daily_predictions

app = FastAPI(title="Navadharma Astrology API", version="2.5")

class BirthDetails(BaseModel):
    name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str

class MatchRequest(BaseModel):
    person1: BirthDetails
    person2: BirthDetails

@app.get("/")
def home():
    return {"message": "Welcome to Navadharma API. Use /generate-report, /chart, /matchmaking, /pdf, etc."}


@app.post("/generate-report")
def generate_report(data: BirthDetails):
    try:
        return {"success": True, "data": generate_kundli_report(**data.dict())}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/chart")
def chart(data: BirthDetails):
    return {"success": True, "chart": get_kundli_chart(**data.dict())}


@app.post("/dasha")
def dasha(data: BirthDetails):
    return {"success": True, "dasha": get_dasha_periods(**data.dict())}


@app.post("/nakshatra")
def nakshatra(data: BirthDetails):
    return {"success": True, "nakshatra": get_nakshatra_info(**data.dict())}


@app.post("/lagna")
def lagna(data: BirthDetails):
    return {"success": True, "lagna": get_lagna_info(**data.dict())}


@app.post("/navamsa")
def navamsa(data: BirthDetails):
    return {"success": True, "navamsa": get_navamsa_chart(**data.dict())}


@app.post("/positions")
def planetary_positions(data: BirthDetails):
    return {"success": True, "positions": get_planetary_positions(**data.dict())}


@app.post("/transit")
def transit(data: BirthDetails):
    return {"success": True, "transit": get_transit_analysis(**data.dict())}


@app.post("/pdf")
def generate_pdf(data: BirthDetails):
    try:
        filename = generate_pdf_report(**data.dict())
        return FileResponse(filename, media_type='application/pdf', filename=filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF generation failed: {str(e)}")


@app.post("/matchmaking")
def matchmaking(data: MatchRequest):
    return {
        "success": True,
        "match": get_matchmaking_report(data.person1.dict(), data.person2.dict())
    }


@app.post("/numerology")
def numerology(data: BirthDetails):
    return {"success": True, "numerology": get_numerology_report(**data.dict())}


@app.post("/remedies")
def remedies(data: BirthDetails):
    return {"success": True, "remedies": get_remedies(**data.dict())}


@app.post("/daily-prediction")
def daily_prediction(data: BirthDetails):
    return {"success": True, "prediction": get_daily_predictions(**data.dict())}
