import os
import hashlib
import base64

class PasswordHasher:
    def salting(self):
        return base64.b64encode(os.urandom(24)).decode()

    def hash(self,passwordToHash):
        return hashlib.sha256(passwordToHash.encode('utf-8')).hexdigest()

    def validate_password(self,plain_password,salt_password,expected_password):
        return self.hash(salt_password+plain_password)==expected_password