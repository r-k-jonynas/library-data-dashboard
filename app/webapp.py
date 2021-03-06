from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.extensions import db
from app.forms import LoginForm
from app.models import User

# Enables role-based authentication
from functools import wraps

def requires_roles(roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated == False:
                flash("You have to login before you can access this site.")
                return redirect(url_for('main.login'))
            if current_user.role not in roles:
                flash("Your Account doesn't have access to this site.")
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        try:
            return wrapped
        except Exception as e:
            print(e)
    return wrapper
    

server_bp = Blueprint('main', __name__)

@server_bp.route('/')
def index():
    return render_template('index.html', title='Home Page')


@server_bp.route('/login/', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@server_bp.route("/logout/")
@login_required
def logout():
    logout_user()

    flash("you are logged out!")
    return redirect(url_for('main.index'))
