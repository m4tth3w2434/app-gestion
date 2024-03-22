from flask import Flask, render_template, request, redirect, url_for,session
from forms import SignupForm, LoginForm,editForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from conexionDB import UserDatabase
import datetime

app = Flask(__name__)
# Configuración de la aplicación
app.config['SECRET_KEY'] = 'mondongo'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion'
# Crear una instancia de la base de datos
dbu = UserDatabase( app )
login_manager = LoginManager( app )
login_manager.login_view = 'login'
# Función para cargar un usuario
@login_manager.user_loader
def load_user(user_id):
    return dbu.get_user_by_id(user_id)
# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')
# Ruta de registro
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Crear una instancia del formulario
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        admin = False
        # Verificar si el usuario ya existe
        if dbu.existing_user(email):
            return redirect(url_for('signup'))
        # Verificar si el usuario es administrador o no y modificar el valor para la base de datos
        if admin == True:
            admin = 1
        else:
            admin = 0
        if remember_me == True:
            remember_me = 1
        else:
            remember_me = 0
        # Crear un nuevo usuario
        dbu.create_user(name, email, password, remember_me, admin)
        login_user(user=dbu.get_user_by_email(email), remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('sign_up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Crear una instancia del formulario
    form = LoginForm()
    if form.validate_on_submit():
        # Intentar iniciar sesión
        try:
            email = form.email.data
            password = form.password.data
            remember_me = form.remember_me.data
            #modificar el valor para la base de datos
            if remember_me == True:
                remember_me = 1
            else:
                remember_me = 0
            user = dbu.get_user_by_email(email)
            # Verificar si el usuario existe y si la contraseña es correcta
            if user and user.check_password(password):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))
        except:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/panelAdministrdor')
@login_required
def dashboard():
    # Verificar si el usuario es administrador
    if current_user.admin == 1:
        userstuple = dbu.get_all_users()
        users = []
        # Iterar sobre los usuarios y modificar el valor numérico del rol
        for user in userstuple:
            # Convertir el valor numérico en una cadena de texto para mostrar en la tabla
            role = "Administrador" if user[4] == 1 else "Empleado"
            # Crear una nueva tupla con el valor de rol modificado
            modified_user = (*user[:4], role, *user[5:])
            users.append(modified_user)
        return render_template('dashboard.html', users=users)
    else:
        return redirect(url_for('index'))

@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    # Obtener el usuario por su ID
    user = dbu.get_user_by_id(user_id)
    print(user)
    return render_template('profile.html', user=user)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
# Función para editar un usuario
def edit(user_id):
    # Obtener el usuario por su ID
    user = dbu.get_user_by_id(user_id)
    form = editForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        street = form.address.data
        birthdate = form.birthdate.data
        dbu.update_user(user_id, name, email, phone, street, birthdate)
        user.update_user(name, email, phone, street, birthdate)
        return redirect(url_for('index',))
    form.name.data = user.name
    form.email.data = user.email
    form.phone.data = user.phone
    form.address.data = user.street
    form.birthdate.data = user.birthdate
    return render_template('edit_proifle.html', form=form,user=user)
@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_profile(user_id):
    dbu.delete_user(user_id)
    if current_user.id == user_id:
        logout_user()
        return redirect(url_for('index'))
    return redirect(url_for('index'))
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
