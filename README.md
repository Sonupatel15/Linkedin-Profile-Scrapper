# LinkedIn Profile Scraper & Analyzer

This is an advanced Streamlit application designed to search, fetch, analyze, and summarize LinkedIn profiles. It offers multiple search methods, including by name with filters, direct URL, and bulk processing from a CSV file. The app leverages `staffspy` for data scraping and an AI service for intelligent profile summarization.

---

## ✨ Key Features

-   **Search by Name**: Find profiles using a name and optional filters like current company, past company, school, and location.
-   **Search by Profile URL**: Directly fetch and display data for a specific LinkedIn profile URL.
-   **Bulk Search via CSV**: Upload a CSV file with a 'url' column to fetch and process multiple profiles at once.
-   **Detailed Profile View**: Renders structured information for skills, work experience, and certifications.
-   **AI-Powered Summaries**: Automatically generates a concise summary of the candidate's profile using an AI model.
-   **Smart Caching**: Avoids re-fetching recent data by using a "freshness" setting, saving time and reducing risk.

---

## 🏗️ Project Architecture

The application follows a service-oriented architecture where the Streamlit UI interacts with a set of backend services to handle API calls, data processing, and caching.

```mermaid
flowchart TD
    subgraph "User Interface"
        A[Streamlit App]
    end

    subgraph "Search Methods"
        B[Search by Name]
        C[Search by ID/URL]
        D[Search by CSV]
    end

    subgraph "Backend Services"
        E[Profile Service (Single Fetch & Cache)]
        F[Bulk Service (CSV Processing)]
        G[Harvest API Service (Name Search)]
        H[Summarizer Service (AI Summary)]
        I[StaffSpy Wrapper]
    end

    subgraph "External Systems & Data"
        J[LinkedIn]
        K[Database / Cache]
        L[AI Model API]
    end

    A --> B
    A --> C
    A --> D

    B --> G --> I
    C --> E
    D --> F --> E

    E --> I
    I --> J
    E <--> K
    E --> H --> L

    H --> A
    E --> A
    F --> A
```

---

## ⚙️ Requirements

-   Python 3.10+
-   macOS, Windows, or Linux
-   An active LinkedIn account
-   API keys for any external services used (e.g., OpenAI for summarization).

---

## 🛠️ Installation Guide

### 1. Clone the Repository

First, get the project files on your local machine.
```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment (Recommended)

Create and activate a virtual environment to keep dependencies isolated.

```bash
# Create the environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

### 3. Install Required Packages

Install all the necessary Python libraries with a single command.

```bash
pip install streamlit pandas requests python-dotenv sqlalchemy psycopg2-binary staffspy
```
*Note: You may also need to install a library for the AI summarizer, such as `openai`.*

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of your project. This file will store your sensitive credentials securely.

```env
# LinkedIn Credentials used by StaffSpy
LINKEDIN_USERNAME="your_linkedin_email@example.com"
LINKEDIN_PASSWORD="your_linkedin_password"

# API Key for the AI Summarizer Service (e.g., OpenAI)
OPENAI_API_KEY="sk-..."

# Add any other API keys or database URLs if required
# DATABASE_URL="..."
```

---

## 🚀 How to Run the App

With your environment activated and `.env` file configured, run the following command in your terminal:

```bash
streamlit run app.py
```

Navigate to the local URL displayed in your terminal (usually `http://localhost:8501`) to start using the application.

---

## 🖥️ App Workflow

The application provides three distinct methods for finding and analyzing profiles:

1.  **Search by Name**:
    -   Select the "Search by Name" option.
    -   Enter the full name of the person you are looking for.
    -   Optionally, add filters like company, school, or location to narrow the results.
    -   Click "Search Profiles" to get a list of potential matches.
    -   Select a profile from the list to fetch and display its full details and AI summary.

2.  **Search by Id (URL)**:
    -   Select the "Search by Id" option.
    -   Paste the full LinkedIn profile URL into the input field.
    -   Click "Fetch Profile" to immediately retrieve, display, and summarize the data.

3.  **Search by CSV**:
    -   Select the "Search by CSV" option.
    -   Upload a CSV file that contains a column named `url` with a list of LinkedIn profile URLs.
    -   Click "Fetch All Profiles" to begin the bulk processing job.
    -   The app will iterate through each URL, fetch the data, and display the profiles and their summaries one by one.

---

## ⚡ Troubleshooting

| Issue                                    | Fix                                                                                                                               |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError`                    | Ensure all packages are installed in your active virtual environment by running `pip install -r requirements.txt` (if you have one) or the install command from Step 3. |
| LinkedIn Login Fails                     | Double-check your `LINKEDIN_USERNAME` and `LINKEDIN_PASSWORD` in the `.env` file. LinkedIn may occasionally require a manual login or captcha to authorize a new location. |
| AI Summary Fails or `AuthenticationError` | Verify that your `OPENAI_API_KEY` (or other AI service key) in the `.env` file is correct and has sufficient credits.               |
| Streamlit Not Opening                    | Check your firewall settings or try navigating to `http://localhost:8501` manually in your web browser.                             |

