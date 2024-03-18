from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask import Flask

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion'

mysql = pymysql.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'],
                        password=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'])

class User(UserMixin):
    #datos de la tabla users:id, name, email, password, remember_me, is_Admin los dos ultimos booleanos
    def __init__(self,id, name, email, password,remember_me, is_Admin):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.remember_me = remember_me
        self.is_Admin = is_Admin

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.email)
    

class database:
    def __init__(self):
        self.app = app
        self.mysql = mysql
    def get_user(self,email):
        with self.app.app_context():  # Envolvemos nuestro código en el contexto de la aplicación Flask
            # Abre una conexión a la base de datos
            cur = self.mysql.cursor()
            
            # Consulta SQL para buscar un usuario por su email
            cur.execute("SELECT * FROM users WHERE correo_electronico = %s", (email))
            user_data = cur.fetchone()  # Recupera el primer usuario encontrado
            
            cur.close()  # Cierra el cursor
            
            if user_data:
                user = user_data  # Crea un objeto Usuario con los datos recuperados
                return user
            else:
                return None

    def get_user_by_id(self,email):
        with self.app.app_context():  # Envolvemos nuestro código en el contexto de la aplicación Flask
            # Abre una conexión a la base de datos
            cur = self.mysql.cursor()
            
            # Como nuestra tabla tiene un id autoincremental, podemos buscar un la id del usuario con su email
            cur.execute("SELECT id FROM users WHERE email = %s", (email))
            user_data = cur.fetchone()  # Recupera el primer usuario encontrado
            
            cur.close()  # Cierra el cursor
            print(user_data)
            if user_data:
                user = user_data # Crea un objeto Usuario con los datos recuperados
                return user
            else:
                return None
    def create_user(self,name,email,password,remember_me,is_Admin):
        with self.app.app_context():
            cur = self.mysql.cursor()
            if remember_me == True:
                remember_me = 1
            else:
                remember_me = 0
            if is_Admin == True:
                is_Admin = 1
            else:
                is_Admin = 0
            cur.execute("INSERT INTO users (name,email,password,remember_me	,is_admin) VALUES (%s,%s,%s,%s,%s)",(name,email,password,remember_me,is_Admin))
            self.mysql.commit()
            cur.close()
            return True

# Función para obtener un usuario por su dirección de correo electrónico
users = []
def get_user(email):
    with app.app_context():  # Envolvemos nuestro código en el contexto de la aplicación Flask
        # Abre una conexión a la base de datos
        cur = mysql.cursor()
        
        # Consulta SQL para buscar un usuario por su email
        cur.execute("SELECT * FROM users WHERE correo_electronico = %s", (email))
        user_data = cur.fetchone()  # Recupera el primer usuario encontrado
        
        cur.close()  # Cierra el cursor
        
        if user_data:
            user = email  # Crea un objeto Usuario con los datos recuperados
            return user
        else:
            return None

# Ejemplo de uso



