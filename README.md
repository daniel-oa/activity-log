
# Activity Log

**Turn everyday activity notes into summaries and professional reports with AI.**

Activity Log is a Streamlit application for recording daily activities, generating AI-assisted summaries and work reports, and exporting polished documents to Word. It supports local record storage and a cloud mode with user authentication and Supabase-backed storage.

**[Try Activity Log](https://activity-log.streamlit.app)** · **[View Source Code](https://github.com/daniel-oa/activity-log)**

## Features

- **Daily Activity Logging** — Record activities naturally without needing to organize them into a formal report.
- **AI-Generated Daily Summaries** — Turn daily notes into concise summaries.
- **Professional Work Reports** — Transform activity logs into structured work reports.
- **Weekly Summaries** — Consolidate activities across a week into a higher-level summary.
- **Editable Outputs** — Review and edit generated summaries and reports before saving or exporting.
- **Word Export** — Download reports as Word documents using customizable report templates.
- **Local and Cloud Storage** — Store records locally or use Supabase-backed cloud storage.
- **User Authentication** — Create an account, confirm your email, and sign in to access your records in cloud mode.
- **AI Integration** — Use Google's Gemini API to generate summaries and reports.

## How It Works

1. **Record:** Write your daily activities in plain language.
2. **Generate:** Use AI to create a daily summary, work report, or weekly summary.
3. **Review:** Edit the generated content to make sure it accurately reflects your work.
4. **Save:** Save the output so it can be retrieved later.
5. **Export:** Download your report as a Word document.

The goal is to make activity reporting less repetitive while keeping the original notes available for reference.

## Technology Stack

- **Python** — Application logic and data handling
- **Streamlit** — User interface
- **Google Gemini API** — AI-assisted text generation
- **Supabase** — Authentication and cloud data storage
- **python-docx** — Word document generation

## Getting Started

### Prerequisites

- Python installed on your computer
- A Google Gemini API key for AI generation

### 1. Clone the repository

```bash
git clone https://github.com/daniel-oa/activity-log.git
cd activity-log
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Set the `GEMINI_API_KEY` environment variable, or use the application's API key input where available.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**macOS / Linux:**

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Get an API key through [Google AI Studio](https://aistudio.google.com/).

Never commit API keys or other secrets to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application should open in your browser.

## Storage and Privacy

Activity Log supports two operating modes:

- **Local mode:** Activity records and generated outputs are stored in the local `Records/` directory.
- **Cloud mode:** Supabase handles authentication and cloud record storage, with access policies intended to restrict users to their own records.

AI generation sends the relevant activity content to the configured Gemini API. Avoid submitting sensitive information unless you are comfortable sharing it with the service.

The `Records/` directory and secret configuration files should remain excluded from version control. Never expose Supabase service-role keys or other privileged credentials in client-facing code.

Cloud mode requires the appropriate Supabase configuration and database policies. Follow the project's configuration in `utils/` when setting up your own deployment.

## Project Structure

```text
activity-log/
├── ai/             # AI generation logic
├── pages/          # Additional Streamlit pages
├── templates/      # Report templates
├── utils/          # Authentication, storage, and helpers
├── Records/        # Local activity records (not committed)
├── app.py          # Main application
├── requirements.txt
├── .gitignore
└── README.md
```

## Current Scope

Activity Log focuses on daily activity capture, AI-assisted reporting, persistent record storage, and Word document export.

Generated content should be reviewed before use, especially when preparing formal work reports. AI-generated summaries may omit details or misinterpret notes.

## Future Improvements

- Automatically save generated outputs
- Further improve report formatting and customization
- Expand activity analytics and reporting options

## Author

**Daniel Onabanjo**

[GitHub](https://github.com/daniel-oa)
