import os

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import current_app
from werkzeug.urls import url_fix
from werkzeug.utils import secure_filename

from portfolio.database import db_session
from portfolio.models import User
from portfolio.models import Category
from portfolio.models import Picture
from portfolio.views.auth import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(1)


@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/categories', methods=('GET', 'POST'))
@login_required
def manage_categories():

    if request.method == 'POST':
        name = request.form['name']
        name_url = url_fix(name).replace('%20', '-').lower()
        hidden = True if 'hidden' in request.form else False
        error = None

        if not name:
            error = 'Category name is required.'

        if error is None:
            category = Category(name, name_url, hidden)
            db_session.add(category)
            db_session.commit()
            return redirect(url_for('admin.index'))

        flash(error)

    else:
        return render_template('admin/categories.html')


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload_picture():

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        file = request.files['file']
        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            filename = secure_filename(file.filename).lower()
            file.save(
                os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            )
            picture = Picture(title, description, category, filename)
            db_session.add(picture)
            db_session.commit()
            return redirect(url_for('admin.index'))

        flash(error)

    else:
        return render_template('admin/upload.html')
