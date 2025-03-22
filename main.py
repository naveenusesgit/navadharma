from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.astro_logic import analyze_chart
from utils.transit import get_transits
from utils.match_logic import analyze_compatibility
from utils.pdf_generator import generate_pdf, generate_match_pdf
from utils.gpt_summary import generate_gpt_summary
from utils.numerology import calculate_numerology
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BirthDetails(BaseModel):
    name: str
    date: str
    time: str
    place: str
    lat: float
    lon: float
    lang: str = "en"
    pdf: bool = False

class MatchDetails(BaseModel):
    person1: dict
    person2: dict
    lang: str = "en"
    pdf: bool = False

@app.post("/predict-kp")
async def predict_kp(data: BirthDetails):
    chart_data = analyze_chart(data.date, data.time, data.place, data.lat, data.lon)
    gpt_summary = generate_gpt_summary(chart_data, lang=data.lang)
    numerology = calculate_numerology(data.name, data.date)

    response = {
        "name": data.name,
        "birthDetails": {
            "date": data.date,
            "time": data.time,
            "place": data.place
        },
        "chart": chart_data,
        "summary": gpt_summary,
        "numerology": numerology
    }

    if data.pdf:
        filename = generate_pdf({
            "name": data.name,
            "date": data.date,
            "time": data.time,
            "place": data.place,
            "lagna": chart_data.get("lagna"),
            "currentDasha": chart_data.get("currentDasha"),
            "predictions": gpt_summary
        })
        response["pdf"] = filename

    return response

@app.post("/match-compatibility")
async def match_compatibility(match_data: MatchDetails):
    analysis = analyze_compatibility(match_data.person1, match_data.person2)
    gpt_summary = generate_gpt_summary(analysis, lang=match_data.lang)

    result = {
        "compatibility": analysis,
        "gpt_summary": gpt_summary
    }

    if match_data.pdf:
        filename = generate_match_pdf(match_data.person1, match_data.person2, analysis, gpt_summary)
        result["pdf"] = filename

    return result

@app.get("/daily-transit")
async def daily_transit():
    transit_data = get_transits()
    summary = generate_gpt_summary(transit_data, lang="en")
    return {
        "transits": transit_data,
        "summary": summary
    }

@app.get("/")
async def root():
    return {"message": "🪔 Navadharma API is live and cosmic!"}
