# Core Components Documentation

This directory contains the primary logic classes that power the application's automated extraction and analysis capabilities.

## `JobScraper` (`job_scraper.py`)

This class handles the browser automation and DOM interaction. It is designed to be a generic frame for extracting list-based data from dynamic websites.

*   **Technology**: Built on **Camoufox**, a wrapper around Playwright that offers advanced anti-detection features to ensure consistent rendering.
*   **Key Features**:
    *   **Human Simulation**: Implements randomized delays (`human_wait`) and scrolling patterns (`human_scroll`) to mimic organic user behavior.
    *   **`navigate_to_jobs(url)`**: Handles consistent navigation to the target URL defined in your configuration.
    *   **`get_jobs_cards_html()`**: Executes JavaScript directly within the browser context. This approach is chosen for its robustness in handling Single Page Applications (SPAs) where data is rendered client-side. It extracts structured fields like Title, Company, and Skills into a normalized format.

## `JobAnalyzer` (`job_analyzer.py`)

This class integrates the local Large Language Model (LLM) into the data processing pipeline.

*   **Technology**: Uses **LangChain** (`langchain_ollama`) to interface with a locally running **Ollama** instance.
*   **Key Features**:
    *   **Semantic Analysis**: `analyze_job(job_data)` constructs a prompt containing the item details and user preferences. It asks the LLM to return a relevance score (0-100), allowing for fuzzy matching (e.g., understanding that "Node.js" is relevant to a "Backend Engineer" preference).
    *   **Decision Logic**: `should_email` asks the LLM for a binary decision on whether the found item warrants a notification.
    *   **Configuration**: Defaults to the `llama3.2` model but can be configured in the `__init__` method.
