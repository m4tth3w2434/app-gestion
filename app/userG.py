from flask_login import UserMixin
from conexionDB import database_connection
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
    


def get_user_by_id(user_id):
    with database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            print(user)
            if user:
                return User(id=user[0], name=user[1], email=user[2], password=user[3], remember_me=user[4])
            return None

def get_user_by_email(email):
    with database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            if user:
                return User(id=user[0], name=user[1], email=user[2], password=user[3], remember_me=user[4])
            return None
