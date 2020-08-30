from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

class Admin(UserMixin):
    def __init__(self, id):
        self.id = 1
        self.role = 'admin' 
        self.email = 'admin@admin.com'
        self.password = 'admin'
        self.username = 'admin'
    
    def check_password(self, password):
        # return check_password_hash(self.password, password)
        return self.password == password

admin = Admin(1)

@login_manager.user_loader
def load_user(id):
    return admin