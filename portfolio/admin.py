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

from portfolio.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            db = get_db()
            user = db.execute(
                'SELECT * FROM user WHERE id = ?', (1,)
            ).fetchone()
            if user:
                return redirect(url_for('admin.login'))
            elif user is None:
                return redirect(url_for('admin.create'))

        return view(**kwargs)

    return wrapped_view


def admin_exists():
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (1,)
    ).fetchone()

    return True if user is not None else False


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/', methods=('GET', 'POST'))
@login_required
def admin():
    db = get_db()
    error = None

    if request.method == 'POST':
        name = request.form['name']
        # hide = request.form['hide']
        if not name:
            error = 'Name is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO category (name, hide) VALUES (?, ?)',
                    (name, False),
                )
                db.commit()
            except db.IntegrityError:
                error = f'{name} category already exists.'
            else:
                return redirect(url_for('admin.admin'))

        flash(error)

    return render_template('admin/index.html')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    permission = False if admin_exists() else True

    if permission and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                return redirect(url_for('admin.login'))

        flash(error)

    if permission:
        return render_template('admin/create-admin-user.html')
    else:
        return redirect(url_for('admin.admin'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('admin.admin'))

        flash(error)

    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
