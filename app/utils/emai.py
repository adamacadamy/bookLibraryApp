from email.mime.text import MIMEText
import smtplib

from app.config.email import (
    SMTP_SERVER,
    SMTP_PORT,
    FROM_EMAIL,
    EMAIL_PASSWORD,
    EMAIL_REGISTRATION_MESSAGE_TEMPLATE,
)


def send_registration_email(
    to_email: str,
    full_name: str,
    username: str,
    password: str,
) -> bool:
    """Send confirmation email using SMTP"""
    msg = MIMEText(
        EMAIL_REGISTRATION_MESSAGE_TEMPLATE, "html"
    )  # Set MIME type to 'html'
    msg["full_name"] = full_name
    msg["username"] = username
    msg["password"] = password
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable TLS
        server.login(FROM_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
