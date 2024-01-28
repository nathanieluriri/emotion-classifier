import streamlit as st
from dbfunctions import  query_userName_from_UID
import os
def db_login_signup(proceed,user_name,password):
    import bcrypt
    from pymongo import MongoClient
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    from dotenv import load_dotenv
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    connect(MONGO_URI)

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
        if signup_process == uid:
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
        try:
            logged_in_Successful,uID =auth(user_name=user,password=passw)
        except:
            logged_in_Successful,uID = False,False
        if logged_in_Successful:
            print("logged in")
            return uID
            
        else:
            # print(logged_in_Successful,uID)
            return" Wrong password or username"
            # print(logged_in)


    def auth(user_name, password):
        users = User.objects.all()

        # print("HHHHHHHHHHHHHHHHHHHHHHHHHH", User.objects.raw({}))
        

        for u in users:
            # print("HHHHHHHHHHHHHHHHHHHHHHHHHH", users)
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
                    # print(user_name,"user name not found",u.user_name)

                    logged_in,user_id= False,False



        # return logged_in, user_id

        


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




if 'name' not in st.session_state:
    st.session_state.name = None

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'UID' not in st.session_state:
    st.session_state.UID = "Nothing has happened yet"
if 'UserName' not in st.session_state:
    st.session_state.UserName = "No Name yet"

if 'Login' not in st.session_state:
    st.session_state.Login = False
















login_form = st.empty()
if st.session_state.submitted == False:
    with login_form:
        with st.form("my_form"):
            st.write("To login enter your details")
            st.session_state.name = st.text_input("Enter your User Name",placeholder="Jenifer-channn")
            st.session_state.password = st.text_input("Enter your Password",placeholder="Enter your password",type='password')
            

            
            st.session_state.submitted = st.form_submit_button("Submit")
            if st.session_state.submitted:
                # print(st.session_state.name,st.session_state.password)


                st.session_state.UID=db_login_signup(2,st.session_state.name,st.session_state.password)
                if type(st.session_state.UID) == type("Mee") or type(st.session_state.UID) == None:
                    st.error(f"{st.session_state.UID} ",icon="😢") 
                    st.toast(f"{st.session_state.UID} ",icon="😢")

                    st.session_state.submitted = False
                else:
                    st.session_state.Login = True
                    try:
                        st.session_state.UserName = query_userName_from_UID(st.session_state.UID)['User Name']
                    except:
                        st.session_state.submitted = False


                    login_form.success(f"Succesfully Logged In: {st.session_state.UserName} ",icon="✅")
                    st.toast(f"Welcome back user '{st.session_state.UID}'  ",icon="✅")

else:
    # print("Hiiiiiiiiiiiiiiiiiiiiiiii",st.session_state.UID,st.session_state.name)
    st.session_state.UID=db_login_signup(2,st.session_state.name,st.session_state.password)
    # print("Hiiiiiiiiiiiiiiiiiiiiiiii",st.session_state.UID,st.session_state.name)
    st.session_state.Login = True
    st.session_state.UserName = query_userName_from_UID(st.session_state.UID)['User Name']
    st.toast(f" Welcome backk  {st.session_state.UserName}", icon='🔑')
    login_form.success(f"  Great to have you back {st.session_state.UserName}",icon="✅")

    


# if 'check' not in st.session_state:
#     st.session_state.check = 'Checked'

# if "CHecking" not in st.session_state:
#     print("checked")
#     st.session_state.CHecking = False

# if st.checkbox("check or uncheck",value=st.session_state.CHecking):
#     print('checking stage')
#     st.session_state.CHecking = True

#     st.write(st.session_state.CHecking)
#     st.session_state.check = 'Check'
    
# else:
#     st.session_state.CHecking = False
#     st.write(st.session_state.CHecking)
#     st.session_state.check ='Uncheck'



