from fastapi import FastAPI, Query
import swisseph as swe
from utils.kundli import generate_kundli_chart

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Navadharma API is live 🎉"}

@app.get("/kundli")
def get_kundli(
    year: int = Query(..., description="Birth year"),
    month: int = Query(..., description="Birth month"),
    day: int = Query(..., description="Birth day"),
    hour: int = Query(12, description="Hour of birth (24h)"),
    minute: int = Query(0, description="Minute of birth"),
    latitude: float = Query(..., description="Latitude of birth"),
    longitude: float = Query(..., description="Longitude of birth"),
    tz: float = Query(5.5, description="Timezone offset from UTC"),
    system: str = Query("vedic", enum=["vedic", "kp"], description="Astrological system: vedic or kp")
):
    jd = swe.julday(year, month, day, hour + (minute / 60.0))
    chart = generate_kundli_chart(jd, latitude, longitude, tz, system)
    return chart
