import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
from ai.gemini import generate_work_report, generate_daily_summary
from utils.word_export import export_to_word

st.set_page_config(page_title='Activity Log')

if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.now()

if 'ai_error' not in st.session_state:
    st.session_state['ai_error'] = None

folder_path = Path(__file__).resolve().parent/'Records'
folder_path.mkdir(parents=True, exist_ok=True)
template_path = Path('templates/daily_summary_template.docx')

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
    if file_path.exists() and file_path.is_file():
        st.session_state['daily_text'] = file_path.read_text(encoding='utf-8')
    else:
        st.session_state['daily_text'] = ''

if selected_date.date() != st.session_state['text_date']:
    if file_path.exists() and file_path.is_file():
        st.session_state['daily_text'] = file_path.read_text(encoding = 'utf-8')
    else:
        st.session_state['daily_text'] =''
    st.session_state['text_date'] = selected_date.date()

if 'work_report' not in st.session_state:
    if work_report_file_path.exists() and work_report_file_path.is_file():
        st.session_state['work_report'] = work_report_file_path.read_text(encoding='utf-8')
    else:
        st.session_state['work_report'] = ''

if 'daily_summary' not in st.session_state:
    if daily_summary_file_path.exists() and daily_summary_file_path.is_file():
        st.session_state['daily_summary'] = daily_summary_file_path.read_text(encoding = 'utf-8')
    else:
        st.session_state['daily_summary'] = ''

if selected_date.date() != st.session_state['work_report_date']:
    if work_report_file_path.exists() and work_report_file_path.is_file():
        st.session_state['work_report'] = work_report_file_path.read_text(encoding='utf-8')
    else:
        st.session_state['work_report'] = ''
    st.session_state['work_report_date'] = selected_date.date()

if selected_date.date() != st.session_state['daily_summary_date']:
    if daily_summary_file_path.exists() and daily_summary_file_path.is_file():
        st.session_state['daily_summary'] = daily_summary_file_path.read_text(encoding='utf-8')
    else:
        st.session_state['daily_summary'] = ''
    st.session_state['daily_summary_date'] = selected_date.date()

st.markdown("""
                <div style = 'text-align: center; margin-bottom: 4px;'>
                    <div style = 'font-size: 40px; font-weight: 700;'>
                        Activity Log
                    </div>
                    <div style = 'font-size: 16px; color: #888;'>
                        Capture your day. Keep the details.
                    </div>
                </div>
            """, unsafe_allow_html= True)

st.markdown(f"""<div style = 'text-align: center;  font-size: 18px; font-weight: 500; margin-bottom: 18px;'>
            {selected_date.strftime('%A %d %B, %Y')}
            </div>""", unsafe_allow_html = True)

previous,today,next = st.columns(3)
with previous:
    previous_button = st.button('← Previous',on_click=go_previous, width='stretch')
with today:
    today_button = st.button('Today',on_click=go_today, width='stretch', type ='primary')
with next:
    if selected_date.date() < datetime.now().date():
        next_button = st.button('Next →',on_click=go_next, width='stretch')

st.markdown(
    """
    <div style = 'font-size: 24px; font-weight: 600; margin-top: 32px; margin-bottom: 8px;'>
        📖 Today's Activity
    </div>
    <div style = 'font-size: 15px; color: #888; margin-bottom: 8px;'>
        Write freely. Don't worry about organizing it.
    </div>
    """,
    unsafe_allow_html= True
)
text = st.text_area(' ', height = 'content', key='daily_text', label_visibility='collapsed')

if st.button('Save Note', width='stretch', type='primary'):
        file_path.write_text(text, encoding= 'utf-8')

st.markdown("""
        <div style = 'font-size: 24px; font-weight: 600; margin-top: 32px; margin-bottom: 14px;'>
            ✨ Create from today's notes
        </div>
        """, unsafe_allow_html= True)

left, right = st.columns([1,1])
with left:
    if st.button('Daily Summary', width = 'stretch'):
        with st.spinner('Generating daily summary...'):
            result = generate_daily_summary(text)
        if result['success']:
            st.session_state['daily_summary'] = result['summary']
            st.session_state['ai_error'] = None
        else:
            st.session_state['ai_error'] = result['error']
    
with right:
    if st.button('Work Report',  width = 'stretch'):
        with st.spinner('Generating work report...'):
            result = generate_work_report(text)
        if result['success']:
            st.session_state['work_report'] = result['report']
            st.session_state['ai_error'] = None
        else:
            st.session_state['ai_error'] = result['error']
    
week_start = selected_date - timedelta(days=(selected_date.weekday()+1)%7)
day_list = [week_start+timedelta(days=day) for day in range(7)]

exist_dict = {}
for date in day_list:
    date_file_name = f"{date.strftime('%Y-%m-%d')}.txt"
    date_file_path = folder_path/date_file_name
    if date_file_path.exists() and date_file_path.is_file():
        exist_dict.update({date.strftime('%A %d %b'): True})
    else:
        exist_dict.update({date.strftime('%A %d %b'): False})

if st.session_state['ai_error']:
    st.error(st.session_state['ai_error'])

if st.session_state['daily_summary'] != '':
    st.markdown("""<div style = 'font-size:24px; font-weight:600; margin-top:32px; margin-bottom: 8px'>
                📔 Daily Summary
                </div>""", unsafe_allow_html = True)
    st.text_area('Edit Daily Summary', key = 'daily_summary', height = 'content')
    if st.button('Save Daily Summary', width = 'stretch'):
            daily_summary_file_path.write_text(st.session_state['daily_summary'], encoding='utf-8')
    if st.button('Export Daily Summary', width = 'stretch'):
        with st.spinner('Exporting to Word...'):
            export_to_word(st.session_state['daily_summary'], folder_path/f'{date_str} Daily Summary.docx', template_path)  
        st.success('Word document exported successfully')
    
if st.session_state['work_report'] != '':
    st.markdown("""<div style = 'font-size:24px; font-weight:600; margin-top:32px; margin-bottom: 8px'>
                    💼 Work Report
                    </div>""", unsafe_allow_html = True)
    st.text_area('Edit Work Report', key = 'work_report', height = 'content')
    if st.button('Save Work Report', width = 'stretch'):
        work_report_file_path.write_text(st.session_state['work_report'], encoding='utf-8')
    if st.button('Export Work Report', width = 'stretch'):
        with st.spinner('Exporting to Word...'):
            export_to_word(st.session_state['work_report'], folder_path/f'{date_str} Work Report.docx')  
        st.success('Word document exported successfully')
st.markdown("""<div style = 'font-size:24px; font-weight:600; margin-top:32px; margin-bottom: 14px'>
                🗓️ This Week
                </div>""", unsafe_allow_html = True)

week_columns = st.columns(7) 
for column, date in zip(week_columns, day_list):
    with column:
        is_today= date.date() == datetime.now().date()
        has_record = exist_dict[date.strftime('%A %d %b')]
        day_weight = '700' if is_today else '400'
        day_color = '#000' if is_today else '#888'
        status = '✓' if has_record else '—'

        st.markdown(f"""
                    <div style = 'text-align: center;'>
                        <div style = 'font-size: 13px; font-weight: {day_weight}; color: {day_color};'>
                            {date.strftime('%a')}
                        </div>
                        <div style = 'font-size: 20px; font-weight: 600; margin-top: 4px;'>
                            {status}
                        </div>
                    </div>
                    """,unsafe_allow_html= True)