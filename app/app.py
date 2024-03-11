from flask import Flask, render_template, request, redirect, url_for
from forms import SignupForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from userG import users, get_user

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


if __name__ == '__main__':
    app.run(debug=True)