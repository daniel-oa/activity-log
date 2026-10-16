import streamlit as st
from utils.supabase_client import get_supabase_client

def render_authentication():
    if 'supabase' not in st.session_state:
        st.session_state['supabase'] = get_supabase_client()

    supabase = st.session_state['supabase']

    if 'user' in st.session_state:
        with st.sidebar:
            st.write(f"Signed in as {st.session_state['user'].email}")

        if st.button('Log out'):
            supabase.auth.sign_out()
            del st.session_state['user']
            st.rerun()

        return True

    st.title('Activity Log')
    st.subheader('Sign in or create an account')

    sign_in_tab, sign_up_tab = st.tabs(['Log in', 'Create account'])
    with sign_in_tab:
        with st.form('login_form'):
            email = st.text_input('Email address', key = 'login_email')
            password = st.text_input('Password', type = 'password', key = 'login_password')
            login_submitted = st.form_submit_button('Log in')

            if login_submitted:
                try:
                    response = supabase.auth.sign_in_with_password({'email': email,
                                                                    'password': password,
                                                                    'options': {'email_redirect_to': 'https://activity-log.streamlit.app'}})
                    if response.user:
                        st.session_state['user'] = response.user
                        st.rerun()
                except Exception:
                    st.error('Login failed. check your email and password')

    with sign_up_tab:
        with st.form('signup_form'):
            email = st.text_input('Email address', key = 'signup_email')
            password = st.text_input('Password', type = 'password', key = 'signup_password')
            confirm_password = st.text_input('Confirm Password', type = 'password', key = 'confirm_password')
            signup_submitted = st.form_submit_button('Create account')

            if signup_submitted:
                if not email or not password:
                    st.warning('Enter your email address and password.')
                elif password != confirm_password:
                    st.warning('Your passwords do not match.')
                elif len(password) < 8:
                    st.warning('Use a password with at least 8 characters')
                else:
                    try:
                        response = supabase.auth.sign_up({'email': email,
                                                            'password': password,})
                        if response.session and response.user:
                            st.session_state['user'] = response.user
                            st.rerun()
                        else:
                            st.success('Account created. Check your email to confirm your account, then log in.')
                    except Exception:
                        st.error('Account creation failed. Check your details')
    return False