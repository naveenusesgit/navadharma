from fastapi import FastAPI, Query
from utils.kundli import generate_kundli_chart, get_julian_day
import swisseph as swe

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Navadharma KP Astrology API is live 🎉"}

@app.get("/kundli")
def get_kundli(
    year: int = Query(..., description="Birth year"),
    month: int = Query(..., description="Birth month"),
    day: int = Query(..., description="Birth day"),
    hour: int = Query(..., description="Birth hour in 24h format"),
    minute: int = Query(0, description="Birth minute"),
    latitude: float = Query(..., description="Latitude (positive for N, negative for S)"),
    longitude: float = Query(..., description="Longitude (positive for E, negative for W)"),
    tz: float = Query(5.5, description="Timezone offset from UTC (e.g. 5.5 for IST)")
):
    jd = get_julian_day(year, month, day, hour, minute, tz)
    return generate_kundli_chart(jd, latitude, longitude, tz)
