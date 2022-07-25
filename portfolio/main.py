from flask import Blueprint
from flask import render_template

from portfolio.db import get_db

bp = Blueprint('main', __name__)


def load_categories():
    db = get_db()
    categories = db.execute('SELECT * FROM category')

    return categories


@bp.route('/')
def index():
    return render_template('main/index.html')
