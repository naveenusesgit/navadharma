from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY", "kp-demo-secret-key-123456")

class KPInput(BaseModel):
    date: str
    time: str
    place: str

@app.get("/")
def read_root():
    return {
        "message": "👋 Welcome to the KP Predictor API! Use POST /predict-kp to get detailed Vedic astrology predictions using the KP system."
    }

@app.post("/predict-kp")
def predict_kp(request: Request, data: KPInput):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer ") or auth.split(" ")[1] != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "lagna": "Aries",
        "currentDasha": {
            "mahadasha": "Venus",
            "antardasha": "Saturn",
            "period": "2023-08-01 to 2026-05-15"
        },
        "predictions": {
            "marriage": {
                "likely": True,
                "window": "2024–2025",
                "explanation": "Venus is sub-lord of 7th house and active in Dasha"
            },
            "career": {
                "change": False,
                "explanation": "10th lord is stable and unaffected by transit"
            }
        }
    }
