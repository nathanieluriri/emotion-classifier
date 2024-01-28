




def db_login_signup(proceed,user_name,password):
    import bcrypt
    from pymongo import MongoClient
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    import os
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
        signup_process, uid = auth(user, passw)
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




def query_userName_from_UID(UID):
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    filter = {'_id':UID}
    db = client.auth_tutorial
    collection = db.user
    query_output = collection.find_one(filter)
    return query_output
