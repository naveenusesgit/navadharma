from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.pdf_generator import generate_pdf
from openai import OpenAI
from datetime import datetime
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PredictionRequest(BaseModel):
    date: str
    time: str
    place: str
    pdf: bool = False

@app.post("/predict-kp")
def predict_kp(req: PredictionRequest):
    data = req.dict()

    # ✅ Lagna + Dasha (mocked)
    data["lagna"] = "Aries"
    data["currentDasha"] = {
        "mahadasha": "Venus",
        "antardasha": "Saturn",
        "period": "2023-08-01 to 2026-05-15"
    }

    # ✅ Nakshatra + Yogas (mocked)
    data["nakshatra"] = {
        "nakshatra": "Ashwini",
        "nakshatra_lord": "Ketu",
        "yogas": [
            {"name": "Raja Yoga", "effect": "Power and influence in career"},
            {"name": "Gaja Kesari Yoga", "effect": "Wisdom and popularity"}
        ]
    }

    # ✅ Divisional charts
    data["divisional_charts"] = {
        "D9": {
            "ascendant": "Libra",
            "notes": "Strong partnership energy, love/marriage focus"
        },
        "D10": {
            "ascendant": "Capricorn",
            "notes": "Career progress slow but steady, gains in service"
        }
    }

    # ✅ Remedies
    data["remedies"] = suggest_remedies(data)

    # ✅ GPT Summary
    data["summary"] = generate_gpt_summary(data)

    # ✅ Optional PDF
    if data.get("pdf"):
        filename = "Navadharma_Report.pdf"
        filepath = generate_pdf(data, filename=filename)
        return {"summary": data["summary"], "pdf_url": f"/static/{filename}"}

    return data
