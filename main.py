from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils.kundli import generate_kundli_chart

app = FastAPI(title="Navadharma Jyotish API", version="1.0.0")

# 📦 Input schema
class KundliRequest(BaseModel):
    datetime: str  # ISO format e.g. "1990-07-16T04:30:00"
    latitude: float
    longitude: float
    timezone: Optional[float] = 5.5  # default IST
    place: Optional[str] = "India"

# ✅ Root health check
@app.get("/")
def root():
    return {"message": "🕉️ Navadharma Jyotish API is online."}

# ✅ Basic health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 🧠 Generate Kundli chart using Swiss Ephemeris + KP Ayanamsa
@app.post("/generate-kundli-chart")
def generate_kundli(req: KundliRequest):
    try:
        result = generate_kundli_chart(req.dict())
        return {"kundli_chart": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kundli generation error: {str(e)}")
