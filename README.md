# Velai Vettaiyan - Intelligent Internship Scraper

**Velai Vettaiyan** is an advanced, automated internship hunting tool designed to streamline the search for relevant opportunities on Internshala. By combining stealthy browser automation with the cognitive power of local Large Language Models (LLMs), it autonomously navigates job listings, extracts structured data, and intelligently scores opportunities based on your personal preferences—sending you real-time email alerts for high-value matches.

## Tech Stack

*   **Python**: The core logic and orchestration.
*   **Ollama**: Local LLM inference engine used for analyzing job descriptions and scoring relevance (defaults to `llama3.2`).
*   **Playwright (via Camoufox)**: Provides stealthy, anti-detect browser automation to navigate and scrape dynamic web content without triggering bot defenses.
*   **SQLite3**: A lightweight, serverless database used to track visited internships and prevent duplicate processing.
*   **LangChain**: Framework for interfacing with the Ollama LLM.

## Setup Instructions

### 1. Environment Setup

Clone the repository and create a virtual environment to keep dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r check/requirements.txt
```

### 3. Database Setup

The project uses **SQLite3** for data persistence. 
*   **No manual setup is required.**
*   The database (`jobs.db`) and necessary tables are automatically initialized when you run the application for the first time.

### 4. Ollama Integration

This project uses a local LLM via [Ollama](https://ollama.com/) to analyze job relevance.

1.  **Download Ollama**: Visit the [Ollama Website](https://ollama.com/) and install the version for your OS.
2.  **Pull the Model**: The project defaults to using `llama3.2`. Run the following command in your terminal:
    ```bash
    ollama pull llama3.2
    ```
3.  **Customization**: If you wish to use a different model (e.g., `mistral`, `llama3`), you can change the model name in the source code:
    *   Open `check/classes/job_analyzer.py`
    *   Locate the `JobAnalyzer` class initialization:
        ```python
        self.llm = ChatOllama(model="llama3.2") 
        ```
    *   Change `"llama3.2"` to your preferred model tag.

### 5. Email Configuration

To receive email alerts for high-scoring internships, you must configure SMTP settings.

1.  Create a `.env` file in the `check/` directory (use `check/.env.example` as a template).
2.  Populate the following fields:
    ```ini
    EMAIL_ADDRESS=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    RECEIVER_EMAIL=recipient_email@gmail.com
    ```
    *   **Note**: For Gmail, you cannot use your regular login password. You must generate an **App Password**.
    *   👉 **[Read the Email Setup Guide](EMAIL_SETUP.md)** for detailed instructions on generating an App Password.

## Project Architecture & Features

The project is modularized into distinct components for scalability and maintainability.

*   **[Core Classes](check/classes/explanation.md)**: Contains the intelligent agents for scraping (`InternShalaHuman`) and analysis (`JobAnalyzer`).
*   **[Utilities](check/utils/explanation.md)**: Helper modules for database management and email notifications.
*   **[References](check/refs/explanation.md)**: Static HTML snapshots used for engineering reliable scraping selectors.

### Features
*   **Stealth Scraping**: Uses Camoufox to mimic human behavior (mouse movements, scrolling) and evade detection.
*   **AI-Powered Analysis**: Scores jobs 0-100 based on your specific keywords and requirements, not just simple text matching.
*   **Duplicate Prevention**: Automatically remembers which jobs you've seen using SQLite.
*   **Smart Alerts**: Only emails you when a job exceeds your minimum relevance threshold.

## Contributing

Contributions are welcome! Whether it's fixing a bug, improving the scoring prompt, or adding support for new job portals, feel free to fork the repository and submit a Pull Request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request