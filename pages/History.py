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
    db = client.auth_tutorial
    collection = db.history
    query_output = collection.find(filter)
    query_output_ls=[]
    print(query_output)
    for query in query_output:
        
        query_output_ls.append(query)


    return query_output_ls








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
    print(st.session_state.UID)
    st.session_state.user_history = query_history()
    st.write("# Users history",st.session_state.user_history)
