import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from portfolio.database import db_session
from portfolio.models import User


bp = Blueprint('auth', __name__, url_prefix='/admin/auth')


def admin_exists():
    return True if User.query.get(1) is not None else False


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            if admin_exists():
                return redirect(url_for('auth.login'))
            else:
                return redirect(url_for('auth.create'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(1)


@bp.route('/create', methods=('GET', 'POST'))
def create():

    permission = False if admin_exists() else True

    if permission and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            admin = User(username, generate_password_hash(password))
            db_session.add(admin)
            db_session.commit()
            return redirect(url_for('admin.index'))

        flash(error)

    elif permission:
        return render_template('admin/create-admin-user.html')
    else:
        return redirect(url_for('admin.index'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        admin = User.query.get(1)

        if username is None:
            error = 'Incorrect username.'
        elif not check_password_hash(admin.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = admin.id
            return redirect(url_for('admin.index'))

        flash(error)

    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('general.index'))
