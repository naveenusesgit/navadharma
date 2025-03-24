from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging

from utils.matchmaking import get_matchmaking_report
from utils.kundli import get_kundli_data
from utils.astro_report import generate_astro_pdf

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Navadharma API",
    description="Astrology, Matchmaking and Report Generation API",
    version="1.0.0"
)

# CORS middleware (allow all for now, lock down for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request models
class ReportRequest(BaseModel):
    name: str = Field(..., description="Full name")
    date: str = Field(..., example="1990-05-15", description="Date of birth (YYYY-MM-DD)")
    time: str = Field(..., example="15:45", description="Time of birth (HH:MM)")
    place: str = Field(..., description="Place of birth")

class MatchRequest(BaseModel):
    person1_name: str
    person1_dob: str
    person1_time: str
    person1_place: str
    person2_name: str
    person2_dob: str
    person2_time: str
    person2_place: str

# Health check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Navadharma API is live"}

# Home endpoint
@app.get("/", tags=["General"])
def root():
    return {"message": "Welcome to Navadharma API - Jyotish, Matchmaking, and Reports"}

# Kundli data endpoint
@app.get("/kundli-details", tags=["Kundli"])
def get_kundli_details(
    name: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    place: Optional[str] = None
):
    try:
        data = get_kundli_data(name=name, date=date, time=time, place=place)
        return {"status": "success", "data": data}
    except Exception as e:
        logger.exception("Error in kundli-details")
        raise HTTPException(status_code=500, detail=str(e))

# Report generation endpoint
@app.post("/generate-report", tags=["Astrology"])
def generate_report(data: ReportRequest):
    try:
        logger.info(f"Generating report for {data.name}")
        pdf_path = generate_astro_pdf(data.name, data.date, data.time, data.place)
        return {"message": "Report generated successfully", "pdf_url": pdf_path}
    except Exception as e:
        logger.exception("Failed to generate report")
        raise HTTPException(status_code=500, detail=str(e))

# Matchmaking endpoint
@app.post("/matchmaking", tags=["Matchmaking"])
def matchmaking(data: MatchRequest):
    try:
        logger.info(f"Running matchmaking for {data.person1_name} & {data.person2_name}")
        result = get_matchmaking_report(data)
        return {"message": "Matchmaking report generated", "result": result}
    except Exception as e:
        logger.exception("Matchmaking failed")
        raise HTTPException(status_code=500, detail=str(e))

# Fallback route for errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return HTTPException(status_code=500, detail="An unexpected error occurred.")
