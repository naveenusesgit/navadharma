from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from utils.geolocation import get_lat_lon_timezone
from utils.astro_logic import get_astro_insights
from utils.pdf_generator import generate_pdf
from utils.gpt_summary import generate_gpt_summary

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    name: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    place: str
    pdf: bool = False
    language: str = "English"
    api_key: str = ""

@app.get("/")
def root():
    return {"message": "🌠 Navadharma KP Astrology API is running."}

@app.post("/predict-kp")
def predict_kp(data: UserInput):
    # ✅ API key validation
    expected_key = os.getenv("NAVADHARMA_API_KEY")
    if data.api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        # 🌍 Get lat/lon and timezone
        lat, lon, timezone_str = get_lat_lon_timezone(data.place)

        # 🔭 Generate full astrology data
        astro = get_astro_insights(
            name=data.name,
            date=data.date,
            time=data.time,
            lat=lat,
            lon=lon,
            timezone_str=timezone_str
        )

        # 🌐 GPT prediction summary
        gpt_summary = generate_gpt_summary(astro.get("summaryText", ""), language=data.language)

        # 📄 Prepare report data
        report_data = {
            "name": data.name,
            "date": data.date,
            "time": data.time,
            "place": data.place,
            "lagna": astro.get("lagna"),
            "currentDasha": astro.get("dasha"),
            "planets": astro.get("planets"),
            "nakshatras": astro.get("nakshatras"),
            "yogas": astro.get("yogas"),
            "divisionalCharts": astro.get("divisionalCharts"),
            "gptSummary": gpt_summary,
            "predictions": astro.get("predictions", {}),
        }

        pdf_path = None
        if data.pdf:
            pdf_path = generate_pdf(report_data, filename="Navadharma_Report.pdf")

        return {
            "status": "✅ Success",
            "summary": gpt_summary,
            "data": report_data,
            "pdf_url": pdf_path if pdf_path else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
