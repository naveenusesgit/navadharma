from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from utils.pdf_generator import generate_pdf
from utils.astro_logic import get_astrology_data
from utils.gpt_summary import generate_gpt_summary
from utils.numerology import get_numerology_profile
from utils.transit import get_current_transits
from utils.compatibility import generate_match_report
from utils.match_pdf import generate_match_pdf

load_dotenv()

API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

app = FastAPI(title="Navadharma Astrology API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KPRequest(BaseModel):
    date: str
    time: str
    place: str
    language: str = "en"
    pdf: bool = False
    includeCharts: bool = True
    chartStyle: str = "south"

class MatchRequest(BaseModel):
    boy: dict
    girl: dict
    language: str = "en"
    pdf: bool = False

def verify_api_key(request: Request):
    client_key = request.headers.get("X-API-Key")
    if client_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/")
def home():
    return {"status": "Navadharma Astrology API is live 🌠"}

@app.post("/predict-kp")
def predict_kp(data: KPRequest, request: Request = Depends(verify_api_key)):
    astro_data = get_astrology_data(data.date, data.time, data.place, chart_style=data.chartStyle)
    numerology = get_numerology_profile(data.date, data.time)
    gpt_summary = generate_gpt_summary(astro_data, numerology, lang=data.language)
    transit_data = get_current_transits()

    full_data = {
        **astro_data,
        "numerology": numerology,
        "gptSummary": gpt_summary,
        "transits": transit_data,
        "language": data.language,
        "date": data.date,
        "time": data.time,
        "place": data.place,
    }

    response = {"data": full_data}

    if data.pdf:
        filepath = generate_pdf(full_data)
        response["pdf_url"] = f"/{filepath}"

    return response

@app.post("/match-compatibility")
def match_compatibility(data: MatchRequest, request: Request = Depends(verify_api_key)):
    report = generate_match_report(data.boy, data.girl, data.language)

    response = {"compatibility": report}

    if data.pdf:
        pdf_path = generate_match_pdf(report, data.boy, data.girl)
        response["pdf_url"] = f"/{pdf_path}"

    return response

@app.get("/daily-transit")
def daily_transit(request: Request = Depends(verify_api_key)):
    return {"transits": get_current_transits()}
