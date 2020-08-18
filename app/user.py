class User:
    def __init__(self,login_id,role):
        self.login_id=login_id
        self.role=role

    def get_id(self):
        return  self.login_id

    def get_role(self):
        print(self.role)
        return self.role

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

