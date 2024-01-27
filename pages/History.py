import streamlit as st
from pages import *


try:
    if st.session_state.Login == False:
        st.info("Login Or Sign Up To View History",icon='🚨')
        if st.button("Login", key='2'):
            st.switch_page("pages/login_page.py")
        if st.button("Sign Up",key='1'):
            st.switch_page("pages/sign_up_page.py")
except AttributeError:
    st.info("Login Or Sign Up To View History",icon='🚨')
    if st.button("Login"):      
        st.switch_page("pages/login_page.py")
    if st.button("Sign Up"):
        st.switch_page("pages/sign_up_page.py")
    


# if st.session_state.Login == False:
#     st.info("Login Or Sign Up To View History")
#     if st.button("Login"):
        
#         st.switch_page("pages/login_page.py")
#     if st.button("Sign Up"):
#         st.toast(icon="☑️",body="SignUp Page")
#         st.switch_page("pages/sign_up_page.py")