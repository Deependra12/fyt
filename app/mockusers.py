#This module is temporary until creted database

mockuser=[{'username':'mockTutor',
            'email':'tutor@gmail.com',
            'role':'teacher',
           'phone':9876543210,
           'salt':'kB45AIaawDtNZihQCAt2HipUuV0DA6zi',
           'password':'3af6cdca0d433d7aa1189b71bca6059a15f810d9de04c50d1f798cb049deba49'} ,
          {'username':'mockStudent',
           'email':'student@gmail.com',
           'role':'student',
           'phone':'9876543211',
            'salt':'pzIpQLePSW7R7pjnc92t50hA93Xakp2S',
            'password': 'afc74ab1772ddb5b5830400cb7ca89ae49d4ac4d21a5356025ce7c89a74df412'}]

def get_user(email):
    user=[]
    for x in mockuser:
        if x.get('email')==email:
            user.append(x)
    if user:
        return user[0]
    else:
        return

def add_user(username,email,role,phone,salt,password):
    mockuser.append({'username':username,'email':email,'role':role,'phone':phone,'salt':salt,'password':password})