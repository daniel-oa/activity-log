import html
from datetime import datetime
from pathlib import Path

import streamlit as st

# utils/ui.py -> project root -> assets/style.css (independent of the working directory)
CSS_PATH = Path(__file__).resolve().parent.parent / 'assets' / 'style.css'


def load_css():
    """Inject assets/style.css. If the file is missing the app still works, just unstyled."""
    try:
        css = CSS_PATH.read_text(encoding='utf-8')
    except OSError:
        return
    # Blank lines can end an HTML block in Markdown, so strip them before injecting.
    css = '\n'.join(line for line in css.splitlines() if line.strip())
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


def page_header(title, subtitle):
    st.markdown(
        f"<div class='al-header'>"
        f"<div class='al-title' role='heading' aria-level='1'>{html.escape(title)}</div>"
        f"<div class='al-subtitle'>{html.escape(subtitle)}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def date_label(text):
    st.markdown(f"<div class='al-date'>{html.escape(text)}</div>", unsafe_allow_html=True)


def section_heading(title, hint=''):
    hint_html = f"<div class='al-section-hint'>{html.escape(hint)}</div>" if hint else ''
    st.markdown(
        f"<div class='al-section'>"
        f"<div class='al-section-title' role='heading' aria-level='2'>{html.escape(title)}</div>"
        f"{hint_html}"
        f"</div>",
        unsafe_allow_html=True,
    )


def week_strip(day_list, exist_dict):
    """Read-only 7-day indicator. exist_dict is keyed by date.strftime('%A %d %b').
    The grid layout is inline so the strip stays on one row even if the stylesheet fails to load."""
    today = datetime.now().date()
    cells = []
    for date in day_list:
        has_record = exist_dict[date.strftime('%A %d %b')]
        classes = 'al-day'
        if has_record:
            classes += ' al-day-done'
        if date.date() == today:
            classes += ' al-day-today'
        state = 'note recorded' if has_record else 'no note'
        label = f"{date.strftime('%A %d %B')}: {state}"
        cells.append(
            f"<div class='{classes}' role='listitem' aria-label='{label}' style='min-width:0;'>"
            f"<div class='al-day-name'>{date.strftime('%a')}</div>"
            f"<div class='al-day-mark'></div>"
            f"</div>"
        )
    # One line, no indentation: indented lines would be parsed as a Markdown code block.
    st.markdown(
        f"<div class='al-week' role='list' "
        f"style='display:grid;grid-template-columns:repeat(7,minmax(0,1fr));'>"
        f"{''.join(cells)}</div>",
        unsafe_allow_html=True,
    )