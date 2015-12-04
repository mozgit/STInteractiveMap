from functools import wraps
from flask import request, Response
from flask import redirect, url_for
from app import login_manager
from flask.ext.login import UserMixin
import flask.ext.login as flask_login
from flask import render_template

def get_users():
    return {'admin': {'password': '1234'}, 'Ilya': {'password': '1234'}}

class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in get_users():
        return

    user = User()
    user.id = email
    return user

#def login_required(f):
#    @wraps(f)
#    def decorated_function(*args, **kwargs):
#        if g.user is None:
#            return redirect(url_for('login', wantsurl = request.path))
#        return f(*args, **kwargs)
#    return decorated_function


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in get_users():
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    users = get_users()
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('Login.html', wantsurl=url_for('hello'))


