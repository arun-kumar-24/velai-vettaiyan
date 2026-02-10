# Email Configuration Guide

To enable the automated email notification feature in **Velai Vettaiyan**, you need to provide an App Password for your email account. This is a security requirement for most modern email providers (like Gmail) when accessing them via scripts.

## How to Generate a Google App Password

If you are using Gmail, follow these steps:

1.  **Go to your Google Account**:
    *   Visit [myaccount.google.com](https://myaccount.google.com/).
    *   Ensure you are logged into the account you want to send emails *from*.

2.  **Navigate to Security**:
    *   Click on the **Security** tab in the left-hand sidebar.

3.  **Enable 2-Step Verification** (if not already enabled):
    *   Scroll down to the "How you sign in to Google" section.
    *   Ensure **2-Step Verification** is turned **ON**. App Passwords are *only* available if 2FA is active.

4.  **Create an App Password**:
    *   In the search bar at the top of the page, type **"App passwords"** and select it.
    *   Alternatively, look for "App passwords" under the "How you sign in to Google" section (sometimes hidden at the bottom).
    *   You may be asked to sign in again.

5.  **Generate the Password**:
    *   **App name**: Enter a custom name, e.g., `VelaiVettaiyan`.
    *   Click **Create**.

6.  **Copy the Password**:
    *   Google will generate a 16-character password (e.g., `abcd efgh ijkl mnop`).
    *   **Copy this password immediately**. You will not be able to see it again.

7.  **Update your `.env` file**:
    *   Paste this password into the `EMAIL_PASSWORD` field in your `.env` file inside the `check/` directory.

    ```ini
    EMAIL_ADDRESS=your_email@gmail.com
    EMAIL_PASSWORD=abcd efgh ijkl mnop  <-- Paste here (spaces are fine)
    RECEIVER_EMAIL=recipient_email@gmail.com
    ```

## Troubleshooting

*   **"Username and Password not accepted"**: Ensure you are using the *App Password*, not your main Google account password.
*   **Connection Refused**: Ensure your firewall or antivirus isn't blocking Python from accessing port 587.
