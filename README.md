# LinkedIn Profile Scraper & Analyzer

A powerful Streamlit application designed to search, fetch, analyze, and summarize LinkedIn profiles. This tool offers multiple search methods, including by name with filters, direct URL, and bulk processing from a CSV file. It leverages `staffspy` for efficient data scraping and an integrated AI service for intelligent profile summarization.

---

## ✨ Key Features

-   **Multiple Search Methods**: Find profiles by **name** (with filters like company, school, and location), direct **profile URL**, or in **bulk via CSV** upload.
-   **Detailed Profile View**: Renders structured, easy-to-read information for skills, work experience, and certifications.
-   **AI-Powered Summaries**: Automatically generates a concise, insightful summary of a candidate's professional profile using an integrated AI model.
-   **Smart Caching**: Avoids redundant data fetching by using a "freshness" setting (e.g., 30 or 60 days), saving time and ensuring efficient operation.
-   **User-Friendly Interface**: Built with Streamlit for a clean, interactive, and responsive user experience.

---

## 🏗️ Project Architecture

The application uses a service-oriented architecture where the Streamlit UI interacts with a set of backend services to handle API calls, data processing, and caching.

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
        E["Profile Service (Single Fetch & Cache)"]
        F["Bulk Service (CSV Processing)"]
        G["Harvest API Service (Name Search)"]
        H["Summarizer Service (AI Summary)"]
        I[StaffSpy Wrapper]
    end

    subgraph "External Systems & Data"
        J[LinkedIn]
        K[Database / Cache]
        L[AI Model API]
    end

    A --> B & C & D

    B --> G --> I
    C --> E
    D --> F --> E

    E --> I --> J
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
-   API key for an AI service (e.g., OpenAI) for the summarization feature.

---

## 🛠️ Installation Guide

### 1. Clone the Repository

First, clone the project to your local machine.
```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the environment
python3 -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python libraries using pip.

```bash
pip install streamlit pandas requests python-dotenv sqlalchemy psycopg2-binary staffspy
# You may also need to install the library for your chosen AI service
# pip install openai
```

### 4. Configure Environment Variables

Create a file named `.env` in the root directory of the project. This file will securely store your credentials and API keys. Add the following content to it:

```env
# LinkedIn Credentials used by StaffSpy
LINKEDIN_USERNAME="your_linkedin_email@example.com"
LINKEDIN_PASSWORD="your_linkedin_password"

# API Key for the AI Summarizer Service (e.g., OpenAI)
OPENAI_API_KEY="sk-..."

# Optional: Add database connection string if using a persistent database
# DATABASE_URL="postgresql://user:password@host:port/database"
```

---

## 🚀 How to Run the App

Once the installation is complete and your `.env` file is configured, start the Streamlit application with the following command:

```bash
streamlit run app.py
```

Open the URL displayed in your terminal (typically `http://localhost:8501`) in your web browser to access the application.

---

## 🖥️ How to Use the App

The application offers three intuitive workflows for profile scraping:

1.  **Search by Name**:
    -   Select the **"Search by Name"** option.
    -   Enter the full name of the individual.
    -   (Optional) Add filters such as company, school, or location to refine your search.
    -   Click **"Search Profiles"** to view a list of potential matches.
    -   Select a profile from the list to fetch its full details and AI-generated summary.

2.  **Search by Id (URL)**:
    -   Select the **"Search by Id"** option.
    -   Paste the full LinkedIn profile URL into the text field.
    -   Click **"Fetch Profile"** to instantly retrieve, display, and summarize the profile data.

3.  **Search by CSV**:
    -   Select the **"Search by CSV"** option.
    -   Upload a CSV file containing a column named **`url`**, where each row is a LinkedIn profile URL.
    -   Click **"Fetch All Profiles"** to start the bulk processing job.
    -   The application will iterate through each URL, displaying the results and summaries sequentially.

---

## ⚡ Troubleshooting

| Issue                                    | Solution                                                                                                                               |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError`                    | Ensure you have activated your virtual environment (`source venv/bin/activate`) before running the app. Re-run the `pip install` command from Step 3 to install any missing packages. |
| LinkedIn Login Fails                     | Verify that your `LINKEDIN_USERNAME` and `LINKEDIN_PASSWORD` in the `.env` file are correct. LinkedIn may sometimes require a manual login or captcha verification from a new IP address. |
| AI Summary Fails or `AuthenticationError` | Check that your `OPENAI_API_KEY` (or other service key) in the `.env` file is valid and has not expired. Ensure your account has sufficient credits. |
| Streamlit Not Opening                    | Confirm that no other process is using port 8501. Check your firewall settings and try navigating to `http://localhost:8501` manually in your browser. |

