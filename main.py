from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel
from utils.pdf_generator import generate_pdf
from utils.astro_logic import analyze_chart
from utils.gpt_summary import generate_gpt_summary
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

# ------------------ INPUT MODEL ------------------ #

class KPRequest(BaseModel):
    date: str           # Format: YYYY-MM-DD
    time: str           # Format: HH:MM (24h)
    place: str
    lat: float
    lon: float
    pdf: bool = False
    gpt: bool = False


# ------------------ PROTECTED ENDPOINT ------------------ #

@app.post("/predict-kp")
async def predict_kp(request: KPRequest, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # 🌌 Step 1: Analyze chart
    astro = analyze_chart(request.date, request.time, request.lat, request.lon)

    # 📜 Step 2: Build predictions (placeholder logic)
    predictions = {
        "marriage": {
            "likely": True,
            "window": "2024–2025",
            "explanation": "Venus is sub-lord of 7th house and active in Dasha",
            "hidden": True
        },
        "career": {
            "change": False,
            "explanation": "10th lord is stable and unaffected by transit",
            "hidden": True
        }
    }

    # ✨ Step 3: GPT Summary (if requested)
    gpt_summary = ""
    if request.gpt:
        try:
            gpt_summary = generate_gpt_summary(request.date, request.time, request.place, astro)
        except Exception as e:
            gpt_summary = f"GPT error: {str(e)}"

    # 📄 Step 4: Generate PDF (if requested)
    report_data = {
        "date": request.date,
        "time": request.time,
        "place": request.place,
        "lagna": astro.get("lagnaDegree"),
        "nakshatras": astro.get("nakshatras"),
        "dasha": astro.get("dasha", {}),
        "yogas": {
            "Lagna Yogas": astro.get("lagnaYogas", []),
            "Chandra Yogas": astro.get("chandraLagnaYogas", []),
            "Special Yogas": astro.get("specialYogas", [])
        },
        "predictions": predictions,
        "gpt": gpt_summary
    }

    pdf_url = None
    if request.pdf:
        filename = f"Navadharma_Report_{request.date}.pdf"
        filepath = generate_pdf(report_data, filename=filename)
        pdf_url = f"https://navadharma.onrender.com/static/{filename}"

    return {
        "nakshatras": astro.get("nakshatras"),
        "yogas": astro.get("lagnaYogas") + astro.get("chandraLagnaYogas") + astro.get("specialYogas"),
        "planetHouses": astro.get("planetHouses"),
        "gpt_summary": gpt_summary,
        "pdf": pdf_url
    }


@app.get("/")
def root():
    return {"message": "🪔 Navadharma KP Prediction API is live!"}
