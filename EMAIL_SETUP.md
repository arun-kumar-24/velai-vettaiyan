
# Email Setup for Automation

Since Google requires secure authentication for scripts (due to 2-Step Verification being enabled on most accounts), you cannot use your standard login password.

You need to create an **App Password**. This is a 16-character code that allows your script to send emails safely.

## Step-by-Step Instructions

1.  **Open Google Account Settings**:
    *   Go to [https://myaccount.google.com/](https://myaccount.google.com/).
    *   On the left, select **Security**.

2.  **Enable 2-Step Verification** (if not already enabled):
    *   Under "Signing in to Google", ensure 2-Step Verification is **ON**.
    *   If OFF, turn it on and follow the prompts.

3.  **Generate App Password**:
    *   Still under "Signing in to Google" (or search "App Passwords" in the search bar at the top):
        *   Select **App passwords**.
    *   For "Select app", choose **Mail**.
    *   For "Select device", choose **Other (Custom name)** and type something like `Velai Vettaiyan Scraper`.
    *   Click **Generate**.

4.  **Copy the Password**:
    *   A 16-character password will appear (e.g., `abcd efgh ijkl mnop`).
    *   Copy this password (without spaces if possible, though Google accepts them or you can remove them manually).

5.  **Update `scrape.py`**:
    *   `SMTP_USER`: Your Gmail address (e.g., `you@gmail.com`).
    *   `SMTP_PASS`: Paste the 16-character App Password (e.g., `"abcdefghijklmnop"`).

## Testing

Once you fill these in `scrape.py`, running the script will automatically send an email to yourself whenever a job scores above 80/100 and passes the LLM check.
