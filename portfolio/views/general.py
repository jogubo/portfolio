from flask import Blueprint
from flask import render_template

from portfolio.models import Category

bp = Blueprint('general', __name__)


def get_categories():
    return Category.query.all()


@bp.route('/')
def index():
    return render_template('general/index.html')
