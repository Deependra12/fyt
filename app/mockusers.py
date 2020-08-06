#This module is temporary until creted database

mockadmin=[{'username':'admin','salt':'UGg3TRzW+tNc5eVFHOwuthtEFWEINocR','password':'7030f34ee6c1f2d85e2db54df5a70d31152b890fc3215ea1587a2516d0b09d10'}]

def get_admin(username):
    admin=[]
    for x in mockadmin:
        if x.get('username')==username:
            admin.append(x)
    if admin:
        return admin[0]
    else:
        return


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