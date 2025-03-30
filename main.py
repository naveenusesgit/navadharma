from fastapi import FastAPI, Query
from utils.kundli import generate_kundli_chart, compute_julian_day

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Navadharma KP API is live 🎯"}

@app.get("/kundli")
def get_kundli(
    year: int = Query(..., description="Birth year"),
    month: int = Query(..., description="Birth month"),
    day: int = Query(..., description="Birth day"),
    hour: int = Query(..., description="Hour of birth (24h format)"),
    minute: int = Query(0, description="Minute of birth"),
    latitude: float = Query(..., description="Latitude of birthplace"),
    longitude: float = Query(..., description="Longitude of birthplace"),
    tz: float = Query(5.5, description="Timezone offset from UTC (e.g., 5.5 for IST)")
):
    jd = compute_julian_day(year, month, day, hour, minute, tz)
    return generate_kundli_chart(jd, latitude, longitude, tz)
