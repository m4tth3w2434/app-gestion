from flask import Flask, render_template, request, redirect, url_for,session
from forms import SignupForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from userG import User, get_user,users,database

import pymysql
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion'
mysql1= database()
mysql = pymysql.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'],
                        password=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mondongo'

login_manager = LoginManager( app )
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
        remember_me = form.remember_me.data
        user = User(name,email,password,remember_me,False)
        create_user = mysql1.create_user(user.name, user.email, user.password, user.remember_me, user.is_Admin)
        ids = mysql1.get_user_by_id(email)
        user.set_id(ids)
        users.append(user)
        login_user(user, remember=remember_me)
        return redirect(url_for('index'))
    return render_template('sign_up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = get_user(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=remember_me)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)



@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

if __name__ == '__main__':
    app.run(debug=True)
