from flask import Blueprint
from flask import render_template

from portfolio.models import Category

bp = Blueprint('general', __name__)


def get_categories():
    return Category.query.all()


@bp.route('/')
def index():
    return render_template('general/index.html')


@bp.route('/gallery/<category_name_url>')
def gallery(category_name_url: str):
    category = Category.query.filter_by(name_url=category_name_url).first()
    return render_template('general/index.html', pictures=category.pictures)


@bp.route('/contact')
def contact():
    return render_template('general/contact.html')
