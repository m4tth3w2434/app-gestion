from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin):
    def __init__(self, id, name, email, password, remember_me,is_admin):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.admin = is_admin
        self.remember_me = remember_me
        self.phone = "No registrado"
        self.street = "No registrado"
        self.birthdate = '1990-05-15'
    def update_user(self, name, email, password, phone, street, birthdate):
        self.name = name
        self.email = email
        self.set_password(password)
        self.phone = phone
        self.street = street
        self.birthdate = birthdate
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return f'<User: {self.email}>'
