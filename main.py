from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.pdf_generator import generate_pdf
from utils.astro_logic import get_full_astrology_data
from utils.gpt_summary import generate_gpt_summary
from utils.email_utils import send_email_with_attachment
from utils.match_logic import match_compatibility
from utils.numerology import numerology_profile
from utils.transit import get_current_transits
import os

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protect with API key
API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

def verify_key(request: Request):
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/predict-kp")
async def predict_kp(request: Request, payload: dict):
    verify_key(request)

    name = payload.get("name", "User")
    date = payload.get("date")
    time = payload.get("time")
    place = payload.get("place")
    lang = payload.get("lang", "en")
    send_pdf = payload.get("pdf", False)
    email = payload.get("email")

    if not (date and time and place):
        raise HTTPException(status_code=400, detail="Missing date, time, or place.")

    # Astrology logic
    astro_data = get_full_astrology_data(date, time, place)

    # GPT Summary
    gpt_prompt = f"Generate a short astrological summary for {name}, born on {date} at {time} in {place}. Lagna: {astro_data.get('lagna')}, Dasha: {astro_data.get('currentDasha')}."
    gpt_summary = generate_gpt_summary(gpt_prompt, lang=lang)

    # Numerology
    numerology = numerology_profile(name, date)

    # Transit
    transits = get_current_transits()

    # Final report data
    report_data = {
        "name": name,
        "date": date,
        "time": time,
        "place": place,
        **astro_data,
        "gptSummary": gpt_summary,
        "numerology": numerology,
        "transits": transits
    }

    if send_pdf:
        filename = f"{name}_Navadharma_Report.pdf"
        filepath = generate_pdf(report_data, filename=filename)

        if email:
            send_email_with_attachment(email, filepath)

        return {"success": True, "pdf": filepath, "summary": gpt_summary}

    return report_data


@app.post("/match-compatibility")
def match_report(request: Request, payload: dict):
    verify_key(request)

    p1 = payload.get("partner1", {})
    p2 = payload.get("partner2", {})
    lang = payload.get("lang", "en")

    match_data = match_compatibility(p1, p2)

    match_data["numerology"] = {
        "partner1": numerology_profile(p1.get("name", ""), p1.get("date", "")),
        "partner2": numerology_profile(p2.get("name", ""), p2.get("date", ""))
    }

    prompt = f"""
    Match compatibility:
    Partner 1: {p1.get('name')} ({p1.get('date')})
    Partner 2: {p2.get('name')} ({p2.get('date')})
    Score: {match_data['ashtakootScore']} / 36
    Dasha: {match_data['dashaCompatibility']}
    Remedies: {', '.join(match_data['remedies'])}
    Write a relationship prediction in {lang}.
    """

    match_data["gptSummary"] = generate_gpt_summary(prompt, lang=lang)
    return match_data


@app.get("/daily-transit")
def daily_transits(request: Request):
    verify_key(request)
    return get_current_transits()
