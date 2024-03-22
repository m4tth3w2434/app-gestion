import pymysql
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from userG import User

class UserDatabase:
    def __init__(self,app):
        self.host = app.config['MYSQL_HOST']
        self.user = app.config['MYSQL_USER']
        self.password = app.config['MYSQL_PASSWORD']
        self.db = app.config['MYSQL_DB']
        
    def connect(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db
        )

    def existing_user(self, email):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                user = cursor.fetchone()
                connection.commit()
                if user:
                    return True
                return False

    def create_user(self, name, email, password, remember_me, admin):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                password = generate_password_hash(password)
                cursor.execute('INSERT INTO users (name, email, password, remember_me, is_admin) VALUES (%s, %s, %s, %s, %s)', (name, email, password, remember_me, admin))
                connection.commit()
                new_user_id = cursor.lastrowid
                return

    def get_user_by_id(self, user_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
                user = cursor.fetchone()
                if user:
                    userC=User(id=user[0], name=user[1], email=user[2], password=user[3], is_admin=user[4], remember_me=user[5])
                    return userC
                return None
    def get_user_by_email(self, email):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                user = cursor.fetchone()
                if user:
                    return User(id=user[0], name=user[1], email=user[2], password=user[3], is_admin=user[4], remember_me=user[5])
                return None
    def get_all_users(self):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users')
                users = cursor.fetchall()
                return users
    def update_user(self,user_id,name, email, password, phone, street, birthdate):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                def comprobar():
                    cursor.execute('SELECT * FROM detailsUsers WHERE user_id = %s', (user_id,))
                    user = cursor.fetchone()
                    print("ads",user)

                    if user:
                        return True
                    return False
                if comprobar():
                    password = generate_password_hash(password)
                    cursor.execute('UPDATE users SET name=%s,email=%s,password=%s WHERE id=%s', (name, email, password, user_id))
                    cursor.execute('UPDATE detailsUsers SET phone=%s,street=%s,birthday=%s WHERE user_id=%s', (phone, street, birthdate, user_id))
                else:
                    cursor.execute('INSERT INTO detailsUsers (user_id,phone,street,birthday) VALUES (%s, %s, %s, %s)', (user_id, phone, street, birthdate))
                    connection.commit()
                connection.commit()
                return

            