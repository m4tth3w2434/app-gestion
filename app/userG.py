from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin):
    def __init__(self, id, name, email, password, remember_me,is_admin, phone, street, birthdate):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.admin = is_admin
        self.remember_me = remember_me
        self.phone = phone
        self.street = street
        self.birthdate = birthdate
    def update_user(self, name, email, phone, street, birthdate):
        self.name = name
        self.email = email
        self.phone = phone
        self.street = street
        self.birthdate = birthdate
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User: {self.email}>'
