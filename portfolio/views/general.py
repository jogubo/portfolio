from flask import Blueprint
from flask import render_template

from portfolio.models import Category
from portfolio.models import Picture

bp = Blueprint('general', __name__)


def get_categories():
    return Category.query.all()


@bp.route('/')
def index():
    pictures = Picture.query.all()
    return render_template('general/index.html', pictures=pictures)
