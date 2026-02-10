
import sys
import os
# Add current directory to path so we can import from classes/utils
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from utils.send_email import send_email

# Dummy job data matching the structure used in main.py
# [id, title, company, location, stipend, duration, type, skills, link]
dummy_job_data = [
    "123", 
    "Software Engineer Test", 
    "Test Company", 
    "Remote", 
    "10000", 
    "6 Months", 
    "Full Time", 
    "Python, Testing", 
    "http://example.com"
]

print("Attempting to send test email via utils.send_email...")
send_email(dummy_job_data, 95)
print("Finished.")
