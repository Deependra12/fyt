class User:
    def __init__(self,login_id):
        self.login_id=login_id

    def get_id(self):
        return  self.login_id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
