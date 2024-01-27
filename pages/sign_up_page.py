import streamlit as st
from pages import *
from dbfunctions import  query_userName_from_UID

if 'UID' not in st.session_state:
    st.session_state.UID = "Nothing has happened yet"

def db_login_signup(proceed,user_name,password):
    import bcrypt
    from pymongo import MongoClient
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId

    connect("mongodb://localhost:27017/auth_tutorial")

    class User(MongoModel):
        user_name = fields.CharField(mongo_name="User Name")
        password = fields.CharField(mongo_name="Password")
        # likes = fields.ListField(mongo_name="Likes")

    class Actions(MongoModel):
        UserID = fields.ReferenceField(User, mongo_name='User Details')
        ActionType = fields.CharField(mongo_name="Action Taken")




    def signup(user,passw):
        try:
            signup_process, uid = auth(user, passw)
        except:
            signup_process , uid = False,False
        if signup_process == uid or type(signup_process) == type("sasa")or type(uid) == type("sasa"):
            passw_2_hash= passw.encode('utf-8')
            hashed_passw =  bcrypt.hashpw(passw_2_hash,bcrypt.gensalt())
            new_user = User(user_name=user,password=hashed_passw)
            new_user.save()
            print('signup successfull')
        else:
            new_user = "User Has Signed Up ALready"
        return new_user
        


    def login(user,passw):
        passw = passw.encode('utf-8')
        #function that takes login details and returns true of false
        logged_in_Successful,uID =auth(user_name=user,password=passw)
        if logged_in_Successful:
            print("logged in")
            return uID
            
        else:
            return" Wrong password or username"
            # print(logged_in)


    def auth(user_name, password):
        users = User.objects.all()
        for u in users:
            if user_name == u.user_name:
                checkP = u.password
                checkP = checkP[2:-1]
                checkP= bytes(checkP,'utf-8')
                # print(type(checkP))            
                logged_in = bcrypt.checkpw(password,checkP)
                if logged_in:
                    user_id = u._id
                    return logged_in, user_id
                    
            elif user_name != u.user_name:
                # print("user name not found")
                logged_in,user_id= None,None
            return logged_in, user_id

        


    def start(process,user_name,password):
        if process == 1:
            #Sign up process starts here
            UserObject = signup(user_name,password)
            return UserObject
            
            
        elif process == 2:
            #login process starts here
            UserObject=login(user_name,password)

            return UserObject
        
        else:
            print("error")
            return 'Erroorrrrr IN processsss'
        
    return start(proceed,user_name,password)






try:
    if st.session_state.Login== False:
        with st.form("my_form",key="Trial"):
            st.write("To login enter your details")
            user_name = st.text_input("Enter your User Name",placeholder="Nattyboi")
            password = st.text_input("Enter your Password",placeholder="Enter your password",type='password')
            

        # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.session_state.UID=db_login_signup(1,st.session_state.name,st.session_state.password)
                st.success(st.session_state.UID)

                # st.toast(icon="☑️",body="Successfully Signed up ")

    elif st.session_state.Login == True:
        st.session_state.UserName = query_userName_from_UID(st.session_state.UID)['User Name']
        st.toast(f" Already Logged In as : {st.session_state.UserName}", icon='🔥')
        st.info(f"  Already Logged In as: {st.session_state.UserName}",icon="☑️")

except:
    
    with st.form("my_form"):
        st.write("To Sign Up enter your details")
        user_name = st.text_input("Create a User Name",placeholder="Jenifer-channn")
        password = st.text_input("Create a Password",placeholder="Enter your password",type='password')
        

    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.UID=db_login_signup(1,user_name,password)
            st.success(f"Welcome aboard 😁 {st.session_state.UID.user_name} ",icon="☑️")
            st.toast(body=f"PLease go and log In {st.session_state.UID.user_name} 😊")






# st.session_state.UID=db_login_signup(2,st.session_state.name,st.session_state.password)
# if type(st.session_state.UID) == type("Mee"):
#     st.error(f"{st.session_state.UID} ",icon="😢") 
#     st.toast(f"{st.session_state.UID} ",icon="😢")

#     st.session_state.submitted = False
# else:
#     st.session_state.Login = True
#     st.session_state.UserName = query_userName_from_UID(st.session_state.UID)['User Name']

#     st.success(f"Succesfully Logged In: {st.session_state.UserName} ",icon="✅")
#     st.toast("successfully submitted ",icon="✅")



