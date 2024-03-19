from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin):
    def __init__(self, id, name, email, password, remember_me):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.admin = False
        self.remember_me = remember_me

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return f'<User: {self.email}>'
