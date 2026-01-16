# UX Tester

**UX Tester** is a powerful, AI-driven web application designed to audit websites for User Experience (UX), performance, and accessibility issues. It provides actionable insights, generates CSS fixes, and continuously monitors your digital assets.

![UX Tester Dashboard](https://via.placeholder.com/800x400?text=UX+Tester+Dashboard)

##  Features

-   ** AI-Powered Scanning**: Analyzes any URL for UX friction points using Gemini AI.
-   ** Detailed Audits**: Scores performance, accessibility, SEO, and best practices.
-   ** One-Click Fixes**: Generates code snippets (CSS/JS) to resolve identified issues.
-   ** Advanced Analytics**: Visualizes historical performance trends and category breakdowns.
-   ** Bulk Scanning**: Audit multiple URLs simultaneously and export results to CSV/PDF.
-   ** Real-Time Monitoring**: Automatically watches websites and alerts on score drops.
-   ** Public API**: Developer-friendly API for integrating audits into CI/CD pipelines.

##  Tech Stack

-   **Backend**: Python (Flask)
-   **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (CDN)
-   **Scheduling**: APScheduler
-   **Visualization**: Chart.js
-   **Icons**: Lucide Icons

##  Prerequisites

-   **Python 3.8+**
-   **Google Gemini API Key** (Get one [here](https://makersuite.google.com/app/apikey))

##  Installation

1.  **Clone the repository** (or unzip source):
    ```bash
    git clone https://github.com/yourusername/ux-tester.git
    cd ux-tester
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

##  Running the App

Start the Flask development server:

```bash
python app.py
```

Open your browser and navigate to:
**http://127.0.0.1:5000**

## 📖 API Documentation

The UX Tester exposes a REST API for automated audits.

**Base URL**: `http://localhost:5000/api/v1`

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/scan` | POST | Scan a URL (Requires `x-api-key`) |
| `/health` | GET | Check service status |

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/v1/scan \
  -H "x-api-key: ux_test_12345" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

View full docs at: `http://127.0.0.1:5000/api-docs`

##  Project Structure

```
ux-tester/
├── app.py              # Main Flask Application & Logic
├── requirements.txt    # Python Dependencies
├── .env                # Environment Variables (API Keys)
├── templates/
│   ├── index.html      # Main Dashboard & UI
│   └── api_docs.html   # API Documentation Page
└── static/
    └── style.css       # Custom Styles
```

##  License

MIT License. Free for personal and commercial use.
