# main.py

from fastapi import FastAPI, Query
from utils.kundli import generate_kundli_chart

app = FastAPI(title="Jyotish-as-a-Service 🔮")

@app.get("/kundli")
def kundli(
    name: str = Query(...),
    date: str = Query(..., description="Format: YYYY-MM-DD"),
    time: str = Query(..., description="Format: HH:MM (24h)"),
    place: str = Query(...),
):
    return generate_kundli_chart(name, date, time, place)
