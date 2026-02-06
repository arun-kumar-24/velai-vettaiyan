import random
import time
from camoufox.sync_api import Camoufox

class HumanBrowser:
    def __init__(self):
        # We initialize the manager, but the actual launch happens in 'start'
        self.cm_manager = Camoufox(headless=False)
        self.browser = None
        self.page = None

    def start(self):
        """Starts the browser and creates a new page."""
        # Entering the context manager launches the camoufox server
        self.browser = self.cm_manager.__enter__()
        self.page = self.browser.new_page()

    def human_delay(self, min_s=1, max_s=3):
        """Randomizes wait times between actions."""
        time.sleep(random.uniform(min_s, max_s))

    def human_scroll(self):
        """Scrolls down in chunks, like a person reading."""
        for _ in range(3):
            scroll_amount = random.randint(300, 700)
            self.page.mouse.wheel(0, scroll_amount)
            self.human_delay(0.5, 1.5)

    def scrape_headings_and_links(self, url):
        """Navigates and extracts headings and links."""
        print(f"Navigating to {url}...")
        self.page.goto(url, wait_until="domcontentloaded")
        self.human_delay(2, 4)
        
        # Selector for 'Scrape This Site' headings
        selector = ".page-title a"
        self.page.wait_for_selector(selector)
        
        elements = self.page.query_selector_all(selector)
        data = []
        for el in elements:
            data.append({
                "heading": el.inner_text().strip(),
                "link": el.get_attribute("href")
            })
        return data

    def close(self):
        """Ensures the browser server is shut down."""
        if self.cm_manager:
            self.cm_manager.__exit__(None, None, None)

if __name__ == "__main__":
    scraper = HumanBrowser()
    
    try:
        scraper.start()
        results = scraper.scrape_headings_and_links("https://www.scrapethissite.com/pages/")
        
        print(f"\nSuccessfully extracted {len(results)} items:\n")
        print("=" * 60)
        for item in results:
            print(f"Heading : {item['heading']}")
            # Construct full URL if needed
            full_link = f"https://www.scrapethissite.com{item['link']}"
            print(f"Link    : {full_link}")
            print("-" * 60)
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("\nClosing browser...")
        scraper.close()