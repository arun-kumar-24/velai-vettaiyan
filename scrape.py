import random
import time
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
from camoufox.sync_api import Camoufox
from langchain_ollama import ChatOllama

# Configuration
DB_NAME = "jobs.db"
SMTP_SERVER = "smtp.gmail.com" # Example
SMTP_PORT = 587
SMTP_USER = os.getenv("EMAIL_ADDRESS")
SMTP_PASS = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

USER_PREFS = {
    "target_role_keywords": ["Software", "Developer", "Engineer", "Testing", "Python", "Web"],
    "target_skills": ["python", "software testing", "manual testing", "selenium", "java"],
    "preferred_location": "work from home",
    "min_stipend": 2000
}

class JobAnalyzer:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2")

    def analyze_job(self, job_data):
        """
        Analyzes the job to determine a relevance score (0-100).
        job_data: [id, title, company, location, stipend, duration, type, skills, link]
        """
        job_text = f"""
        Role: {job_data[1]}
        Company: {job_data[2]}
        Location: {job_data[3]}
        Stipend: {job_data[4]}
        Skills: {job_data[7]}
        Type: {job_data[6]}
        """

        prompt = f"""
        You are a job relevance scorer. 
        User Preferences: {USER_PREFS}
        
        Job Details:
        {job_text}
        
        Task: rate this job from 0 to 100 based on how well it matches the user's preferences.
        Consider Role title matches, Skills overlap, Location, and Stipend.
        
        Output strictly only the number (e.g., 85). Do not output any text.
        """
        
        try:
            response = self.llm.invoke(prompt)
            # Invoke returns a message object or string depending on version, 
            # assuming .content for AIMessage or string directly.
            content = response.content if hasattr(response, 'content') else str(response)
            score = int(''.join(filter(str.isdigit, content)))
            return min(100, max(0, score))
        except Exception as e:
            print(f"[-] LLM Error (Score): {e}")
            return 0

    def should_email(self, job_data, score):
        """
        Asks LLM if we should email the user about this high-scoring job.
        """
        prompt = f"""
        The following job scored {score}/100 for the user.
        Job: {job_data[1]} at {job_data[2]}
        Skills: {job_data[7]}
        
        Should I send an email notification to the user?
        Reply strictly with 'YES' or 'NO'.
        """
        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            return "YES" in content.upper()
        except:
            return False

