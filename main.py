from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from utils.location_utils import get_coordinates
from utils.astro_utils import compute_astro_data
from utils.astro_logic import extract_yogas, extract_nakshatras, analyze_moon_lagna_combinations
from utils.divisional_charts import get_divisional_chart_data, render_divisional_chart
from utils.transit import get_today_transits, get_gpt_transit_summary
from utils.numerology import get_numerology_profile
from utils.gpt_summary import generate_gpt_summary
from utils.pdf_generator import generate_pdf

load_dotenv()

# Auth check
NAVADHARMA_API_KEY = os.getenv("NAVADHARMA_API_KEY")

app = FastAPI()

# CORS for browser-based testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class PredictionRequest(BaseModel):
    name: Optional[str] = "User"
    date: str
    time: str
    place: str
    language: Optional[str] = "en"
    pdf: Optional[bool] = False
    chartStyle: Optional[str] = "south"
    charts: Optional[list[str]] = ["D1", "D9", "D10"]

@app.post("/predict-kp")
async def predict_kp(req: Request, body: PredictionRequest):
    # 🔐 API key auth
    auth_header = req.headers.get("Authorization")
    if auth_header != f"Bearer {NAVADHARMA_API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API key.")

    # 🌐 Convert place to coordinates
    lat, lon = get_coordinates(body.place)
    if not lat or not lon:
        raise HTTPException(status_code=400, detail="Invalid place name.")

    # 🧠 Astro core logic
    astro_data = compute_astro_data(body.date, body.time, lat, lon)
    nakshatras = extract_nakshatras(astro_data)
    yogas = extract_yogas(astro_data)
    moon_lagna_logic = analyze_moon_lagna_combinations(astro_data)

    # 📊 Divisional chart logic
    divisional_charts = {}
    for chart in body.charts:
        divisional_charts[chart] = get_divisional_chart_data(body.date, body.time, lat, lon, chart)
        render_divisional_chart(divisional_charts[chart], chart, body.chartStyle)

    # 🔮 Numerology
    numerology = get_numerology_profile(body.name, body.date)

    # 🌠 GPT summary
    gpt_summary = generate_gpt_summary(
        language=body.language,
        astro_data=astro_data,
        yogas=yogas,
        nakshatras=nakshatras,
        numerology=numerology,
        moon_lagna_logic=moon_lagna_logic
    )

    # 🧾 Optionally generate PDF
    filepath = None
    if body.pdf:
        filepath = generate_pdf({
            "name": body.name,
            "date": body.date,
            "time": body.time,
            "place": body.place,
            "lagna": astro_data.get("lagna"),
            "currentDasha": astro_data.get("current_dasha"),
            "nakshatras": nakshatras,
            "yogas": yogas,
            "numerology": numerology,
            "moonLagnaLogic": moon_lagna_logic,
            "gptSummary": gpt_summary,
            "chartsGenerated": body.charts
        }, filename=f"{body.name}_Navadharma_Report.pdf")

    return {
        "status": "ok",
        "summary": gpt_summary,
        "nakshatras": nakshatras,
        "yogas": yogas,
        "numerology": numerology,
        "moonLagnaLogic": moon_lagna_logic,
        "charts": body.charts,
        "pdf_url": filepath
    }

@app.get("/daily-transit")
async def daily_transit(lang: Optional[str] = Query("en")):
    transit_data = get_today_transits()
    gpt_transit_summary = get_gpt_transit_summary(transit_data, lang=lang)
    return {
        "date": transit_data.get("date"),
        "transits": transit_data,
        "gpt_summary": gpt_transit_summary
    }

@app.get("/")
async def root():
    return {"status": "Navadharma API running ✅"}
