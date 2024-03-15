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
    
    def __repr__(self):
        return '<User {}>'.format(self.email)

# Función para obtener un usuario por su dirección de correo electrónico
def get_user(email):
    with app.app_context():  # Envolvemos nuestro código en el contexto de la aplicación Flask
        # Abre una conexión a la base de datos
        cur = mysql.connection.cursor()
        
        # Consulta SQL para buscar un usuario por su email
        cur.execute("SELECT * FROM usuarios WHERE correo_electronico = %s", (email,))
        user_data = cur.fetchone()  # Recupera el primer usuario encontrado
        
        cur.close()  # Cierra el cursor
        
        if user_data:
            user = User(email=user_data[0])  # Crea un objeto Usuario con los datos recuperados
            return user
        else:
            return None

# Ejemplo de uso
email_a_buscar = 'correo@example.com'
usuario_encontrado = get_user(email_a_buscar)
if usuario_encontrado:
    print("El usuario existe en la base de datos.")
else:
    print("El usuario no fue encontrado en la base de datos.")
