from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Navadharma Jyotish Report", ln=True, align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"{title}", ln=True)
        self.ln(2)

    def chapter_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, text)
        self.ln()

    def add_section(self, title, content):
        self.chapter_title(title)
        if isinstance(content, str):
            self.chapter_body(content)
        elif isinstance(content, dict):
            for k, v in content.items():
                self.chapter_title(f"{k}")
                self.chapter_body(str(v))
        elif isinstance(content, list):
            for item in content:
                self.chapter_body(str(item))
        self.ln()

def generate_full_report(name, chart, dasha, yogas, nakshatra, remedies, gpt, lang="en"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_section("🪐 Birth Chart", chart)
    pdf.add_section("📊 Dasha", dasha)
    pdf.add_section("🔮 Yogas", yogas)
    pdf.add_section("🌟 Nakshatra Details", nakshatra)
    pdf.add_section("🧙 Remedies", remedies)
    pdf.add_section("🧠 GPT Interpretation", gpt)

    filename = f"reports/{name.replace(' ', '_')}_full_report.pdf"
    os.makedirs("reports", exist_ok=True)
    pdf.output(filename)
    return filename

def generate_match_report(result, gpt, person1, person2, lang="en"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.chapter_title("💑 Match Compatibility Report")
    pdf.chapter_body(f"👩 {person1.name} vs 👨 {person2.name}")
    
    pdf.add_section("📊 Compatibility Scores", result.get("scores", {}))
    pdf.add_section("🧘‍♀️ Summary", result.get("summary", ""))
    pdf.add_section("🧠 GPT Summary", gpt)

    filename = f"reports/{person1.name.replace(' ', '_')}_{person2.name.replace(' ', '_')}_match_report.pdf"
    os.makedirs("reports", exist_ok=True)
    pdf.output(filename)
    return filename
