# main.py

from fastapi import FastAPI, Query
from utils.kundli import generate_kundli_chart
from utils.full_kundli_prediction import generate_full_kundli_prediction
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Jyotish-as-a-Service 🔮",
    description="Global Astrology API powered by Swiss Ephemeris & KP system",
    version="1.0.0"
)

# ✅ Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Jyotish-as-a-Service API 🌐🔮",
        "endpoints": [
            "/kundli",
            "/planet-positions",
            "/nakshatra-details",
            "/dasha-periods",
            "/remedies",
            "/pdf-report",
        ]
    }

@app.get("/kundli")
def get_kundli_chart(
    name: str = Query(...),
    date: str = Query(..., description="Date of birth in YYYY-MM-DD format"),
    time: str = Query(..., description="Time of birth in HH:MM 24hr format"),
    place: str = Query(..., description="Birthplace, e.g. Varanasi, India")
):
    """
    ✅ Generate full Kundli chart with Lagna, Rasi, Nakshatra & Planetary positions.
    """
    return generate_kundli_chart(name, date, time, place)

# === 🛠️ Stubs for upcoming features ===

@app.get("/planet-positions")
def get_planet_positions_stub():
    return {"message": "Coming soon: Planetary positions based on Swiss Ephemeris"}

@app.get("/nakshatra-details")
def get_nakshatra_details_stub():
    return {"message": "Coming soon: Nakshatra personality and pada-based details"}

@app.get("/dasha-periods")
def get_dasha_periods_stub():
    return {"message": "Coming soon: Vimshottari Dasha periods"}

@app.get("/remedies")
def get_remedies_stub():
    return {"message": "Coming soon: Remedies based on afflicted grahas and houses"}

@app.get("/pdf-report")
def get_pdf_report_stub():
    return {"message": "Coming soon: Generate downloadable Kundli PDF report"}
