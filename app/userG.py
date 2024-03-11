from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, name, email, password, is_Admin):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_Admin = is_Admin

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)