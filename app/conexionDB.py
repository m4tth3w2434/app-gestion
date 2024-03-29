import pymysql
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from userG import User
import datetime
# Clase para la conexión a la base de datos
class UserDatabase:
    def __init__(self,app):
        self.host = app.config['MYSQL_HOST']
        self.user = app.config['MYSQL_USER']
        self.password = app.config['MYSQL_PASSWORD']
        self.db = app.config['MYSQL_DB']
    # Función para conectar a la base de datos
    def connect(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db
        )
# Funciones para la base de datos
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
        # Crear un nuevo usuario conectando a la base de datos y ejecutando una consulta
        with self.connect() as connection:
            with connection.cursor() as cursor:
                password = generate_password_hash(password)
                cursor.execute('INSERT INTO users (name, email, password, remember_me, is_admin) VALUES (%s, %s, %s, %s, %s)', (name, email, password, remember_me, admin))
                connection.commit()
                new_user_id = cursor.lastrowid
                return

    def get_user_by_id(self, user_id):
        # Obtener un usuario por su ID por consulta a la base de datos  
        with self.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
                user = cursor.fetchone()
                cursor.execute('SELECT * FROM detailsUsers WHERE user_id = %s', (user_id,))
                userD = cursor.fetchone()
                if user:
                    if userD != None:
                        # Crear una instancia de la clase User con los datos obtenidos
                        userC=User(id=user[0], name=user[1], email=user[2], password=user[3], is_admin=user[4], remember_me=user[5], phone=userD[1], street=userD[2], birthdate=userD[3])
                    else:
                        # Si no se tiene registro detallados del usuario, se asignan valores por defecto
                        userD = (user[0], "No registrado", "No registrado", datetime.datetime.now())
                    userC=User(id=user[0], name=user[1], email=user[2], password=user[3], is_admin=user[4], remember_me=user[5], phone=userD[1], street=userD[2], birthdate=userD[3])
                    return userC
                return None
    def get_user_by_email(self, email):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                # Obtener un usuario por su email por consulta a la base de datos   
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                user = cursor.fetchone()

                cursor.execute('SELECT * FROM detailsUsers WHERE user_id = %s', (user[0],))
                userD = cursor.fetchone()
                print(userD)
                if userD != None:
                    # Crear una instancia de la clase User con los datos obtenidos
                    return User(id=user[0], name=user[1], email=user[2], password=user[3], is_admin=user[4], remember_me=user[5], phone=userD[1], street=userD[2], birthdate=userD[3])
                else:
                    if user:
                        # Si no se tiene registro detallados del usuario, se asignan valores por defecto
                        userD = (user[0], "No registrado", "No registrado", datetime.datetime.now())
                        return User(id=user[0], name=user[1], email=user[2], password=user[3], is_admin=user[4], remember_me=user[5], phone=userD[1], street=userD[2], birthdate=userD[3])
                return None
    def get_all_users(self):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                # Obtener todos los usuarios por consulta a la base de datos
                cursor.execute('SELECT * FROM users')
                users = cursor.fetchall()
                return users
    def update_user(self,user_id,name, email, phone, street, birthdate):
        with self.connect() as connection:
            with connection.cursor() as cursor:
                def comprobar():
                    # Verificar si el usuario tiene detalles en la tabla detailsUsers
                    cursor.execute('SELECT * FROM detailsUsers WHERE user_id = %s', (user_id,))
                    user = cursor.fetchone()
                    print("ads",user)
                    connection.commit()
                    if user:
                        return True
                    return False
                if comprobar():
                    # Actualizar los datos del usuario en la tabla users y detailsUsers SI existe
                    cursor.execute('UPDATE users SET name=%s,email=%s WHERE id=%s', (name, email, user_id))
                    cursor.execute('UPDATE detailsUsers SET phone=%s,street=%s,birthday=%s WHERE user_id=%s', (phone, street, birthdate, user_id))
                else:
                    # Crear un registro en la tabla detailsUsers SI no existe
                    cursor.execute('INSERT INTO detailsUsers (user_id,phone,street,birthday) VALUES (%s, %s, %s, %s)', (user_id, phone, street, birthdate))
                    connection.commit()
                connection.commit()
                return

    def delete_user(self, user_id):
        with self.connect() as connection:
            with connection.cursor() as cursor:# Eliminar un usuario por su ID por consulta a la base de datos
                cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
                connection.commit()
                return