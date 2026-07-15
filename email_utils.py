import smtplib
from email.mime.text import MIMEText
import streamlit as st

SMTP_EMAIL = "poorviarora2005@gmail.com"
SMTP_PASSWORD = "tezmkgjxrwppmqzb"

APPROVER_EMAIL = "approver_email_here@gmail.com"
PARTNER_EMAIL = "partner_email_here@gmail.com"


def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        st.error(f"Email Error: {e}")
        print("Email Error:", repr(e))
        return False