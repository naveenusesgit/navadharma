from fastapi import FastAPI, Query
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
    hour: int = Query(..., description="Hour of birth (24h)"),
    minute: int = Query(0, description="Minute of birth"),
    latitude: float = Query(..., description="Latitude of birth"),
    longitude: float = Query(..., description="Longitude of birth"),
):
    chart = generate_kundli_chart(year, month, day, hour, minute, latitude, longitude)
    return chart
