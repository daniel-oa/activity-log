import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
from ai.gemini import generate_weekly_summary
from utils.word_export import export_to_word

st.set_page_config(page_title='Weekly Summary')

st.markdown("""
                <div style = 'text-align: center; margin-bottom: 4px;'>
                    <div style = 'font-size: 40px; font-weight: 700;'>
                        Weekly Summary
                    </div>
                    <div style = 'font-size: 16px; color: #888;'>
                        Look back at your week
                    </div>
                </div>
                """,unsafe_allow_html= True)
def go_previous_week():
    st.session_state['selected_date'] -= timedelta(days=7)
def go_this_week():
    st.session_state['selected_date'] = datetime.now()
def go_next_week():
    st.session_state['selected_date'] += timedelta(days=7)

if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.now()

if 'weekly_summary' not in st.session_state:
    st.session_state['weekly_summary'] = ''

if 'weekly_summary_date' not in st.session_state:
    st.session_state['weekly_summary_date'] = None

if 'ai_error' not in st.session_state:
    st.session_state['ai_error'] = None

selected_date = st.session_state['selected_date']
week_start = selected_date - timedelta(days = (selected_date.weekday() + 1) % 7)
week_end = week_start + timedelta(days = 6)

st.markdown(f"""<div style = 'text-align: center; font-size:18px; margin-bottom: 18px'>
                {week_start.strftime('%d %B')} - {week_end.strftime('%d %B, %Y')}
                </div>""", unsafe_allow_html = True)

previous,today,next = st.columns(3)
with previous:
    previous_button = st.button('← Previous Week',on_click=go_previous_week, width='stretch')
with today:
    today_button = st.button('This Week',on_click=go_this_week, width='stretch', type ='primary')
with next:
    if selected_date.date() < datetime.now().date():
        next_button = st.button('Next Week →',on_click=go_next_week, width='stretch')

folder_path = Path(__file__).resolve().parent.parent/'Records'
folder_path.mkdir(parents=True, exist_ok=True)
week_str = f"{week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}"
weekly_summary_file_name = f'{week_str} Weekly Summary.txt'
weekly_summary_file_path = folder_path/weekly_summary_file_name
weekly_summary_template_path = Path('templates/weekly_summary_template.docx')

day_list = [week_start+timedelta(days=day) for day in range(7)]
weekly_text = ''

if st.session_state['weekly_summary_date'] != week_start.date():
    if weekly_summary_file_path.exists() and weekly_summary_file_path.is_file():
        st.session_state['weekly_summary'] = weekly_summary_file_path.read_text(encoding='utf-8')
    else:
        st.session_state['weekly_summary'] = ''
    st.session_state['weekly_summary_date'] = week_start.date()

st.markdown("""<div style = 'font-size:24px; font-weight: 600; margin-top:32px; margin-bottom: 14px'>
                📖 Daily Records
                </div>""", unsafe_allow_html = True)

exist_dict = {}
for date in day_list:
    date_file_name = f"{date.strftime('%Y-%m-%d')}.txt"
    date_file_path = folder_path/date_file_name
    if date_file_path.exists() and date_file_path.is_file():
        exist_dict.update({date.strftime('%A %d %b'): True})
        daily_text = date_file_path.read_text(encoding='utf-8')
        weekly_text += f"""{date.strftime('%A %d %B, %Y')}: {daily_text}

        """
    else:
        exist_dict.update({date.strftime('%A %d %b'): False})

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

st.markdown("""<div style = 'font-size:24px; font-weight: 600; margin-top:32px; margin-bottom: 14px'>
                ✨ Create Weekly Summary
                </div>""", unsafe_allow_html = True)

if st.button('Weekly Summary', width = 'stretch'):
        with st.spinner('Generating weekly summary...'):
            result = generate_weekly_summary(weekly_text)
        if result['success']:
            st.session_state['weekly_summary'] = result['summary']
            st.session_state['ai_error'] = None
        else:
            st.session_state['ai_error'] = result['error']
            
if st.session_state['ai_error']:
    st.error(st.session_state['ai_error'])

if st.session_state['weekly_summary'] != '':
    st.markdown("""<div style = 'font-size:24px; font-weight:600; margin-top:32px; margin-bottom: 8px'>
                📔 Weekly Summary
                </div>""", unsafe_allow_html = True)
    st.text_area('Edit Weekly Summary', key = 'weekly_summary', height = 'content')
    if st.button('Save Weekly Summary', width = 'stretch'):
        weekly_summary_file_path.write_text(st.session_state['weekly_summary'], encoding='utf-8')
    if st.button('Export Weekly Summary', width = 'stretch'):
        with st.spinner('Exporting to Word...'):
            export_to_word(st.session_state['weekly_summary'], 
                           folder_path/f'{week_str} Weekly Summary.docx',
                           weekly_summary_template_path,
                           {'{{week_start}}':week_start.strftime('%A %d %B %Y.'),
                            '{{week_end}}':week_end.strftime('%A %d %B %Y.'),
                            '{{weekly_summary}}': st.session_state['weekly_summary']})  
        st.success('Word document exported successfully')