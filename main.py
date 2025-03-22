from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import FileResponse, JSONResponse
from utils.pdf_generator import generate_pdf
import os

app = FastAPI()

# Optional: allow CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input structure
class PredictionRequest(BaseModel):
    date: str
    time: str
    place: str
    pdf: Optional[bool] = False

@app.post("/predict-kp")
async def predict_kp(request: PredictionRequest):
    try:
        # 👇 Simulated astrology logic
        report_data = {
            "date": request.date,
            "time": request.time,
            "place": request.place,
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
                    "explanation": "Venus is sub-lord of 7th house and active in Dasha",
                    "hidden": True
                },
                "career": {
                    "change": False,
                    "explanation": "10th lord is stable and unaffected by transit"
                },
                "health": {
                    "summary": "Stable energy seen through Moon placement",
                    "hidden": True
                },
                "finance": {
                    "summary": "Steady flow expected; Jupiter aspect supports gains",
                    "hidden": True
                }
            }
        }

        # ✅ If PDF requested, generate and return file
        if request.pdf:
            filename = "Navadharma_Report.pdf"
            filepath = generate_pdf(report_data, filename=filename)
            return FileResponse(filepath, filename=filename, media_type="application/pdf")

        # ✅ Else return plain JSON
        return JSONResponse(content=report_data)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
