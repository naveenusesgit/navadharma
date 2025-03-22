from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import requests
import openai
from utils.pdf_generator import generate_pdf
from utils.astro_logic import (
    get_lat_lon, get_julian_day, get_moon_nakshatra,
    get_sample_yogas, get_dasha
)
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("NAVADHARMA_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ✅ Request model
class KPRequest(BaseModel):
    name: Optional[str] = "User"
    date: str  # YYYY-MM-DD
    time: str  # HH:MM (24h)
    place: str
    pdf: Optional[bool] = False

# ✅ API Key verification
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# ✅ GPT-powered summary
def generate_gpt_summary(data):
    try:
        prompt = f"""You're a wise Vedic astrologer. Given this data:
        Nakshatra: {data['nakshatra']['nakshatra']},
        Mahadasha: {data['currentDasha']['mahadasha']},
        Yogas: {', '.join([y['name'] for y in data['nakshatra']['yogas']])}
        Give a short, elegant prediction."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "GPT prediction unavailable."

# ✅ Predict endpoint
@app.post("/predict-kp", dependencies=[Depends(verify_api_key)])
async def predict_kp(req: KPRequest):
    # 🌍 Get lat/lon from place
    lat, lon = get_lat_lon(req.place)

    # 📆 Julian Day from date/time
    jd = get_julian_day(req.date, req.time)

    # 🌓 Nakshatra, Dasha, Yogas
    nakshatra = get_moon_nakshatra(jd)
    yogas = get_sample_yogas(jd)
    dasha = get_dasha(jd)

    # 📦 Full Data Bundle
    report_data = {
        "name": req.name,
        "date": req.date,
        "time": req.time,
        "place": req.place,
        "lagna": "Aries",  # Optional: Add real calculation
        "currentDasha": dasha,
        "nakshatra": {
            "nakshatra": nakshatra,
            "nakshatra_lord": "Ketu",  # Example
            "yogas": yogas
        },
        "predictions": {
            "marriage": {
                "likely": True,
                "window": "2024–2025",
                "explanation": "Venus sub-lord active in Dasha.",
                "hidden": True
            },
            "career": {
                "change": False,
                "explanation": "10th house lord stable.",
                "hidden": True
            },
            "gpt_summary": generate_gpt_summary({
                "nakshatra": {"nakshatra": nakshatra, "yogas": yogas},
                "currentDasha": dasha
            })
        }
    }

    # 📄 Generate PDF if needed
    if req.pdf:
        filename = f"{req.name.replace(' ', '_')}_Navadharma_Report.pdf"
        pdf_path = generate_pdf(report_data, filename=filename)
        return {
            "success": True,
            "data": report_data,
            "pdf_url": f"https://navadharma.onrender.com/{pdf_path}"
        }

    return {"success": True, "data": report_data}

