from . import db

# models go here

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), index = True, unique = True)
    hash_password = db.Column(db.String(120))

    def __repr__(self):
        return '<Email {}>'.format(self.email)

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password , password)   
