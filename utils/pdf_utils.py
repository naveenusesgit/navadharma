from fpdf import FPDF
import os
from utils.kundli import get_planet_positions, get_lagna_info, get_dasha_periods

def generate_kundli_report_pdf(datetime_str, place, latitude, longitude, timezone_offset):
    # Get basic info
    planet_data = get_planet_positions(datetime_str, latitude, longitude, timezone_offset)
    lagna_info = get_lagna_info(datetime_str, latitude, longitude, timezone_offset)
    dasha_info = get_dasha_periods(datetime_str, latitude, longitude, timezone_offset)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(40, 40, 40)

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "🪐 Navadharma Kundli Report", ln=True, align='C')
    pdf.ln(5)

    # Metadata
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"📍 Place: {place}", ln=True)
    pdf.cell(0, 10, f"📅 DateTime: {datetime_str}", ln=True)
    pdf.cell(0, 10, f"🧭 Timezone Offset: GMT {'+' if timezone_offset >= 0 else ''}{timezone_offset}", ln=True)
    pdf.ln(5)

    # Lagna Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "🌅 Lagna Info", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Lagna: {lagna_info['lagna']}", ln=True)
    pdf.cell(0, 10, lagna_info['description'], ln=True)
    pdf.ln(5)

    # Planet Positions
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "🪐 Planetary Positions", ln=True)
    pdf.set_font("Arial", size=12)
    for planet, pos in planet_data["positions"].items():
        pdf.cell(0, 10, f"{planet}: {pos}", ln=True)
    pdf.ln(5)

    # Dasha Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "📊 Mahadasha Periods", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, dasha_info["summary"])

    # Save to static
    output_path = "/app/static/kundli_report.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)

    return {
        "pdf_url": "https://navadharma.onrender.com/static/kundli_report.pdf"
    }
