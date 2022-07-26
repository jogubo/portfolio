from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from portfolio.database import db_session
from portfolio.models import User
from portfolio.models import Category
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
        hidden = True if 'hidden' in request.form else False
        error = None

        if not name:
            error = 'Category name is required.'

        if error is None:
            category = Category(name, hidden)
            db_session.add(category)
            db_session.commit()
            return redirect(url_for('admin.index'))

        flash(error)

    else:
        return render_template('admin/categories.html')