def send_email(job_data, score):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"High Match Job Found! ({score}/100): {job_data[1]}" # Title
    
    body = f"""
    New Job Match Found!
    
    Role: {job_data[1]}
    Company: {job_data[2]}
    Score: {job_data[4]}
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

class InternshalaHumanScraper:
    def __init__(self):
        # 'humanize=True' enables realistic mouse paths and speeds
        self.cm = Camoufox(headless=False, humanize=True)
        self.browser = None
        self.page = None

    def start(self):
        self.browser = self.cm.__enter__()
        self.page = self.browser.new_page()
        # Set a realistic window size
        self.page.set_viewport_size({"width": 1280, "height": 800})

    def human_wait(self, min_s=2, max_s=5):
        """Standard human 'thinking' time."""
        time.sleep(random.uniform(min_s, max_s))

    def human_scroll(self):
        """Scrolls like someone looking for interesting jobs."""
        print("[*] Scrolling to mimic reading...")
        for _ in range(random.randint(3, 6)):
            # Scroll by a random amount
            amount = random.randint(400, 900)
            self.page.mouse.wheel(0, amount)
            # Pause to 'read'
            time.sleep(random.uniform(0.8, 2.0))
    
    def get_jobs_cards_html(self):
        """Extracts job details into a 2D list directly using browser JS."""
        print("[*] Extracting and parsing 10 job cards via JS...")
        
        extracted_data = self.page.evaluate("""() => {
            const selector = '.container-fluid.individual_internship.view_detail_button.visibilityTrackerItem';
            const cards = Array.from(document.querySelectorAll(selector)).slice(0, 10);
            
            return cards.map(card => {
                // Helper for safe text extraction
                const getText = (sel) => {
                    const el = card.querySelector(sel);
                    return el ? el.innerText.trim() : 'Unknown';
                };

                // ID
                const id = card.getAttribute('internshipid') || 'Unknown';
                
                // Title & Link
                const titleEl = card.querySelector('.job-internship-name a');
                const title = titleEl ? titleEl.innerText.trim() : 'Unknown';
                const link = titleEl ? titleEl.href : '';

                // Company
                const company = getText('.company-name');

                // Location
                const location = getText('.locations');

                // Stipend
                const stipend = getText('.stipend');

                // Duration
                let duration = 'Unknown';
                const calendarIcon = card.querySelector('.ic-16-calendar');
                if (calendarIcon && calendarIcon.parentElement) {
                    // Try to find span sibling or parent text
                    const span = calendarIcon.parentElement.querySelector('span');
                    duration = span ? span.innerText.trim() : calendarIcon.parentElement.innerText.trim();
                }

                // Type
                let type = 'Full Time';
                const statusDivs = card.querySelectorAll('.status-li');
                for (const div of statusDivs) {
                    if (div.innerText.includes('Part time')) {
                        type = 'Part Time';
                        break;
                    }
                }

                // Skills
                const skillsEls = card.querySelectorAll('.job_skills .job_skill');
                const skills = Array.from(skillsEls).map(el => el.innerText.trim()).join(', ');

                return [id, title, company, location, stipend, duration, type, skills, link];
            });
        }""")
        
        print(f"[*] Parsed {len(extracted_data)} jobs.")
        return extracted_data
    
    def navigate_to_internships(self, category_url):
        print(f"[*] Navigating to {category_url}")
        # Land on the page
        self.page.goto(category_url, wait_until="domcontentloaded")
        self.human_wait(3, 6)
        
        # Sometimes a 'Subscribe' or 'Location' popup appears on Internshala
        # We handle it by pressing Escape or waiting it out
        self.page.keyboard.press("Escape")
        self.human_wait(3, 6)
        self.human_scroll()
        
        # Extract data automatically after navigation
        return self.get_jobs_cards_html()


    def close(self):
        self.cm.__exit__(None, None, None)

# DB Helper Functions
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visited_internships (
            id TEXT PRIMARY KEY,
            visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_visited(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM visited_internships WHERE id = ?", (job_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_visited(job_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO visited_internships (id) VALUES (?)", (job_id,))
        conn.commit()
    except:
        pass
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    scraper = InternshalaHumanScraper()
    analyzer = JobAnalyzer()
    
    scraper.start()
    
    try:
        search_url = "https://internshala.com/internships/computer-science-internship-in-mumbai/"
        
        # Scrape
        jobs_list = scraper.navigate_to_internships(search_url)
        print(f"[*] Processing {len(jobs_list)} jobs...")

        for i, job_data in enumerate(jobs_list):
            job_id = job_data[0] # ID is at index 0
            
            if is_visited(job_id):
                print(f"[!] Skipping Visited Job ID: {job_id}")
                continue
            
            # Analyze Score
            score = analyzer.analyze_job(job_data)
            
            # Append Score to data (Index 9)
            job_data.append(score)
            
            print(f"\n--- Job {i+1} ---")
            print(f"Title: {job_data[1]} | Company: {job_data[2]}")
            print(f"Score: {score}/100")
            
            # Action Decision
            if score > 65:
                print(f"[*] High Score! Checking if email is needed...")
                if analyzer.should_email(job_data, score):
                    send_email(job_data, score)
                else:
                    print(f"[*] LLM decided NOT to email.")
            
            # Checkpoint
            mark_visited(job_id)
            
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        print("[*] Task complete. Closing browser.")
        scraper.close()