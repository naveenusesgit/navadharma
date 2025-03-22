from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from utils.pdf_generator import generate_pdf
from utils.swisseph_utils import calculate_planet_positions
from openai import OpenAI
from dotenv import load_dotenv
import os

# 🌍 Load environment variables (OPENAI_API_KEY etc.)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()

# 🧾 Request model
class KPRequest(BaseModel):
    date: str
    time: str
    place: str
    pdf: bool = False
    persona: str = "vedic_sage"

# 🧠 GPT Summary Function
def generate_gpt_summary(data, persona="vedic_sage"):
    system_prompt = {
        "vedic_sage": "You are a wise Vedic astrologer using deep yogas, dasha, and planetary karma insights.",
        "cool_astro_bro": "You are a witty Gen-Z astrologer who makes karma cool and predictions accessible.",
        "fortune_teller": "You're a dramatic astrologer who speaks like an oracle with prophecy-like tone."
    }

    messages = [
        {"role": "system", "content": system_prompt.get(persona, system_prompt["vedic_sage"])},
        {"role": "user", "content": f"""
Lagna: {data.get('lagna')}
Mahadasha: {data.get('currentDasha', {}).get('mahadasha')}
Nakshatra: {data.get('nakshatra', {}).get('nakshatra')}
Yogas: {data.get('nakshatra', {}).get('yogas', [])}
Planetary Positions: {data.get('planet_positions')}
Remedies: {data.get('remedies')}
Divisional Charts: {data.get('divisional_charts')}
        """}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.85,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error from GPT: {str(e)}"

# 🎯 Main Prediction Endpoint
@app.post("/predict-kp")
async def predict_kp(req: KPRequest):
    # 🌠 Prepare prediction data (mocked for now)
    data = {
        "date": req.date,
        "time": req.time,
        "place": req.place,
        "lagna": "Aries",
        "currentDasha": {
            "mahadasha": "Venus",
            "antardasha": "Saturn",
            "period": "2023-08-01 to 2026-05-15"
        },
        "nakshatra": {
            "nakshatra": "Ashwini",
            "nakshatra_lord": "Ketu",
            "yogas": [
                {"name": "Chandra-Mangal Yoga", "effect": "Gives financial intuition."},
                {"name": "Budha-Aditya Yoga", "effect": "Sharp intellect and communication skills."}
            ]
        },
        "remedies": [
            "Chant 'Om Shukraya Namah' on Fridays",
            "Donate white sweets to unmarried women"
        ],
        "divisional_charts": {
            "D9 (Navamsa)": {"ascendant": "Sagittarius", "notes": "Focus on dharma and partnerships"},
            "D10 (Dasamsa)": {"ascendant": "Libra", "notes": "Career through diplomacy or beauty"}
        }
    }

    # 🪐 Calculate Real Planetary Positions
    # (Assume Mumbai for now — update with real geocoding later)
    lat, lon = 19.0760, 72.8777
    data["planet_positions"] = calculate_planet_positions(req.date, req.time, lat, lon)

    # 🧠 GPT Summary
    data["summary"] = generate_gpt_summary(data, persona=req.persona)

    if req.pdf:
        pdf_path = generate_pdf(data, filename="Navadharma_Report.pdf")
        return FileResponse(pdf_path, media_type="application/pdf", filename="Navadharma_Report.pdf")

    return JSONResponse(content=data)
