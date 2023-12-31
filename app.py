import streamlit as st
import time
import pickle
from pathlib import Path
from dotenv import load_dotenv
from transformers import pipeline

pipe = pipeline("sentiment-analysis")


def display_toast():
    if st.session_state.uploaded_file !=None:
        st.toast("Audio successfully loaded in")
        print("if",st.session_state.uploaded_file)
        

    else:
        st.toast("Upload audio to analyze emotion")
        print("else",st.session_state.uploaded_file)

    
st.set_page_config("emotion sound Project",page_icon=":books:",)
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
with st.sidebar:
    st.session_state.uploaded_file =st.file_uploader("Upload audio data to be analyzed",type=["wav","mp3","AAC"],on_change=display_toast())
    
main_container = st.empty()
with main_container:
    with st.container():
       stupid,dog= st.tabs(["Analysis","Prediction settings"])
       with stupid:
           st.header("Analysis")
           st.write(pipe("Are you Mad?"))
           analysis = st.empty()
           analysis.write("based on the audio file provided and the prediction settings the results of the analysis say there is 20% ")


       with dog:
           st.header("Prediction settings")










