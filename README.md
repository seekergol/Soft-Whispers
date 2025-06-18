# Soft Whispers - AI Bedtime Story Subscription Service

"Soft Whispers" is a tranquil and minimalistic landing page designed to capture user interest for an upcoming AI-powered bedtime story service. The project is built with pure HTML, CSS, and JavaScript, and is optimized for seamless deployment on Vercel.

## Core Features

- **Clean & Minimalist UI**: A calming, aesthetically pleasing interface built with HTML5, CSS3, and modern JavaScript.
- **Email Subscription**: A simple email collection form that sends data to a third-party API.
- **Responsive Design**: Fully responsive layout that works on mobile, tablet, and desktop devices.
- **Automated Deployment**: Fully configured for continuous deployment on Vercel as a static site.

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (no frameworks)
- **Deployment**: Vercel (static site)
- **Data Processing**: Third-party API integration

## Project Structure

```
.
├── bedtime_story_landing.html  # Main landing page HTML
├── button_test.html            # A page for testing buttons
├── privacy.html                # Privacy Policy page
├── vercel.json                 # Vercel deployment configuration
└── README.md                   # This file
```

## Local Development Setup

To run this project on your local machine, simply open the HTML files in your browser. No server setup or dependencies are required.

## API Integration

The form on the landing page submits user email addresses to a third-party API:

- **Endpoint**: `http://10gjiv9932240.vicp.fun/submit`
- **Method**: POST
- **Payload**:
  ```json
  {
    "email": "user@example.com",
    "time": "2023-06-18T12:34:56.789Z"
  }
  ```

## Vercel Deployment

This project is ready for Vercel as a static site. Simply connect your GitHub repository to a new Vercel project, and it will automatically deploy the static files. 