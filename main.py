from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.pdf_generator import generate_pdf
from utils.astro_logic import generate_astrology_report
from utils.gpt_summary import generate_gpt_summary
import os

load_dotenv()

app = FastAPI()

class RequestData(BaseModel):
    name: str
    date: str
    time: str
    place: str
    pdf: bool = False

@app.post("/predict-kp")
async def predict_kp(request: RequestData):
    try:
        # Step 1: Parse request data
        name = request.name
        date = request.date
        time = request.time
        place = request.place

        # Step 2: Generate astrology data
        astro_data = generate_astrology_report(name, date, time, place)

        # Step 3: Get GPT summary
        gpt_summary = generate_gpt_summary(astro_data)
        astro_data["gptSummary"] = gpt_summary

        # Step 4: Generate PDF if requested
        if request.pdf:
            filepath = generate_pdf(astro_data, filename="Navadharma_Report.pdf")
            return FileResponse(filepath, media_type="application/pdf", filename="Navadharma_Report.pdf")

        # Otherwise return JSON
        return JSONResponse(content={
            "astroData": astro_data,
            "gptSummary": gpt_summary
        })

    except Exception as e:
        print("❌ Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
