# utils/email_utils.py
import smtplib
from email.message import EmailMessage
import os

def send_report_email(to_email, pdf_path, subject="Your Navadharma Report"):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_EMAIL")
    msg["To"] = to_email
    msg.set_content("Please find your full report attached.\n\nWith Blessings,\nNavadharma Team")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASS"))
        smtp.send_message(msg)
