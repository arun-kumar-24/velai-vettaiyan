import sqlite3
import random
from scrape import InternshalaHumanScraper
from job_scorer import JobScorer
from create_db import create_table

# 1. Define User Preferences (Customize as needed)
USER_PREFS = {
    "target_role_keywords": ["Software", "Developer", "Engineer", "Testing", "Python", "Web"],
    "target_skills": ["python", "software testing", "manual testing", "selenium", "java"],
    "preferred_location": "work from home",
    "min_stipend": 2000
}

def save_to_db(job_details, score):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO internships (
                id, title, company, location, stipend, duration, type, skills, link, score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job_details['id'],
            job_details['title'],
            job_details['company'],
            job_details['location'],
            job_details['stipend'],
            job_details['duration'],
            job_details['type'],
            ", ".join(job_details['skills']), # Store skills as string
            job_details['link'],
            score
        ))
        conn.commit()
    except Exception as e:
        print(f"[-] DB Error: {e}")
    finally:
        conn.close()

def main():
    # Ensure DB exists
    print("[*] Initializing Database...")
    create_table()

    # Initialize Scorer
    scorer = JobScorer(USER_PREFS)

    # Initialize Scraper
    scraper = InternshalaHumanScraper()
    scraper.start() # Opens browser

    try:
        # Navigate to a generic search page or use a specific one
        # Using a search for "web development" as an example
        search_url = "https://internshala.com/internships/web-development-internship/"
        print(f"[*] Starting scrape for: {search_url}")
        
        scraper.navigate_to_internships(search_url)
        
        # Get Data
        cards_html = scraper.get_job_cards_html()
        
        print(f"[*] Processing {len(cards_html)} cards...")
        for html in cards_html:
            details = scorer.extract_details(html)
            if details and details['id']: # Ensure valid ID
                score = scorer.calculate_score(details)
                print(f"    > Found: {details['title']} @ {details['company']} (Score: {score})")
                save_to_db(details, score)
        
        print("[*] Done! Check 'jobs.db' or run a query to see results.")

    except Exception as e:
        print(f"[-] Main Error: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
