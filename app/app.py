from flask import Flask, render_template, request, redirect, url_for,session
from forms import SignupForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from conexionDB import UserDatabase

import pymysql
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mondongo'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion'

dbu = UserDatabase( app )
login_manager = LoginManager( app )
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return dbu.get_user_by_id(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        admin = False
        if dbu.existing_user(email):
            print('Usuario ya registrado')
            return redirect(url_for('signup'))
        if admin == True:
            admin = 1
        else:
            admin = 0
        if remember_me == True:
            remember_me = 1
        else:
            remember_me = 0
        dbu.create_user(name, email, password, remember_me, admin)
        login_user(user=dbu.get_user_by_email(email), remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('sign_up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        if remember_me == True:
            remember_me = 1
        else:
            remember_me = 0
        user = dbu.get_user_by_email(email)
        print(user.password)
        if user and user.check_password(password):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
