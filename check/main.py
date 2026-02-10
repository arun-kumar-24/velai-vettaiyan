import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path so we can import from classes/utils
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from classes.job_scraper import JobScraper
from classes.job_analyzer import JobAnalyzer
from utils.send_email import send_email
from utils.db_utils import init_db, is_visited, mark_visited

# Configuration
USER_PREFS = {
    "target_role_keywords": ["Software", "Developer", "Engineer", "Testing", "Python", "Web"],
    "target_skills": ["python", "software testing", "manual testing", "selenium", "java"],
    "preferred_location": "work from home",
    "min_stipend": 2000
}

if __name__ == "__main__":
    init_db()
    
    target_url = os.getenv("TARGET_URL")
    if not target_url:
        print("[-] Error: TARGET_URL not set in .env")
        sys.exit(1)

    scraper = JobScraper()
    analyzer = JobAnalyzer(user_prefs=USER_PREFS)
    
    scraper.start()
    
    try:
        # Scrape
        jobs_list = scraper.navigate_to_jobs(target_url)
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