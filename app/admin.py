from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

class Admin:
    def __init__(self, id):
        self.id = id
        self.role = 'admin' 
        self.email = 'admin@admin.com'
        self.password = 'admin'
    
    def check_password(self, password):
        # return check_password_hash(self.password, password)
        return self.password == password

admin = Admin(1)