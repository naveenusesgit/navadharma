from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from utils.pdf_generator import generate_pdf
from utils.astro_logic import generate_full_kp_report
from utils.numerology import get_numerology_summary
from utils.transit import get_today_transits, get_gpt_transit_summary
from utils.gpt_summary import gpt_summary

load_dotenv()

API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")
app = FastAPI()

# Allow all origins for testing (limit this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KPRequest(BaseModel):
    name: str
    date: str       # format YYYY-MM-DD
    time: str       # format HH:MM
    place: str
    pdf: bool = True
    lang: str = "en"

@app.post("/predict-kp")
async def predict_kp(req: KPRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Main Astro Report
    report_data = generate_full_kp_report(
        name=req.name,
        date=req.date,
        time=req.time,
        place=req.place,
        lang=req.lang
    )

    # Numerology
    numerology = get_numerology_summary(req.name, req.date)
    report_data["numerology"] = numerology

    # GPT Summary
    summary = await gpt_summary(report_data, lang=req.lang)
    report_data["gpt_summary"] = summary

    if req.pdf:
        filepath = generate_pdf(report_data, filename="Navadharma_Report.pdf")
        return FileResponse(filepath, media_type='application/pdf', filename="Navadharma_Report.pdf")
    
    return report_data

@app.get("/daily-transit")
async def daily_transit():
    transits = get_today_transits()
    gpt = await get_gpt_transit_summary(transits)
    return {
        "transits": transits,
        "gpt_summary": gpt
    }

@app.get("/")
async def root():
    return {"status": "🌠 Navadharma Astro API is live"}
