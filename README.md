# Soft Whispers - AI Bedtime Story Subscription Service

"Soft Whispers" is a tranquil and minimalistic landing page designed to capture user interest for an upcoming AI-powered bedtime story service. The project is built with a Python Flask backend and is optimized for seamless deployment on Vercel.

## Core Features

- **Clean & Minimalist UI**: A calming, aesthetically pleasing interface built with HTML5, CSS3, and modern JavaScript.
- **Email Subscription**: A robust email collection form that saves user emails to a MySQL database.
- **Duplicate Prevention**: The backend logic prevents the same email from being registered twice.
- **Scalable Backend**: A lightweight Flask server handles API requests.
- **Automated Deployment**: Fully configured for continuous deployment on Vercel.

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (no heavy frameworks)
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Deployment**: Vercel

## Project Structure

```
.
├── app.py                   # The main Flask application
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel deployment configuration
├── db_setup.sql             # SQL script for initial database setup
├── templates/
│   └── bedtime_story_landing.html  # Main landing page HTML
│   └── button_test.html            # A page for testing buttons
│   └── privacy.html                # Privacy Policy page
└── README.md                # This file
```

## Local Development Setup

To run this project on your local machine, follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd Soft-Whispers
    ```

2.  **Set Up the Database**
    - Ensure you have a running MySQL server.
    - Create a database named `dreamtales`.
    - Import the `db_setup.sql` file to create the `user_subscriptions` table.
      ```sql
      -- Example using MySQL command line
      mysql -u root -p dreamtales < db_setup.sql
      ```

3.  **Configure `app.py`**
    - Open `app.py` and update the `DB_CONFIG` dictionary with your MySQL credentials:
      ```python
      DB_CONFIG = {
          'host': 'localhost',
          'user': 'your_mysql_user',
          'password': 'your_mysql_password',
          'database': 'dreamtales'
      }
      ```

4.  **Install Dependencies & Run**
    - It's highly recommended to use a virtual environment.
    ```bash
    # Create and activate a virtual environment (optional but recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install the required packages
    pip install -r requirements.txt

    # Run the Flask application
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

## Vercel Deployment

This project is ready for Vercel. Simply connect your GitHub repository to a new Vercel project. Vercel will automatically use `vercel.json` and `requirements.txt` to build and deploy the application.

**Important**: You will need to configure Vercel Environment Variables for your database connection details (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) instead of hardcoding them in `app.py` for production. The code in `app.py` would need to be updated to read these environment variables. 