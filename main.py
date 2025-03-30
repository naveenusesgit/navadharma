from fastapi import FastAPI, Query
from utils.kundli import generate_kundli_chart, get_julian_day

app = FastAPI(title="Navadharma KP API", version="1.0")

@app.get("/")
def root():
    return {"message": "🚀 Navadharma KP Astrology API is live and accurate 🎯"}

@app.get("/kundli")
def get_kundli(
    year: int = Query(..., description="Birth year"),
    month: int = Query(..., description="Birth month"),
    day: int = Query(..., description="Birth day"),
    hour: int = Query(12, description="Hour of birth (24h format)"),
    minute: int = Query(0, description="Minute of birth"),
    latitude: float = Query(..., description="Latitude of birth place"),
    longitude: float = Query(..., description="Longitude of birth place"),
    tz: float = Query(5.5, description="Timezone offset from UTC")
):
    jd = get_julian_day(year, month, day, hour, minute)
    chart = generate_kundli_chart(jd, latitude, longitude, tz)
    return chart
