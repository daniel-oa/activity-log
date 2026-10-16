
# Activity Log 📝

**Turn everyday activity notes into useful summaries and work reports.**

Activity Log is a Streamlit app for keeping track of what you do throughout the day without having to write every update as a formal report. Log activities naturally, then use AI to turn those notes into daily summaries, professional work reports, and weekly overviews.

Less time formatting reports. More time getting things done.

🔗 **[Try Activity Log](https://activity-log.streamlit.app)** — Access it online with an account, or [run it locally](#run-locally) without creating one.

## What can it do?

- **Log daily activities** — Record what you worked on in your own words.
- **Generate daily summaries** — Turn your notes into a clear overview of the day.
- **Create work reports** — Convert informal activity logs into more professional reports.
- **Review the week** — Generate a weekly summary from your recorded activities.
- **Edit AI-generated content** — Refine the output before saving or exporting it.
- **Export to Word** — Download summaries and reports as Word documents.
- **Keep your records** — Use local storage or cloud storage with account authentication, depending on the app mode.

## How it works

1. **Write it down.** Record your activities as they happen or at the end of the day.
2. **Generate.** Choose a daily summary, work report, or weekly summary.
3. **Review and edit.** Check the generated content and make any necessary corrections.
4. **Save or export.** Save your output in the app or download it as a Word document.

The goal is simple: you shouldn't have to remember everything you did at the end of the day or start every report from scratch.

## Built with

- Python
- Streamlit
- Google Gemini API
- Supabase
- python-docx

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/daniel-oa/activity-log.git
cd activity-log
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Set the `GEMINI_API_KEY` environment variable, or enter your key in the app's API-key input where available.

You can get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey). Keep API keys and other secrets out of your source code and Git history.

### 5. Start the app

```bash
streamlit run app.py
```

Cloud mode also requires the appropriate Supabase configuration. The exact configuration depends on the app's deployment setup.

## Storage and privacy

Activity Log supports local and cloud modes:

- **Local mode:** Activity records and generated outputs are stored locally in the `Records/` directory.
- **Cloud mode:** User authentication and cloud records are handled through Supabase, with database access controlled by Row Level Security policies.

AI generation sends the relevant activity content to Google Gemini to produce the requested output. Avoid entering information you would not want processed by the service.

## What's next?

Activity Log is a work in progress. Planned improvements include:

- **Better Word templates** — The current templates are basic and functional. More polished layouts, improved formatting, and greater customization are planned.
- **Automatic saving** — Save generated summaries and reports without requiring a separate manual save action.
- **More useful insights** — Build on recorded activities to make weekly reviews more informative.

## A note on AI-generated content

Generated summaries and reports may need editing. Review the output for accuracy before using it as a formal record or submitting it as a work report.
