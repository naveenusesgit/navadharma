from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.pdf_generator import generate_pdf
from utils.astro_logic import calculate_astrology_data
from utils.transits import get_current_transits, compare_transits_with_natal
from utils.gpt_summary import generate_gpt_summary
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NAVADHARMA_API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

class KPRequest(BaseModel):
    name: str
    date: str
    time: str
    place: str
    pdf: bool = False
    lang: str = "en"

@app.get("/")
def read_root():
    return {"msg": "🌠 Navadharma Astrology API is Live"}

@app.post("/predict-kp")
async def predict_kp(request: Request, data: KPRequest, x_api_key: str = Header(None)):
    if x_api_key != NAVADHARMA_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Get Lat/Lon and TZ offset
        from utils.geo import get_lat_lon_tz
        lat, lon, tz_offset = get_lat_lon_tz(data.place)

        # Compute Astrology Data
        astro_data = calculate_astrology_data(
            date=data.date, time=data.time, lat=lat, lon=lon, tz_offset=tz_offset
        )

        # Compute Transits
        current_transits = get_current_transits(lat, lon)
        transit_analysis = compare_transits_with_natal(current_transits, astro_data["planetData"])
        gpt_transit_summary = generate_gpt_summary(transit_analysis, lang=data.lang)

        # Generate GPT Summary of the Chart (optional)
        gpt_chart_summary = generate_gpt_summary(astro_data["planetData"], lang=data.lang)

        # Construct Report Data
        report_data = {
            "name": data.name,
            "date": data.date,
            "time": data.time,
            "place": data.place,
            "lagna": astro_data.get("lagna"),
            "currentDasha": astro_data.get("dasha"),
            "planetData": astro_data.get("planetData"),
            "nakshatras": astro_data.get("nakshatras"),
            "yogas": astro_data.get("yogas"),
            "gptSummary": gpt_chart_summary,
            "transits": transit_analysis,
            "gptTransitSummary": gpt_transit_summary,
        }

        if data.pdf:
            pdf_path = generate_pdf(report_data, filename=f"{data.name}_Navadharma_Report.pdf")
            return {"pdf_url": f"/{pdf_path}"}

        return report_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
