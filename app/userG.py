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
    
    def __repr__(self):
        return '<User {}>'.format(self.email)
    
users = []
# Función para obtener un usuario por su dirección de correo electrónico
def get_user(email):
    # Itera sobre cada usuario en la lista
    for user in users:
        # Verifica si la dirección de correo electrónico coincide
        if user.email == email:
            # Devuelve el usuario si se encuentra una coincidencia
            return user
    # Devuelve None si no se encuentra ningún usuario con el correo electrónico proporcionado
    return None 