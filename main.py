from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from utils.astro_logic import get_astrology_data
from utils.pdf_generator import generate_pdf
from utils.gpt_summary import generate_gpt_summary
from utils.transit import get_transit_data
from utils.match_logic import analyze_match_compatibility
from utils.numerology import generate_numerology
from utils.remedies import get_remedies_from_gpt

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

class BirthDetails(BaseModel):
    name: str
    date: str
    time: str
    place: str
    lang: str = "en"
    pdf: bool = False

class MatchDetails(BaseModel):
    person1: BirthDetails
    person2: BirthDetails

@app.post("/predict-kp")
async def predict_kp(details: BirthDetails, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 1. Generate Astro Logic
    astro_data = get_astrology_data(details.date, details.time, details.place)

    # 2. Generate GPT-based Summary
    summary = generate_gpt_summary(astro_data, lang=details.lang)

    # 3. Remedies
    remedies = get_remedies_from_gpt(astro_data, lang=details.lang)

    # 4. Numerology
    numerology = generate_numerology(details.name, details.date)

    # 5. Transit
    transit = get_transit_data(details.date, details.time, details.place)

    report_data = {
        "name": details.name,
        "date": details.date,
        "time": details.time,
        "place": details.place,
        "summary": summary,
        "remedies": remedies,
        "numerology": numerology,
        **astro_data,
        "transit": transit
    }

    if details.pdf:
        filepath = generate_pdf(report_data, filename="Navadharma_Report.pdf")
        return FileResponse(filepath, media_type="application/pdf", filename="Navadharma_Report.pdf")
    
    return report_data

@app.post("/match-compatibility")
async def match_compatibility(data: MatchDetails, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    result = analyze_match_compatibility(data.person1, data.person2)

    # Remedies and GPT summary for each person
    p1_remedy = get_remedies_from_gpt(result["person1"]["astro"], lang=data.person1.lang)
    p2_remedy = get_remedies_from_gpt(result["person2"]["astro"], lang=data.person2.lang)

    p1_summary = generate_gpt_summary(result["person1"]["astro"], lang=data.person1.lang)
    p2_summary = generate_gpt_summary(result["person2"]["astro"], lang=data.person2.lang)

    result["person1"]["remedies"] = p1_remedy
    result["person2"]["remedies"] = p2_remedy
    result["person1"]["summary"] = p1_summary
    result["person2"]["summary"] = p2_summary

    if data.person1.pdf or data.person2.pdf:
        pdf_path = generate_pdf(result, filename="Navadharma_Match_Report.pdf", is_match=True)
        return FileResponse(pdf_path, media_type="application/pdf", filename="Navadharma_Match_Report.pdf")

    return result

@app.get("/daily-transit")
async def daily_transit():
    return get_transit_data()
