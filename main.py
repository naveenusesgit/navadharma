from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from utils.pdf_generator import generate_pdf
from utils.astro_logic import get_full_astrology_data
from utils.gpt_summary import generate_gpt_summary

load_dotenv()

app = FastAPI()

# CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key protection
API_KEY = os.getenv("NAVADHARMA_API_KEY", "kp-demo-secret-key-123456")

class PredictionRequest(BaseModel):
    name: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    place: str
    pdf: bool = False

@app.get("/")
def root():
    return {"message": "🔮 Navadharma KP Astrology API is running!"}

@app.post("/predict-kp")
async def predict_kp(request: Request, payload: PredictionRequest):
    # ✅ 1. Check API Key
    headers = request.headers
    client_key = headers.get("X-API-KEY")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized API key")

    # ✅ 2. Extract data
    user_input = payload.dict()

    try:
        # ✅ 3. Perform Astrology Calculations
        report_data = get_full_astrology_data(
            name=user_input["name"],
            date=user_input["date"],
            time=user_input["time"],
            place=user_input["place"]
        )

        # ✅ 4. Generate GPT Summary
        try:
            gpt_output = generate_gpt_summary(report_data)
            report_data["gptSummary"] = gpt_output
        except Exception as e:
            report_data["gptSummary"] = "AI Summary unavailable right now."
            print("GPT Error:", e)

        # ✅ 5. Generate PDF if requested
        if user_input.get("pdf", False):
            pdf_path = generate_pdf(report_data, filename="Navadharma_Report.pdf")
            return FileResponse(pdf_path, media_type="application/pdf", filename="Navadharma_Report.pdf")

        # ✅ 6. Return JSON response
        return {
            "message": "Prediction generated successfully.",
            "data": report_data
        }

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
