from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

class Admin:
    def __init__(self, id):
        self.id = id
        self.role = 'admin' 
        self.email = 'admin@admin.com'
        self.password = 'admin'
        self.username = 'admin'
    
    def check_password(self, password):
        # return check_password_hash(self.password, password)
        return self.password == password

    def is_active(self):
        return True

    def get_id(self):
        return  self.id

    def is_authenticated(self):
        return True

admin = Admin(1)
