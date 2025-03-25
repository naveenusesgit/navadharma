from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from utils.kundli import (
    generate_kundli_report,
    get_dasha_periods,
    get_lagna_info,
    get_nakshatra_info
)
from utils.predictions import get_daily_prediction
from utils.matchmaking import get_matchmaking_report
from utils.numerology import get_numerology_profile
from utils.remedies import get_astrological_remedies
from utils.transit import get_transit_effects
from utils.pdf_generator import generate_pdf_prediction_report

app = FastAPI()

# Serve static files (e.g., generated PDFs)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Schemas ---
class BirthDetails(BaseModel):
    name: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    place: str

class MatchmakingDetails(BaseModel):
    boy_name: str
    boy_dob: str
    boy_tob: str
    boy_pob: str
    girl_name: str
    girl_dob: str
    girl_tob: str
    girl_pob: str

class NameOnly(BaseModel):
    name: str
    date: str

# --- Kundli Endpoints ---
@app.post("/generate-kundli")
def generate_kundli(details: BirthDetails):
    return generate_kundli_report(details.name, details.date, details.time, details.place)

@app.post("/get-dasha")
def get_dasha(details: BirthDetails):
    return get_dasha_periods(details.date, details.time, details.place)

@app.post("/get-lagna")
def lagna_info(details: BirthDetails):
    return get_lagna_info(details.date, details.time, details.place)

@app.post("/get-nakshatra")
def nakshatra_info(details: BirthDetails):
    return get_nakshatra_info(details.date, details.time, details.place)

# --- Prediction ---
@app.post("/predict")
def predict(details: NameOnly):
    return get_daily_prediction(details.name, details.date)

@app.post("/predict/pdf")
def predict_pdf(details: NameOnly):
    file_path = generate_pdf_prediction_report(details.name, details.date)
    return {"message": "PDF generated", "path": file_path}

@app.get("/download-prediction")
def download_pdf(name: str, date: str):
    file_path = f"static/predictions/{name}_{date}.pdf"
    return FileResponse(path=file_path, media_type='application/pdf', filename=f"{name}_{date}_prediction.pdf")

# --- Matchmaking ---
@app.post("/matchmaking")
def match_report(details: MatchmakingDetails):
    return get_matchmaking_report(details)

# --- Numerology ---
@app.post("/numerology")
def numerology(details: NameOnly):
    return get_numerology_profile(details.name, details.date)

# --- Remedies ---
@app.post("/remedies")
def remedies(details: BirthDetails):
    return get_astrological_remedies(details.name, details.date, details.time, details.place)

# --- Transit Effects ---
@app.post("/transit")
def transit(details: BirthDetails):
    return get_transit_effects(details.name, details.date, details.time, details.place)
