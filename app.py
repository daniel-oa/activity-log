import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
from ai.gemini import generate_work_report, generate_daily_summary
from utils.word_export import export_to_word, create_word_document
from utils.app_mode import get_app_mode
from utils.api_key import get_api_key, render_api_key_sidebar
from utils.ui import load_css, page_header, date_label, section_heading, week_strip

st.set_page_config(page_title='Activity Log')
load_css()

app_mode = get_app_mode()

if app_mode == 'cloud':
    from utils.auth import render_authentication
    if not render_authentication():
        st.stop()

render_api_key_sidebar()
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.now()

if 'ai_error' not in st.session_state:
    st.session_state['ai_error'] = None

folder_path = Path(__file__).resolve().parent/'Records'
folder_path.mkdir(parents=True, exist_ok=True)
daily_summary_template_path = Path('templates/daily_summary_template.docx')
work_report_template_path = Path('templates/work_report_template.docx')

def go_previous():
    st.session_state['selected_date'] -= timedelta(days=1)
def go_today():
    st.session_state['selected_date'] = datetime.now()
def go_next():
    st.session_state['selected_date'] += timedelta(days=1)

selected_date = st.session_state['selected_date']
date_str = selected_date.strftime('%Y-%m-%d')
file_name = f'{date_str}.txt'
file_path = folder_path/file_name
work_report_file_name = f'{date_str} Work Report.txt'
work_report_file_path = folder_path/work_report_file_name
daily_summary_file_name = f'{date_str} Daily Summary.txt'
daily_summary_file_path = folder_path/daily_summary_file_name

if 'text_date' not in st.session_state:
    st.session_state['text_date'] = selected_date.date()

if 'work_report_date' not in st.session_state:
    st.session_state['work_report_date'] = selected_date.date()

if 'daily_summary_date' not in st.session_state:
    st.session_state['daily_summary_date'] = selected_date.date()

if 'daily_text' not in st.session_state:
    if app_mode == 'cloud':
        from utils.records import load_record
        st.session_state['daily_text'] = load_record(date_str, 'daily_note')
    elif file_path.exists() and file_path.is_file():
        st.session_state['daily_text'] = file_path.read_text(encoding='utf-8')
    else:
        st.session_state['daily_text'] = ''

if selected_date.date() != st.session_state['text_date']:
    if app_mode == 'cloud':
        from utils.records import load_record
        st.session_state['daily_text'] = load_record(date_str, 'daily_note')
    elif file_path.exists() and file_path.is_file():
        st.session_state['daily_text'] = file_path.read_text(encoding = 'utf-8')
    else:
        st.session_state['daily_text'] =''
    st.session_state['text_date'] = selected_date.date()

if 'work_report' not in st.session_state:
    if app_mode == 'cloud':
        from utils.records import load_record
        st.session_state['work_report'] = load_record(date_str,'work_report')
    elif work_report_file_path.exists() and work_report_file_path.is_file():
        st.session_state['work_report'] = work_report_file_path.read_text(encoding='utf-8')
    else:
        st.session_state['work_report'] = ''

if 'daily_summary' not in st.session_state:
    if app_mode == 'cloud':
        from utils.records import load_record
        st.session_state['daily_summary'] = load_record(date_str, 'daily_summary')
    elif daily_summary_file_path.exists() and daily_summary_file_path.is_file():
        st.session_state['daily_summary'] = daily_summary_file_path.read_text(encoding = 'utf-8')
    else:
        st.session_state['daily_summary'] = ''

if selected_date.date() != st.session_state['work_report_date']:
    if app_mode == 'cloud':
        from utils.records import load_record
        st.session_state['work_report'] = load_record(date_str, 'work_report')
    elif work_report_file_path.exists() and work_report_file_path.is_file():
        st.session_state['work_report'] = work_report_file_path.read_text(encoding='utf-8')
    else:
        st.session_state['work_report'] = ''
    st.session_state['work_report_date'] = selected_date.date()

if selected_date.date() != st.session_state['daily_summary_date']:
    if app_mode == 'cloud':
        from utils.records import load_record
        st.session_state['daily_summary'] = load_record(date_str, 'daily_summary')
    elif daily_summary_file_path.exists() and daily_summary_file_path.is_file():
        st.session_state['daily_summary'] = daily_summary_file_path.read_text(encoding='utf-8')
    else:
        st.session_state['daily_summary'] = ''
    st.session_state['daily_summary_date'] = selected_date.date()

page_header('Activity Log', 'Capture your day. Keep the details.')
date_label(selected_date.strftime('%A %d %B, %Y'))

previous,today,next = st.columns(3)
with previous:
    previous_button = st.button('← Previous',on_click=go_previous, width='stretch')
with today:
    today_button = st.button('Today',on_click=go_today, width='stretch', type ='primary')
with next:
    if selected_date.date() < datetime.now().date():
        next_button = st.button('Next →',on_click=go_next, width='stretch')

section_heading("Today's Activity", "Write freely. Don't worry about organizing it.")
text = st.text_area(' ', height = 'content', key='daily_text', label_visibility='collapsed')

if st.button('Save Note', width='stretch', type='primary'):
        if app_mode == 'cloud':
            from utils.records import save_record
            save_record(st.session_state['selected_date'].strftime('%Y-%m-%d'), 'daily_note', text)
        else:
            file_path.write_text(text, encoding= 'utf-8')
        st.success('Note saved successfully.')

