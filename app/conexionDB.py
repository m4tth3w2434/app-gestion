import pymysql
from flask import Flask,current_app
from werkzeug.security import generate_password_hash, check_password_hash

def database_connection():
    return pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        db=current_app.config['MYSQL_DB']
    )

def existing_user(email):
    with database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            connection.commit()
            if user:
                return True
            return False
    
def create_user(name, email, password, remember_me, admin):
    with database_connection() as connection:
        with connection.cursor() as cursor:
            password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (name, email, password, remember_me, is_admin) VALUES (%s, %s, %s, %s, %s)', (name, email, password, remember_me, admin))
            connection.commit()
            new_user_id = cursor.lastrowid
            print('Usuario creado con id:', new_user_id)
            return