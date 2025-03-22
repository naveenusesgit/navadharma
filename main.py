from fastapi import FastAPI, Request, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from datetime import datetime
from utils.astro_logic import analyze_chart
from utils.pdf_generator import generate_pdf
from utils.gpt_summary import generate_gpt_summary
from utils.match_logic import analyze_compatibility
from utils.numerology import get_numerology_report
from utils.transit import get_transits

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionInput(BaseModel):
    name: str
    date: str
    time: str
    place: str
    lat: float
    lon: float
    tz: str
    lang: str = "en"
    pdf: bool = False

class MatchInput(BaseModel):
    person1: dict
    person2: dict
    lang: str = "en"
    pdf: bool = False

@app.post("/predict-kp")
def predict_kp(data: PredictionInput):
    astro_data = analyze_chart(
        name=data.name,
        date=data.date,
        time=data.time,
        place=data.place,
        lat=data.lat,
        lon=data.lon,
        tz=data.tz
    )
    numerology = get_numerology_report(data.name, data.date)
    gpt_summary = generate_gpt_summary(astro_data, lang=data.lang)

    result = {
        "astro": astro_data,
        "numerology": numerology,
        "summary": gpt_summary,
    }

    if data.pdf:
        filepath = generate_pdf(
            {
                "name": data.name,
                "date": data.date,
                "time": data.time,
                "place": data.place,
                "astro": astro_data,
                "numerology": numerology,
                "gpt": gpt_summary
            },
            filename=f"{data.name.replace(' ', '_')}_report.pdf"
        )
        return FileResponse(filepath, filename=os.path.basename(filepath))

    return result

@app.post("/match-compatibility")
def match_compatibility(match: MatchInput):
    match_data = analyze_compatibility(match.person1, match.person2)
    summary = generate_gpt_summary(match_data, lang=match.lang, type="match")

    result = {
        "match": match_data,
        "summary": summary
    }

    # PDF support if needed later
    return result

@app.get("/daily-transit")
def daily_transit(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    timezone: str = Query("Asia/Kolkata", description="Timezone"),
    lang: str = Query("en", description="Language for GPT summary")
):
    now = datetime.now()
    transits = get_transits(now, lat, lon, timezone)
    gpt_summary = generate_gpt_summary(transits, lang=lang, type="transit")

    return {
        "date": now.strftime("%Y-%m-%d %H:%M"),
        "location": {"lat": lat, "lon": lon, "timezone": timezone},
        "transits": transits,
        "summary": gpt_summary
    }
