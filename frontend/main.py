import streamlit as st
from login import Login_registration_page
from profile import profile_page

if 'user' not in st.session_state:
    st.session_state['user'] = None

st.title("HRM Frontend")
st.write("Welcome to the HRM Frontend Application.")

if st.session_state['user'] is None:
    Login_registration_page()
else:
    profile_page()