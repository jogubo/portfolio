from flask import Blueprint
from flask import request
from flask import jsonify

from portfolio.database import db_session
from portfolio.models import User
from portfolio.models import Category
from portfolio.models import Picture
from portfolio.serializers import UserSerializer
from portfolio.serializers import CategorySerializer
from portfolio.serializers import PicturesSerializer

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/users/', methods=['GET', 'POST'])
@bp.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_api(user_id: int = None) -> jsonify:

    serializer = UserSerializer()

    if user_id is None:
        query = User.query.all()
    else:
        query = User.query.get(user_id)

    if request.method == 'POST':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass

    if user_id is None:
        return jsonify(serializer.list(query))
    else:
        return jsonify(serializer.detail(query))


@bp.route('/categories/', methods=['GET', 'POST'])
@bp.route('/categories/<category_id>', methods=['GET', 'PUT', 'DELETE'])
def category_api(category_id: int = None) -> jsonify:

    serializer = CategorySerializer()

    if category_id is None:
        query = Category.query.all()
    else:
        query = Category.query.get(category_id)

    if request.method == 'POST':
        name = request.json['name']
        hidden = request.json['hidden']
        category = Category(name, hidden)
        category.set_name_url()
        db_session.add(category)
        db_session.commit()
        return jsonify(serializer.detail(category), 201)

    if request.method == 'PUT':
        category = query
        if 'name' in request.json['name']:
            category.name = request.json
            category.set_name_url()
        if 'hidden' in request.json:
            category.hidden = request.json['hidden']
        db_session.commit()
        return jsonify(serializer.detail(category), 200)

    if request.method == 'DELETE':
        category = query
        db_session.delete(category)
        db_session.commit()
        return jsonify(None, 204)

    if category_id is None:
        return jsonify(serializer.list(query))
    else:
        return jsonify(serializer.detail(query))


@bp.route('/pictures/', methods=['GET', 'POST'])
@bp.route('/pictures/<picture_id>', methods=['GET', 'PUT', 'DELETE'])
def picture_api(picture_id: int = None) -> jsonify:

    serializer = PicturesSerializer()

    if picture_id is None:
        query = Picture.query.all()
    else:
        query = Picture.query.get(picture_id)

    if request.method == 'POST':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass

    if picture_id is None:
        query = Picture.query.all()
        return jsonify(serializer.list(query))
    else:
        query = Picture.query.get(picture_id)
        return jsonify(serializer.detail(query))

    # return jsonify({'request_error': f'{request.method}'})
