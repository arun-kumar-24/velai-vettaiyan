# General Purpose Structured Data Extraction Framework

**Velai Vettaiyan** is a technical proof-of-concept for educational purposes. It demonstrates the integration of stealthy browser automation with local Large Language Models (LLMs) to extract, interpret, and score structured data from dynamic web pages.

**Disclaimer**: Users are responsible for ensuring their use cases comply with the Terms of Service of any target website. This project includes an **Offline Development Mode** using local HTML references to minimize network traffic and respect server load during development.

## Tech Stack

*   **Python**: Core logic and orchestration.
*   **Ollama**: Local LLM inference engine used for semantic analysis and relevance scoring (defaults to `llama3.2`).
*   **Playwright (via Camoufox)**: Provides stealthy, anti-detect browser automation to handle dynamic content.
*   **SQLite3**: Lightweight persistence layer for tracking processed items.
*   **LangChain**: Framework for interfacing with the Ollama LLM.

## Setup Instructions

### 1. Environment Setup

Clone the repository and create a virtual environment:

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

```bash
pip install -r check/requirements.txt
```

### 3. Configuration

The project uses environment variables for configuration. Create a `.env` file in the `check/` directory:

```ini
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECEIVER_EMAIL=recipient_email@gmail.com
TARGET_URL=https://example.com/target-page
```

*   **TARGET_URL**: The specific URL you wish to process.
*   **Email Setup**: Refer to **[EMAIL_SETUP.md](EMAIL_SETUP.md)** for instructions on generating secure App Passwords.

### 4. Ollama Integration

1.  **Download Ollama**: [Ollama Website](https://ollama.com/)
2.  **Pull Model**:
    ```bash
    ollama pull llama3.2
    ```
    *To use a different model, update `check/classes/job_analyzer.py`.*

## Project Architecture

*   **[Core Modules](check/classes/explanation.md)**: Includes the `JobScraper` (automation) and `JobAnalyzer` (semantic scoring).
*   **[Utilities](check/utils/explanation.md)**: Database tracking and notification services.
*   **[Offline Development Mode](check/refs/explanation.md)**: Explains the use of static HTML snapshots (`refs/`) for developing parsing logic without live server interaction.

### Features
*   **Stealth Automation**: Uses human-like behavior patterns to render dynamic content.
*   **Semantic Scoring**: Uses LLMs to understand context (e.g., matching "manual testing" skills to "QA" roles) rather than simple keyword matching.
*   **State Management**: Tracks visited IDs to prevent duplicate processing.

## Contributing

This is an open-source educational project. PRs are welcome!

1.  Fork the Project
2.  Create your Feature Branch
3.  Commit your Changes
4.  Push to the Branch
5.  Open a Pull Request