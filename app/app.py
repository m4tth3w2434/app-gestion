from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'gestion'

mysql = MySQL(app)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mondongo'

login = LoginManager(app)
login.login_view = 'login'

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

        

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

app.run(debug=True)

