from fastapi import FastAPI, Query
from datetime import datetime
from utils.kundli import (
    get_planet_positions,
    get_lagna_info,
    get_dasha_periods,
    get_nakshatra_details,
    get_planetary_aspects,
    get_transit_predictions,
    generate_kundli_report_pdf,
    generate_full_kundli_prediction,
    get_kundli_chart
)

app = FastAPI(title="Navadharma API")

def get_julian_day(date_str: str) -> float:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.timestamp() / 86400.0 + 2440587.5  # Convert to Julian Day

# ---------- Endpoints ----------

@app.get("/planet-positions")
def planet_positions(date: str = Query(...), lat: float = Query(...), lon: float = Query(...)):
    jd = get_julian_day(date)
    return get_planet_positions(jd, lat, lon)

@app.get("/lagna-info")
def lagna_info(date: str = Query(...), lat: float = Query(...), lon: float = Query(...)):
    jd = get_julian_day(date)
    return get_lagna_info(jd, lat, lon)

@app.get("/dasha-periods")
def dasha_periods(date: str = Query(...), lat: float = Query(...), lon: float = Query(...)):
    jd = get_julian_day(date)
    return get_dasha_periods(jd, lat, lon)

@app.get("/nakshatra-details")
def nakshatra_details(date: str = Query(...), lat: float = Query(...), lon: float = Query(...)):
    jd = get_julian_day(date)
    return get_nakshatra_details(jd, lat, lon)

@app.get("/planetary-aspects")
def planetary_aspects(date: str = Query(...), lat: float = Query(...), lon: float = Query(...)):
    jd = get_julian_day(date)
    return get_planetary_aspects(jd, lat, lon)

@app.get("/transit-predictions")
def transit_predictions(date: str = Query(...), lat: float = Query(...), lon: float = Query(...)):
    jd = get_julian_day(date)
    return get_transit_predictions(jd, lat, lon)

@app.get("/kundli-chart")
def kundli_chart(
    date: str = Query(...),
    lat: float = Query(...),
    lon: float = Query(...),
    divisional_chart: str = Query("D1")
):
    jd = get_julian_day(date)
    return get_kundli_chart(jd, lat, lon, divisional_chart)

@app.get("/generate-full-prediction")
def generate_prediction(date: str = Query(...), lat: float = Query(...), lon: float = Query(...)):
    jd = get_julian_day(date)
    return generate_full_kundli_prediction(jd, lat, lon)

@app.get("/generate-kundli-pdf")
def generate_pdf(date: str = Query(...), lat: float = Query(...), lon: float = Query(...)):
    jd = get_julian_day(date)
    data = generate_full_kundli_prediction(jd, lat, lon)
    return generate_kundli_report_pdf(data)
