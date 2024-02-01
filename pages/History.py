import streamlit as st
from pages import *
from datetime import datetime
import os
from pymodm import MongoModel,connect,fields
from dotenv import load_dotenv
MONGO_URI = os.getenv('MONGO_URI')
load_dotenv()
if "user_history" not in st.session_state:
    st.session_state.user_history= []

if "history_results" not in st.session_state:
    st.session_state.history_results= []

if "selected_analysis" not in st.session_state:
    st.session_state.selected_analysis ="Nothing selected yet"
if "radio_options" not in st.session_state:
    st.session_state.radio_options =[]

if "radio_option" not in st.session_state:
    st.session_state.radio_option=[]

if "return_point" not in st.session_state:
    st.session_state.return_point = 0

if "disabled" not in st.session_state:
    st.session_state.disabled = True


def refined_output(output,stuff):
    if type(output) == str:
        st.warning(output)
        st.write("Something failed")
    
    st.write(f"## :orange[For File ] : {stuff}")
    for output_dictionary in output:
    #    print(output_dictionary)
       st.code(f"{output_dictionary['label']} : {output_dictionary['score'] * 100} %")
    # return output


class User(MongoModel):
    user_name = fields.CharField(mongo_name="User Name")
    password = fields.CharField(mongo_name="Password")

class History(MongoModel):
    connect(mongodb_uri=MONGO_URI)
    from datetime import datetime
    UserDetails = fields.ReferenceField(User,mongo_name="User Details")
    History_Title = fields.CharField(mongo_name="History Name")
    Date = fields.TimestampField(mongo_name="Date",default=datetime.now)    
    Description = fields.ListField(mongo_name="Description")
    
def query_history():
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI)
    filter = {"User Details":ObjectId(st.session_state.UID)}
    db = client.Emotion_RecognitionDB
    collection = db.history
    query_output = collection.find(filter)
    query_output_ls=[]
    # print(query_output)
    for query in query_output:
        
        query_output_ls.append(query)


    return query_output_ls


def convert_to_date(Timestamp_in_seconds):
    Timestamp_in_seconds = Timestamp_in_seconds.time
    date_and_time = datetime.utcfromtimestamp(Timestamp_in_seconds)
    return date_and_time

def readeable_history(User_history_list):
    radio_options = list()
    selected_analysis = list()
    for n in range(len(User_history_list)):
        radio_options.append(f":orange[{  User_history_list[n]['History Name']  }] `{convert_to_date(User_history_list[n]['Date'])}` ")
        selected_analysis.append(((User_history_list[n],radio_options[n],)))
    return radio_options,selected_analysis
        





try:
    if st.session_state.Login == False:
        st.info("Login Or Sign Up To View History",icon='🚨')
        if st.button("Login", key='2'):
            st.switch_page("pages/login_page.py")
        if st.button("Sign Up",key='1'):
            st.switch_page("pages/sign_up_page.py")
    


except AttributeError:
    st.switch_page('pages/login_page.py')  
    



if st.session_state.Login:
    # print(st.session_state.UID)
    st.session_state.user_history = query_history()
    
    analysis,previous_history = st.tabs(["Analysis","Load Previous History"])

    with  analysis:
        try:
            st.button("Return to point you set", on_click=refined_output(st.session_state.selected_analysis[st.session_state.return_point][0]['Description'],st.session_state.selected_analysis[st.session_state.return_point][0]['History Name']) )
        except IndexError:
            st.write(f"# No History Yet! {st.session_state.selected_analysis}")
            st.button("Check Again")
            
        except TypeError:
            st.write("# History Loading...")

        


    with previous_history:
        st.session_state.radio_options,st.session_state.selected_analysis = readeable_history(st.session_state.user_history)
        st.session_state.radio_option =st.radio("SELECT A POINT To Return to",st.session_state.radio_options)
        if st.session_state.radio_option ==None:
            st.session_state.disabled= True
        else:
            st.session_state.disabled = False
        if st.button("Set return point",disabled=st.session_state.disabled):
            for i in range(len(st.session_state.selected_analysis)):
                if st.session_state.radio_option==st.session_state.selected_analysis[i][1]:
                    st.session_state.return_point = i
                    st.success("Return Point successfully set")
        
        # st.write(checktupleinlist(st.session_state.radio_option,st.session_state.selected_analysis))
        
         # create a dictionary of string that takes timestamp and converts it to human redeable time and takes file name it should be mapped to the st.session_state.user_history 








