from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.astro_logic import calculate_astro_details
from utils.pdf_generator import generate_pdf
from utils.gpt_summary import generate_gpt_summary
from utils.transit import get_current_transits
from utils.numerology import numerology_profile
from utils.match_logic import match_compatibility
import os

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

# ---------------- Models ----------------

class KPRequest(BaseModel):
    name: str
    date: str
    time: str
    place: str
    pdf: bool = False
    lang: str = "en"

class MatchRequest(BaseModel):
    partner1: dict
    partner2: dict
    pdf: bool = False
    lang: str = "en"

# ---------------- Auth ----------------

def verify_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# ---------------- Endpoints ----------------

@app.post("/predict-kp")
async def predict_kp(request: Request, payload: KPRequest):
    verify_key(request)
    data = payload.dict()

    astro = calculate_astro_details(data)
    summary = generate_gpt_summary(astro, lang=data["lang"])
    astro["gptSummary"] = summary

    if data["pdf"]:
        pdf_path = generate_pdf(astro, filename="Navadharma_Report.pdf")
        return FileResponse(pdf_path, media_type="application/pdf", filename="Navadharma_Report.pdf")

    return astro


@app.post("/match-compatibility")
async def match_compat(request: Request, payload: MatchRequest):
    verify_key(request)

    data = payload.dict()
    p1 = data["partner1"]
    p2 = data["partner2"]

    match = match_compatibility(p1, p2)
    match["numerology"] = {
        "partner1": numerology_profile(p1.get("name", ""), p1.get("date", "")),
        "partner2": numerology_profile(p2.get("name", ""), p2.get("date", ""))
    }

    if data["pdf"]:
        from utils.pdf_generator import generate_match_pdf
        path = generate_match_pdf(match, filename="Match_Report.pdf")
        return FileResponse(path, media_type="application/pdf", filename="Match_Report.pdf")

    return match


@app.get("/daily-transit")
async def daily_transit(request: Request):
    verify_key(request)
    return get_current_transits()
