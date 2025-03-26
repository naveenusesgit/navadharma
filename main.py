from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from utils.kundli import (
    get_planet_positions,
    get_lagna_info,
    get_dasha_periods,
    get_nakshatra_details,
    get_planetary_aspects,
    get_transit_predictions,
    get_kundli_chart,
)
from utils.monthly_prediction import get_monthly_prediction
from utils.weekly_prediction import get_weekly_prediction
from utils.numerology import get_numerology
from utils.interpretations import get_yogas
from utils.panchanga_calendar import generate_panchanga_calendar
from utils.muhurat_finder import find_muhurats
from utils.full_kundli_prediction import generate_full_kundli_prediction
from utils.pdf_utils import generate_kundli_report_pdf
from utils.models import (
    KundliRequest,
    MonthlyRequest,
    WeeklyRequest,
    NumerologyRequest,
)

app = FastAPI(title="Navadharma Jyotish API")

# --- Core Endpoints ---

@app.post("/planet-positions", tags=["Kundli Core"])
def planet_positions(req: KundliRequest):
    return {"planet_positions": get_planet_positions(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.post("/lagna-info", tags=["Kundli Core"])
def lagna_info(req: KundliRequest):
    return {"lagna_info": get_lagna_info(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.post("/dasha-periods", tags=["Dasha & Timelines"])
def dasha_periods(req: KundliRequest):
    return {"dasha_periods": get_dasha_periods(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.post("/nakshatra-details", tags=["Nakshatra & Moon"])
def nakshatra_details(req: KundliRequest):
    return {"nakshatra_details": get_nakshatra_details(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.post("/planetary-aspects", tags=["Kundli Core"])
def planetary_aspects(req: KundliRequest):
    return {"planetary_aspects": get_planetary_aspects(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.post("/transit-predictions", tags=["Transits & Gochar"])
def transit_predictions(req: KundliRequest):
    return {"transit_predictions": get_transit_predictions(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.post("/kundli-chart", tags=["Kundli Core"])
def kundli_chart(req: KundliRequest):
    return {"kundli_chart": get_kundli_chart(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.post("/generate-kundli", tags=["Kundli Reports"])
def generate_kundli(req: KundliRequest, goal: str = "business"):
    return {"kundli": generate_full_kundli_prediction(req.datetime, req.place, req.latitude, req.longitude, req.timezone, goal)}

@app.post("/generate-full-prediction", tags=["Kundli Reports"])
def generate_full_prediction(req: KundliRequest):
    return {"full_prediction": generate_full_kundli_prediction(req.datetime, req.place, req.latitude, req.longitude, req.timezone)}

@app.post("/generate-pdf-report", tags=["Kundli Reports"])
def generate_pdf_report(req: KundliRequest):
    return {"pdf_report": generate_kundli_report_pdf(req.datetime, req.place, req.latitude, req.longitude, req.timezone)}

# --- Yoga, Panchanga, Muhurat ---

@app.post("/yogas", tags=["Yogas & Remedies"])
def yoga_interpretations(req: KundliRequest):
    return {"yogas": get_yogas(req.datetime, req.latitude, req.longitude, req.timezone)}

@app.get("/panchanga-calendar", tags=["Panchanga & Muhurat"])
def panchanga_calendar(
    start: str = Query(..., description="ISO start date"),
    days: int = Query(7, description="Number of days"),
    lat: float = Query(...),
    lon: float = Query(...),
    tz: float = Query(...),
):
    return {"calendar": generate_panchanga_calendar(start, days, lat, lon, tz)}

@app.get("/muhurats", tags=["Panchanga & Muhurat"])
def muhurat_finder(
    date: str = Query(..., description="Date in ISO format"),
    lat: float = Query(...),
    lon: float = Query(...),
    tz: float = Query(...),
    type: str = Query("marriage", description="Type: marriage, travel, business"),
):
    result = find_muhurats(date, lat, lon, tz, type)
    return {
        "type": type,
        "gpt_summary": result["gpt_summary"],
        "muhurats": result["muhurats"]
    }

# --- Predictions ---

@app.post("/monthly-prediction", tags=["Predictions"])
def monthly_prediction(req: MonthlyRequest):
    return {"monthly_prediction": get_monthly_prediction(req.rashi, req.month)}

@app.post("/weekly-prediction", tags=["Predictions"])
def weekly_prediction(req: WeeklyRequest):
    return {"weekly_prediction": get_weekly_prediction(req.rashi, req.week)}

@app.post("/numerology", tags=["Numerology"])
def numerology(req: NumerologyRequest):
    return {"numerology": get_numerology(req.name, req.dob)}
