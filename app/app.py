from flask import Flask, render_template, request, redirect, url_for, url_parse
from forms import SignupForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from userG import User, get_user,users

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
        user = User(name,email,password,False)
        login_user(user, remember=remember_me)
        return redirect(url_for('index'))
    return render_template('sign_up.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

if __name__ == '__main__':
    app.run(debug=True)
