from flask import Blueprint
from flask import render_template

bp = Blueprint('category', __name__, url_prefix='/category')


@bp.route('/<name>')
def category(name):
    pass
