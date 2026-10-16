import streamlit as st

def load_record(record_date, record_type):
    user_id = st.session_state['user'].id
    supabase = st.session_state['supabase']

    response = supabase.table('records').select('content').eq('user_id', user_id).eq(
        'record_date', record_date).eq('record_type', record_type).execute()

    if response.data:
        return response.data[0]['content']
    return ''

def save_record(record_date, record_type, content):
    user_id = st.session_state['user'].id
    supabase = st.session_state['supabase']

    supabase.table('records').upsert({'user_id': user_id, 'record_date': record_date,
                                      'record_type': record_type, 'content': content,},
                                      on_conflict = 'user_id, record_date, record_type',).execute()