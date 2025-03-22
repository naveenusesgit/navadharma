from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils.pdf_generator import generate_pdf
from utils.geo import resolve_location
from utils.astro import get_planet_positions, get_nakshatras, get_dasha_periods
from utils.yogas import find_yogas
from utils.gpt_summary import generate_gpt_summary
from utils.divisional_charts import calculate_divisional_chart, plot_chart
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class KPInput(BaseModel):
    name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str
    language: str = "en"
    pdf: bool = False
    chartStyle: str = "south"

@app.post("/predict-kp")
async def predict_kp(payload: KPInput):
    try:
        name = payload.name
        date_str = payload.date
        time_str = payload.time
        place = payload.place
        lang = payload.language
        want_pdf = payload.pdf
        style = payload.chartStyle.lower()

        # 🌐 1. Resolve coordinates and timezone
        geo_data = resolve_location(place, date_str, time_str)
        lat, lon, tz, local_dt = geo_data["lat"], geo_data["lon"], geo_data["tz"], geo_data["datetime"]

        # 🪐 2. Planet positions
        planet_data, jd = get_planet_positions(local_dt, lat, lon)

        # 🌌 3. Nakshatras & Chandra lagna
        nakshatra_data, chandra_lagna = get_nakshatras(planet_data)

        # 🔢 4. Vimshottari Dasha
        dasha_info = get_dasha_periods(jd)

        # 🧘 5. Yogas & Combinations
        yoga_results = find_yogas(planet_data, chandra_lagna)

        # 🧠 6. GPT Summary
        gpt_summary = generate_gpt_summary(name, planet_data, dasha_info, nakshatra_data, yoga_results, lang)

        # 🪔 7. Divisional Charts (D3–D60)
        div_charts = {}
        for chart_type in ["D3", "D7", "D9", "D10", "D12", "D24", "D60"]:
            chart = calculate_divisional_chart(jd, lat, lon, chart_type)
            chart_path = plot_chart(chart, f"{chart_type} Chart", f"{chart_type.lower()}_chart.png", style=style)
            div_charts[chart_type] = chart_path

        # 📄 8. Assemble Report Data
        report_data = {
            "name": name,
            "date": date_str,
            "time": time_str,
            "place": place,
            "planetData": planet_data,
            "nakshatras": nakshatra_data,
            "currentDasha": dasha_info,
            "lagna": planet_data.get("Ascendant", "Unknown"),
            "yogas": yoga_results,
            "gptSummary": gpt_summary,
            "divisionalCharts": div_charts,
        }

        if want_pdf:
            pdf_path = generate_pdf(report_data, filename="Navadharma_Report.pdf")
            return FileResponse(pdf_path, media_type="application/pdf", filename="Navadharma_Report.pdf")

        return {
            "name": name,
            "location": {"lat": lat, "lon": lon, "tz": tz},
            "planets": planet_data,
            "nakshatras": nakshatra_data,
            "dasha": dasha_info,
            "yogas": yoga_results,
            "summary": gpt_summary,
            "charts": list(div_charts.keys()),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "🌠 Navadharma Astrology API is running"}
