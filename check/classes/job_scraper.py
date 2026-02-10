from camoufox.sync_api import Camoufox
import time
import random

class JobScraper:
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
    
    def navigate_to_jobs(self, category_url):
        print(f"[*] Navigating to target URL")
        # Land on the page
        self.page.goto(category_url, wait_until="domcontentloaded")
        self.human_wait(3, 6)
        
        # Sometimes a 'Subscribe' or 'Location' popup appears
        # We handle it by pressing Escape or waiting it out
        self.page.keyboard.press("Escape")
        self.human_wait(3, 6)
        self.human_scroll()
        
        # Extract data automatically after navigation
        return self.get_jobs_cards_html()


    def close(self):
        self.cm.__exit__(None, None, None)
