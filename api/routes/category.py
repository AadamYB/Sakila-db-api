from flask import Blueprint, jsonify, request, url_for
from marshmallow import ValidationError

from api.models import db
from api.models.category import Category
from api.schemas.category import category_schema, categories_schema

categories_router = Blueprint('categories', __name__, url_prefix='/categories')

@categories_router.get('/')
def read_all_categories():
    category = Category.query.all()

    if not category:
        return 'Category Not Found', 404
    
    return categories_schema.jsonify(category), 200


@categories_router.get('/<int:category_id>')
def read_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return 'Category Not Found', 404
    
    return category_schema.dump(category), 200


@categories_router.patch('/')
def update_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return 'Category Not Found', 404
    
    category_data = request.json
    if not category_data:
        return 'ERROR! Missing Payload', 400

    try:
        category_schema.load(category_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in category_data.items():
        setattr(category, key, value)

    db.session.commit()

    return category_schema.dump(category), 200


@categories_router.delete('/<int:category_id>')
def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return 'Category Not Found', 404

    db.session.delete(category)
    db.session.commit()

    return '', 204