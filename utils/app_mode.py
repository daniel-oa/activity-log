import streamlit as st

def get_app_mode():
    try:
        return st.secrets.get('APP_MODE', 'local').strip().lower()
    except FileNotFoundError:
        mode = 'local'
    return mode.strip().lower()