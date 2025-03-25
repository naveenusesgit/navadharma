from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils.kundli import (
    generate_kundli_report,
    get_dasha_periods,
    get_transit_effects,
    get_nakshatra_info,
    get_lagna_info
)
from utils.matchmaking import get_matchmaking_report
from utils.numerology import get_numerology_report
from utils.remedies import get_remedies
from utils.predictions import get_daily_prediction
from utils.pdf_generator import generate_pdf_report

app = FastAPI(
    title="Navadharma Astrology API",
    description="Comprehensive API for Vedic astrology calculations and reports",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class KundliInput(BaseModel):
    name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str

class MatchmakingInput(BaseModel):
    boy_name: str
    boy_dob: str
    boy_tob: str
    boy_pob: str
    girl_name: str
    girl_dob: str
    girl_tob: str
    girl_pob: str

class NameInput(BaseModel):
    name: str

# Root
@app.get("/")
def root():
    return {"message": "🌟 Navadharma Astrology API is running!"}

# Kundli Report
@app.post("/generate-report")
def generate_report(data: KundliInput):
    try:
        return {"status": "success", "data": generate_kundli_report(**data.dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Matchmaking
@app.post("/matchmaking")
def matchmaking(data: MatchmakingInput):
    try:
        return {"status": "success", "data": get_matchmaking_report(**data.dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Numerology
@app.post("/numerology")
def numerology(data: NameInput):
    try:
        return {"status": "success", "data": get_numerology_report(data.name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Remedies
@app.post("/remedies")
def remedies(data: NameInput):
    try:
        return {"status": "success", "data": get_remedies(data.name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Daily Predictions
@app.post("/daily-predictions")
def predictions(data: KundliInput):
    try:
        return {"status": "success", "data": get_daily_prediction(**data.dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Dasha Periods
@app.post("/dasha")
def dasha(data: KundliInput):
    try:
        return {"status": "success", "data": get_dasha_periods(**data.dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Transit effects
@app.post("/transit")
def transit(data: KundliInput):
    try:
        return {"status": "success", "data": get_transit_effects(**data.dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PDF Report Generator
@app.post("/generate-pdf")
def generate_pdf(data: KundliInput):
    try:
        pdf_bytes = generate_pdf_report(**data.dict())
        return {"status": "success", "pdf": pdf_bytes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Nakshatra Info
@app.post("/nakshatra")
def nakshatra(data: KundliInput):
    try:
        return {"status": "success", "data": get_nakshatra_info(**data.dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lagna Info
@app.post("/lagna")
def lagna(data: KundliInput):
    try:
        return {"status": "success", "data": get_lagna_info(**data.dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
