import streamlit as st
from utils.app_mode import get_app_mode

def get_api_key():
    entered_key = st.session_state.get('gemini_api_key_input', '')
    if isinstance(entered_key, str) and entered_key.strip():
        return entered_key.strip()
    if get_app_mode() == 'local':
        try:
            local_key = st.secrets.get('GEMINI_API_KEY', '')
            if isinstance(local_key, str):
                return local_key.strip()
        except (FileNotFoundError, KeyError):
            pass
    return ''