import os
from fpdf import FPDF
from datetime import datetime

from utils.predictions import get_daily_prediction
from utils.kundli import get_nakshatra_info, get_lagna_info
from utils.transit import get_transit_effects
from utils.remedies import get_astrological_remedies

STATIC_DIR = "static/predictions"
os.makedirs(STATIC_DIR, exist_ok=True)

def generate_pdf_prediction_report(name: str, date: str):
    today_str = date or datetime.today().strftime("%Y-%m-%d")
    filename = f"{name}_{today_str}.pdf"
    filepath = os.path.join(STATIC_DIR, filename)

    # Dummy time/place for fallback if not used
    default_time = "12:00"
    default_place = "Delhi, India"

    # Get data
    nakshatra_info = get_nakshatra_info(today_str, default_time, default_place)
    lagna_info = get_lagna_info(today_str, default_time, default_place)
    prediction = get_daily_prediction(name, today_str)
    transits = get_transit_effects(name, today_str, default_time, default_place)
    remedies = get_astrological_remedies(name, today_str, default_time, default_place)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="Daily Astrological Prediction Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {today_str}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Nakshatra Info:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=str(nakshatra_info))
    pdf.ln(3)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Lagna Info:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=str(lagna_info))
    pdf.ln(3)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Today's Prediction:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=str(prediction))
    pdf.ln(3)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Transit Effects:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=str(transits))
    pdf.ln(3)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Recommended Remedies:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=str(remedies))
    pdf.ln(3)

    pdf.output(filepath)
    return filepath
