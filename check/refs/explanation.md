# Offline Development Mode

The `refs/` directory is central to the project's ethical development strategy.

## Purpose

Responsible automation development requires minimizing unnecessary traffic to target servers. Repeatedly hitting a live website to test CSS selectors or parsing logic is inefficient and can be disruptive.

This directory contains **static HTML snapshots** (e.g., `demo_about.html`, `demo_card.html`) captured once and saved locally.

## Usage

These files serve as "Offline References" for engineering the extraction logic:

1.  **Selector Engineering**: Developers load these local HTML files into the browser to test and refine the JavaScript extraction logic (seen in `JobScraper.get_jobs_cards_html()`) in a completely offline environment.
2.  **Stability Testing**: These snapshots act as immutable test fixtures. If the parsing logic works against these files, valid regressions can be identified if live site structures change.
3.  **Ethical Compliance**: By developing against local files, we significantly reduce the request volume sent to external servers during the coding and debugging phases.
