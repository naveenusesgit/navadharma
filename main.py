from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from utils.astro_engine import compute_full_chart
from utils.astro_logic import detect_yogas, get_nakshatras, get_remedies
from utils.gpt_summary import generate_gpt_summary
from utils.pdf_generator import generate_pdf
from utils.transit import get_current_transits
from utils.match_logic import compute_match_score
from utils.email_utils import send_report_email

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

NAVADHARMA_API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

class KPInput(BaseModel):
    name: str
    date: str
    time: str
    place: str
    language: str = "en"
    pdf: bool = False
    paid: bool = False
    email: str | None = None
    partner: dict | None = None


@app.post("/predict-kp")
async def predict_kp(req: Request, input: KPInput):
    api_key = req.headers.get("x-api-key")
    if api_key != NAVADHARMA_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Step 1: Core Chart Data
    full_chart = compute_full_chart(input.date, input.time, input.place)

    # Step 2: Yogas, Nakshatra, Dasha
    yogas = detect_yogas(full_chart["planet_positions"], full_chart["moon"], full_chart["lagna_sign"])
    nakshatras = get_nakshatras(full_chart["planet_longitudes"], full_chart["nakshatra_list"])
    remedies = get_remedies(yogas=yogas, dashas=[full_chart["dasha"]], nakshatras=list(nakshatras.values()), language=input.language)

    # Step 3: GPT Summary
    gpt_summary = generate_gpt_summary(full_chart, yogas, nakshatras, language=input.language)

    # Step 4: Transit
    transit = get_current_transits()

    # Step 5: Match-making (optional)
    match_score = None
    match_summary = None
    if input.partner:
        match_score, match_summary = compute_match_score(full_chart, input.partner)

    # Step 6: Build data
    result = {
        "name": input.name,
        "date": input.date,
        "time": input.time,
        "place": input.place,
        "planet_positions": full_chart["planet_positions"],
        "nakshatras": nakshatras,
        "yogas": yogas,
        "dasha": full_chart["dasha"],
        "gpt_summary": gpt_summary,
        "transit": transit,
        "remedies": remedies,
        "match_score": match_score,
        "match_summary": match_summary
    }

    # Step 7: PDF
    if input.pdf:
        filename = f"{input.name.replace(' ', '_')}_Navadharma_Report.pdf"
        path = generate_pdf(result, filename=filename, remedies=remedies, language=input.language)
        result["pdf_path"] = f"/static/{filename}"

    # Step 8: Email report (paid only)
    if input.paid and input.email:
        try:
            send_report_email(input.email, path)
            result["email_status"] = "sent"
        except Exception as e:
            result["email_status"] = f"failed: {str(e)}"

    return result


@app.get("/daily-transit")
def daily_transit():
    return {
        "transit": get_current_transits()
    }
