import streamlit as st
import time
import pickle
from pathlib import Path
from dotenv import load_dotenv
import requests
import time as t 
API_URL = ["https://api-inference.huggingface.co/models/shivanshu292001/Emotions","https://api-inference.huggingface.co/models/harshit345/xlsr-wav2vec-speech-emotion-recognition","https://api-inference.huggingface.co/models/audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim"] # turn into a list in prediction setting you should be able to select the model you want to use to do a prediction
headers = {"Authorization": "Bearer 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"}

st.set_page_config("emotion sound Project",page_icon=":sound:")

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "multiple_uploaded_files" not in st.session_state:
    st.session_state.multiple_uploaded_files = None

if "prediction_option" not in st.session_state:
    st.session_state.prediction_option = False
if "model_option" not in st.session_state:
    st.session_state.model_option = 0
if "prediction_option" not in st.session_state:
    st.session_state.prediction_option = False


# write a function to handle files if user wants to select multiple files 



def query(file, counter=0):
   
    data = file
    response = requests.post(API_URL[st.session_state.model_option-1], headers=headers, data=data)
    print("using :",API_URL[st.session_state.model_option-1])
    print(response)
    if response.status_code == 503:
        t.sleep(5)
        print("trying again...") 
        counter += 1        
        if counter == 5:
            st.write("Server to busy try again in 20 mins")
            return False
        return query(file, counter)
    elif response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        return ("# Invalid format given")
    



def Multiquery(files, counter=0, res={}, start_index=0):
    for i in range(start_index, len(files)):
        data = files[i]
        
        t.sleep(2.5)
        
        response = requests.post(API_URL, headers=headers, data=data)
        st.spinner("analyzing data...")
        t.sleep(2.5)
        res.update({data.name: response.json()})
        t.sleep(2.5)
        print(response)
        
        if response.status_code == 503:
            t.sleep(5)
            print("trying again...")
            counter += 1
            if counter == 5:
                st.write("Server is too busy, try again in 20 mins")
                return False
            return Multiquery(files, counter, res, start_index=i)
        elif response.status_code == 200:
            st.success(f"{data.name} Successfully Analysed")
        elif response.status_code == 400:
            return "# Invalid format given"

    return res

def reverse_list(input_list):
    """
    Reverse the order of elements in a list.

    Parameters:
    - input_list (list): The list to be reversed.

    Returns:
    - list: The reversed list.
    """
    return input_list[::-1]

def reverse_dict(input_dict):
    """
    Reverse the keys and values of a dictionary.

    Parameters:
    - input_dict (dict): The dictionary to be reversed.

    Returns:
    - dict: The reversed dictionary.
    """
    reversed_dict = {v: k for k, v in input_dict.items()}
    return reversed_dict









def refined_output(output):
    st.write(f"## :orange[For File ] : {st.session_state.uploaded_file.name}")
    for output_dictionary in output:
       print(output_dictionary)
       st.code(f"{output_dictionary['label']} : {output_dictionary['score'] * 100} %")
    
    
    












    


with st.sidebar:
    st.session_state.uploaded_file =st.file_uploader("Upload only one audio file to be analyzed",type=["wav","mp3","AAC","flaac"])
    st.session_state.multiple_uploaded_files = st.file_uploader("Upload multiple audio files for analysis ",type=["wav","mp3","AAC","flaac"],accept_multiple_files=True)
   



    
main_container = st.empty()
with main_container:
    with st.container():
       analysis,prediction_settings= st.tabs(["Analysis","Prediction settings"])
       with analysis: # Add option to visualize the data 
           st.header("Analysis")
           if st.session_state.uploaded_file != None:
               output = query(st.session_state.uploaded_file)
               
               refined_output(output) # replace with a function to display a refined output using the prediction rules 
           analysis = st.empty()
           analysis.write("based on the audio file provided and the prediction settings the results of the analysis say there is 20% ")
            # An option to just visualize the data


       with prediction_settings:
           st.header("Prediction settings")
           # slider to reduce adjust emotions being shown in the anlysis section
           col1, col2 = st.columns(2)
           with st.container(border=True):

            with col1:
                st.checkbox(" Select me if you just want to see Positive and Negative emotions only", key="disabled")
            with col2:
                st.session_state.prediction_option = st.selectbox(        "How Many emotions would you like to see",        (1, 2, 3,4,5),        disabled=st.session_state.disabled )
           st.write("### There are three different models which one would you like to use")
           st.session_state.model_option = st.selectbox(        "Select between 1-3",        (1, 2, 3) ,key="model_selection",        disabled=st.session_state.disabled )
       
            
          
          
           











