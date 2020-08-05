#This module is temporary until creted database

mockuser=[{'email':'tutor@gmail.com', 'password':'tutor','role':'Teacher','phone':9876543210} , {'email':'student@gmail.com', 'password':'student','role':'Student','phone':'9876543211'}]

def get_user(email):
    user=[]
    for x in mockuser:
        if x.get('email')==email:
            user.append(x)
    if user:
        return user[0]
    else:
        return

def add_user(email,password,role,phone):
    mockuser.append({'email':email,'password':password,'role':role,'phone':phone})