# Utilities Documentation

This directory contains helper functions that support the main application logic, primarily focusing on data persistence and communication.

## `db_utils.py`

Handles all interactions with the SQLite3 database (`jobs.db`). This module ensures that the application has a memory of past actions to avoid redundancy.

*   **`init_db()`**: Checks for the existence of the database and creates the `visited_internships` table if it's missing. This is called at application startup.
*   **`is_visited(job_id)`**: specific query to check if a unique job ID has already been processed. Crucial for efficiency so the LLM doesn't re-analyze the same jobs.
*   **`mark_visited(job_id)`**: Records a job ID as processed after scraping/analysis is complete.

## `send_email.py`

Manages outbound notifications using the Simple Mail Transfer Protocol (SMTP).

*   **Functionality**: Constructs a MIME multipart email containing the job details and its relevance score.
*   **Safe Handling**: Uses `smtplib` with TLS encryption (`server.starttls()`) for secure communication.
*   **Configuration**: Reads sensitive credentials (sender email, app password) from environment variables via `python-dotenv`, ensuring that secrets are not hardcoded in the source.
