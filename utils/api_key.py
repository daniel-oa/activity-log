import streamlit as st
from utils.app_mode import get_app_mode

API_KEY_STATE = 'gemini_api_key'  # plain key, not a widget key, so it survives page changes

def render_api_key_sidebar():
    with st.sidebar:
        st.subheader('AI Settings')
        with st.form('gemini_key_form'):
            entered = st.text_input('Gemini API Key', type='password', key='gemini_api_key_input',
                                    help='Optional. Required only for AI generation.')
            applied = st.form_submit_button('Apply API Key')
        if applied:
            st.session_state[API_KEY_STATE] = entered.strip()
        if st.session_state.get(API_KEY_STATE):
            st.caption('API key applied for this session.')
        st.caption("Don't have a key? [Get one from Google AI Studio](https://aistudio.google.com/apikey)")

def get_api_key():
    saved = st.session_state.get(API_KEY_STATE, '')
    if isinstance(saved, str) and saved.strip():
        return saved.strip()
    if get_app_mode() == 'local':
        try:
            local_key = st.secrets.get('GEMINI_API_KEY', '')
            if isinstance(local_key, str):
                return local_key.strip()
        except (FileNotFoundError, KeyError):
            pass
    return ''