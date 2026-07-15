import smtplib
from email.mime.text import MIMEText

SMTP_EMAIL = "poorviarora2005@gmail.com"
SMTP_PASSWORD = "tezmkgjxrwppmqzb"

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
        print("Email Error:", repr(e))
        return False


ok = send_email(
    "poorviarora2005@gmail.com",
    "Test Email",
    "This is a test email from budget app."
)

print("Email sent:", ok)