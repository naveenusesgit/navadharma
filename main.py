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
def suggest_remedies(data):
    remedies = []

    if "Ketu" in data.get("nakshatra", {}).get("nakshatra_lord", ""):
        remedies.append("Recite Ketu Beej Mantra on Tuesdays.")
        remedies.append("Donate sesame seeds and blankets to the poor.")

    if any(yoga["name"] == "Raja Yoga" for yoga in data.get("nakshatra", {}).get("yogas", [])):
        remedies.append("Wear Yellow Sapphire (if horoscope supports it).")

    if data.get("currentDasha", {}).get("mahadasha") == "Venus":
        remedies.append("Worship Goddess Lakshmi every Friday.")

    return remedies

def generate_gpt_summary(data):
    messages = [
        {"role": "system", "content": "You are a traditional Vedic astrologer who uses KP astrology, divisional charts, and nakshatras to guide people. Your tone is spiritual yet clear."},
        {"role": "user", "content": f"""
Analyze this birth chart and provide a spiritual 4-line prediction.

Date: {data.get('date')}
Time: {data.get('time')}
Place: {data.get('place')}
Lagna: {data.get('lagna')}
Mahadasha: {data.get('currentDasha', {}).get('mahadasha')}
Antardasha: {data.get('currentDasha', {}).get('antardasha')}
Nakshatra: {data.get('nakshatra', {}).get('nakshatra')}
Yogas: {data.get('nakshatra', {}).get('yogas', [])}
Remedies: {data.get('remedies')}
D9: {data.get('divisional_charts', {}).get('D9')}
D10: {data.get('divisional_charts', {}).get('D10')}
        """}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error from GPT: {str(e)}"
