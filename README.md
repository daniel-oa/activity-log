# Activity Log

A simple Streamlit app for capturing daily activities and turning them into useful summaries and reports with AI.

## Features

- Free-form daily activity logging
- Daily Summary generation
- Work Report generation
- Weekly Summary generation
- Editable generated outputs
- Local saving of activity records and generated outputs
- Word export using customizable default report templates

## How it works

Write your activities naturally without worrying about organizing them.

Activity Log keeps the original notes and can use them to generate:

- A personal Daily Summary
- A professional Work Report
- A higher-level Weekly Summary

Generated outputs can be edited before being saved or exported to Word.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/daniel-oa/activity-log.git
cd activity-log
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it according to your operating system.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Gemini API key

Set the `GEMINI_API_KEY` environment variable.

Do not add your API key directly to the source code.

### 5. Run the app

```bash
streamlit run app.py
```

## Data and privacy

Activity records are stored locally in the `Records/` folder.

The `Records/` folder is excluded from Git so personal activity records are not committed to the repository.

## Project structure

```text
Activity Log/
├── app.py
├── ai/
├── pages/
├── templates/
├── Records/
├── utils/
├── requirements.txt
├── .gitignore
└── README.md
```

## Current scope

This is an early version of Activity Log focused on daily activity capture, AI-generated summaries and reports, and Word export.