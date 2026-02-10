# Core Components Documentation

This directory contains the primary logic classes that power the application's scraping and analysis capabilities.

## `InternShalaHuman` (`internshala_human.py`)

This class is responsible for the interaction with the target website (Internshala). It is designed to behave like a human user to avoid detection.

*   **Technology**: Built on **Camoufox**, a wrapper around Playwright that offers advanced anti-detection features.
*   **Key Features**:
    *   **`human_wait()` & `human_scroll()`**: Implements randomized delays and scrolling patterns to mimic organic user behavior.
    *   **`navigate_to_internships(url)`**: Handles the browser navigation to specific category pages.
    *   **`get_jobs_cards_html()`**: Executes JavaScript directly within the browser context to robustly parse the DOM and extract structured data (Title, Company, Location, Stipend, etc.). This client-side extraction is often more reliable than server-side parsing for dynamic SPAs.

## `JobAnalyzer` (`job_analyzer.py`)

This class integrates the local Large Language Model (LLM) into the workflow.

*   **Technology**: Uses **LangChain** (`langchain_ollama`) to interface with a locally running **Ollama** instance.
*   **Key Features**:
    *   **`analyze_job(job_data)`**: Constructs a prompt containing the job details and user preferences. It asks the LLM to return a relevance score (0-100) based on semantic matching (e.g., matching "Manual Testing" skills to a "QA Engineer" role).
    *   **`should_email(job_data, score)`**: A secondary decision-making step where the LLM decides if a notification is warranted based on the job's attractiveness, providing a "YES/NO" judgment.
    *   **Configuration**: Defaults to the `llama3.2` model but can be configured in the `__init__` method.