section_heading("Create from today's notes")

left, right = st.columns([1,1])
with left:
    if st.button('Daily Summary', width = 'stretch'):
        api_key = get_api_key()
        if not api_key:
            st.warning('Enter your Gemini API key in the sidebar to generate a summary.')
        else:
            with st.spinner('Generating daily summary...'):
                result = generate_daily_summary(text, api_key)
            if result['success']:
                st.session_state['daily_summary'] = result['summary']
                st.session_state['ai_error'] = None
            else:
                st.session_state['ai_error'] = result['error']

with right:
    if st.button('Work Report',  width = 'stretch'):
        api_key = get_api_key()
        if not api_key:
            st.warning('Enter your Gemini API key in the sidebar to generate a report.')
        else:
            with st.spinner('Generating work report...'):
                result = generate_work_report(text, api_key)
            if result['success']:
                st.session_state['work_report'] = result['report']
                st.session_state['ai_error'] = None
            else:
                st.session_state['ai_error'] = result['error']

week_start = selected_date - timedelta(days=(selected_date.weekday()+1)%7)
day_list = [week_start+timedelta(days=day) for day in range(7)]

exist_dict = {}

for date in day_list:
    if app_mode == 'cloud':
        from utils.records import load_record
        has_record = bool(load_record(date.strftime('%Y-%m-%d'), 'daily_note'))
    else:
        date_file_name = f"{date.strftime('%Y-%m-%d')}.txt"
        date_file_path = folder_path/date_file_name
        has_record = date_file_path.is_file()

    exist_dict[date.strftime('%A %d %b')] = has_record

if st.session_state['ai_error']:
    st.error(f"AI generation failed: {st.session_state['ai_error']}")

if st.session_state['daily_summary'] == '' and st.session_state['work_report'] == '':
    st.markdown("<div class='al-empty'>Your generated daily summary and work report will appear here.</div>",
                unsafe_allow_html=True)

if st.session_state['daily_summary'] != '':
    section_heading('Daily Summary')
    with st.container(border=True):
        st.text_area('Edit Daily Summary', key = 'daily_summary', height = 'content')
        if st.button('Save Daily Summary', width = 'stretch'):
                if app_mode == 'cloud':
                    from utils.records import save_record
                    save_record(date_str, 'daily_summary', st.session_state['daily_summary'])
                else:
                    daily_summary_file_path.write_text(st.session_state['daily_summary'], encoding='utf-8')
                st.success('Daily Summary saved successfully.')

        if app_mode == 'cloud':
            try:
                word_buffer = create_word_document(daily_summary_template_path,
                                                    {'{{date}}':selected_date.strftime('%A %d %B %Y.'),
                                                    '{{daily_summary}}': st.session_state['daily_summary']})
                st.download_button('Download Daily Summary', data = word_buffer, file_name=f'{date_str} Daily Summary.docx',
                                    mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                    key=f'download_daily_summary_{date_str}', width='stretch')
            except Exception:
                st.error('Could not prepare the Word document. Please try again.')
        else:
            if st.button('Export Daily Summary', width='stretch'):
                try:
                    with st.spinner('Exporting to Word...'):
                        export_to_word(st.session_state['daily_summary'], folder_path/f'{date_str} Daily Summary.docx',
                                       daily_summary_template_path, {'{{date}}':selected_date.strftime('%A %d %B %Y.'),
                                                                     '{{daily_summary}}': st.session_state['daily_summary']})
                        st.success('Daily Summary exported successfully!')
                except PermissionError:
                    st.error('Please close the Word document and try again.')
                except Exception:
                    st.error('Could not export the Word document. Please try again.')

if st.session_state['work_report'] != '':
    section_heading('Work Report')
    with st.container(border=True):
        st.text_area('Edit Work Report', key = 'work_report', height = 'content')
        if st.button('Save Work Report', width = 'stretch'):
            if app_mode == 'cloud':
                from utils.records import save_record
                save_record(date_str,'work_report', st.session_state['work_report'])
            else:
                work_report_file_path.write_text(st.session_state['work_report'], encoding='utf-8')
            st.success('Work Report saved successfully.')

        if app_mode == 'cloud':
            try:
                word_buffer = create_word_document(work_report_template_path, {'{{date}}': selected_date.strftime('%A %d %B %Y.'),
                                                                                '{{work_report}}': st.session_state['work_report']})
                st.download_button('Download Work Report',data=word_buffer,file_name=f'{date_str} Work Report.docx',
                                    mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                    key=f'download_work_report_{date_str}', width='stretch')
            except Exception:
                st.error('Could not prepare the Word document. Please try again.')
        else:
            if st.button('Export Work Report', width='stretch'):
                try:
                    with st.spinner('Exporting to Word...'):
                        export_to_word( st.session_state['work_report'], folder_path / f'{date_str} Work Report.docx',
                            work_report_template_path, {'{{date}}': selected_date.strftime('%A %d %B %Y.'),
                                                        '{{work_report}}': st.session_state['work_report']})
                    st.success('Work Report exported successfully!')
                except PermissionError:
                    st.error('Please close the Word document and try again.')
                except Exception:
                    st.error('Could not export the Word document. Please try again.')

section_heading('This Week')
week_strip(day_list, exist_dict)