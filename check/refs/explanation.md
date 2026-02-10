# Reference Material Documentation

The `refs/` directory plays a critical role in the development and maintenance of the scraping logic.

## Purpose

Web scraping relies heavily on CSS selectors and DOM structure. Websites like Internshala frequently update their layouts, classes, and ID attributes. 

This directory contains **static HTML snapshots** (e.g., `demo_about.html`, `demo_card.html`) captured from the live site during development.

## Usage in Structured Parsing

These files serve as the "ground truth" for engineering the Playwright/Camoufox extraction logic:

1.  **Selector Validation**: Developers load these local HTML files into a browser to test and refine CSS selectors (used in `InternShalaHuman.get_jobs_cards_html()`) without needing to send repeated requests to the live server.
2.  **Regression Testing**: If the live site changes and scraping breaks, a new snapshot can be saved here to compare with the old structure, allowing for quick identification of what changed (e.g., a class name change from `.stipend-container` to `.money-box`).
3.  **Offline Development**: Allows for working on the parsing logic (`internshala_human.py`) without an active internet connection or hitting rate limits.

In essence, these files are the **unit test fixtures** for the scraper's parsing engine.
