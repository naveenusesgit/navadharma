from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(200, 10, "Navadharma Prediction Report", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(data: dict, filename="report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section, details in data.items():
        pdf.set_font("Arial", "B", 12)
        safe_section = str(section).replace("–", "-").replace("’", "'").encode("latin-1", "replace").decode("latin-1")
        pdf.cell(200, 10, txt=f"{safe_section}", ln=True)

        if isinstance(details, dict):
            pdf.set_font("Arial", "", 11)
            for key, value in details.items():
                text = f"{key}: {value}"
                safe_text = str(text).replace("–", "-").replace("’", "'").encode("latin-1", "replace").decode("latin-1")
                pdf.cell(200, 10, txt=safe_text, ln=True)
        else:
            pdf.set_font("Arial", "", 11)
            safe_text = str(details).replace("–", "-").replace("’", "'").encode("latin-1", "replace").decode("latin-1")
            pdf.cell(200, 10, txt=safe_text, ln=True)

        pdf.ln(5)

    # Save to /tmp for Render compatibility
    out_path = os.path.join("/tmp", filename)
    pdf.output(out_path)

    return out_path

