from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import swisseph as swe
from utils.match_logic import analyze_compatibility
from datetime import datetime

app = FastAPI(
    title="Navadharma Compatibility API",
    description="Analyzes astrological compatibility between two individuals.",
    version="1.0.0"
)

class CompatibilityInput(BaseModel):
    date1: str  # Format: YYYY-MM-DD
    date2: str  # Format: YYYY-MM-DD

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Navadharma Compatibility API"}

@app.get("/compatibility", tags=["Compatibility"])
def compatibility(date1: str = Query(..., description="First birth date (YYYY-MM-DD)"),
                  date2: str = Query(..., description="Second birth date (YYYY-MM-DD)")):
    try:
        y1, m1, d1 = map(int, date1.split('-'))
        y2, m2, d2 = map(int, date2.split('-'))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    jd1 = swe.julday(y1, m1, d1)
    jd2 = swe.julday(y2, m2, d2)

    result = analyze_compatibility(jd1, jd2)
    return result

