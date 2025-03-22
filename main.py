from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai
from utils.pdf_generator import generate_pdf

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class AstroRequest(BaseModel):
    date: str
    time: str
    place: str
    lagna: str
    currentDasha: dict
    predictions: dict
    pdf: bool = False


# 🧠 GPT summary logic
def generate_gpt_summary(data: dict) -> str:
    prompt = f"""
You are a wise Vedic astrologer using KP astrology. 
Generate a short personalized astro summary based on:

Date: {data['date']}
Time: {data['time']}
Place: {data['place']}
Lagna: {data['lagna']}
Mahadasha: {data['currentDasha'].get('mahadasha')}
Antardasha: {data['currentDasha'].get('antardasha')}
Dasha Period: {data['currentDasha'].get('period')}

Predictions:
{data['predictions']}

Summarize the above in a friendly, professional tone, offering clarity and positivity.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a wise and insightful Vedic astrologer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


@app.post("/predict-kp")
async def predict_kp(request: AstroRequest):
    data = request.dict()

    try:
        # GPT prediction summary
        gpt_summary = generate_gpt_summary(data)
        data["gpt_summary"] = gpt_summary

        if data.get("pdf", False):
            filepath = generate_pdf(data, filename="Navadharma_Report.pdf")
            return FileResponse(filepath, media_type='application/pdf', filename="Navadharma_Report.pdf")

        return JSONResponse(content={
            "status": "success",
            "summary": gpt_summary,
            "data": data
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
