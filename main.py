from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from utils.pdf_generator import generate_pdf

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Navadharma API is running 🔮"}

@app.post("/predict-kp")
async def predict_kp(request: Request):
    req = await request.json()

    # You can replace these with real calculations later
    data = {
        "date": req.get("date", "1990-01-01"),
        "time": req.get("time", "05:45"),
        "place": req.get("place", "Mumbai, India"),
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
            },
            "health": {
                "hidden": True
            },
            "education": {
                "explanation": "Strong Mercury but under aspect of Saturn",
                "hidden": True
            },
            "spirituality": {
                "explanation": "Jupiter in 12th house enhances spiritual interests"
            }
        },
        "yogas": ["Gajakesari Yoga", "Mangal Dosha", "Adhi Yoga"],
        "remedies": [
            "Chant Hanuman Chalisa on Tuesdays",
            "Donate yellow clothes on Thursdays",
            "Recite Vishnu Sahasranama daily"
        ]
    }

    # If user requests PDF
    if req.get("pdf", False):
        filename = "Navadharma_Report.pdf"
        pdf_path = generate_pdf(data, filename=filename)
        return FileResponse(pdf_path, media_type='application/pdf', filename=filename)

    return {"status": "success", "data": data}
