import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Configuration
SMTP_SERVER = "smtp.gmail.com" # Example
SMTP_PORT = 587
SMTP_USER = os.getenv("EMAIL_ADDRESS")
SMTP_PASS = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_email(job_data, score):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"High Match Job Found! ({score}/100): {job_data[1]}" # Title
    
    body = f"""
    New Job Match Found!
    
    Role: {job_data[1]}
    Company: {job_data[2]}
    Score: {score}
    Location: {job_data[3]}
    Stipend: {job_data[4]}
    Skills: {job_data[7]}
    Link: {job_data[8]}
    """
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Actual sending logic
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"[+] Email sent successfully to {RECEIVER_EMAIL} for job: {job_data[1]}")
    except Exception as e:
        print(f"[-] Email Error: {e}")
