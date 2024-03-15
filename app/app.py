from flask import Flask, render_template, request, redirect, url_for, url_parse
from forms import SignupForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from userG import users, get_user

import pymysql

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion'

mysql = pymysql.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'],
                        password=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mondongo'

login_manager = LoginManager()
login_manager.login_view = 'login'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        user = (name, email, password)
        users.append(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # si el usuario ya ha hecho login redirigimos a index
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # inicializamos el formulario
    form = LoginForm()
    # si el usuario hace submit:
    if form.validate_on_submit():
        # comprobamos que el email está en la base de datos:
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
        # si el usuario existe y la contraseña es correcta llamamos
        # la función que loguea al usuario y vemos si ha clicado en "recordarme"
            login_user(user, remember= form.remember_me.data)
            # hacemos un next_page para enviar a un sitio u otro
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                # si se cumple que todo está correcto redireccionamos a
                next_page = url_for('index')
            else:
                # si no ha ido bien, volvemos a mostrar el login
                next_page = url_for('login')

            return redirect(next_page)
            
app.run(debug=True)

