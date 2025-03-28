from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.kundli import generate_kundli_chart

app = FastAPI(title="Navadharma Jyotish API")

class KundliRequest(BaseModel):
    name: str
    birth_date: str  # Format: YYYY-MM-DD
    birth_time: str  # Format: HH:MM (24hr)
    place: str       # City name or location string

@app.post("/get-kundli-chart")
def get_kundli_chart(req: KundliRequest):
    try:
        result = generate_kundli_chart(
            name=req.name,
            birth_date=req.birth_date,
            birth_time=req.birth_time,
            place=req.place
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
