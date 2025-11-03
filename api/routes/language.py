from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from api.models import db
from api.models.language import Language
from api.schemas.language import language_schema, languages_schema

languages_router = Blueprint('languages', __name__, url_prefix='/languages')

@languages_router.get('/')
def read_all_languages():
    languages = Language.query.all()
    return languages_schema.jsonify(languages), 200


@languages_router.get('/<language_id>')
def read_language(language_id):
    language = Language.query.get(language_id)
    return language_schema.dump(language), 200

@languages_router.post('/')
def create_language():
    language_data = request.json

    try:
        language_schema.load(language_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_language = Language(**language_data)
    db.session.add(new_language)
    db.session.commit()

    return language_schema.dump(new_language), 201

@languages_router.patch('/<language_id>')
def update_language(language_id):
    language = Language.query.get(language_id)

    if not language:
        return 'Language Not Found', 404
    
    language_data = request.json
    if not language_data:
        return 'ERROR! Missing Payload', 400

    try:
        language_schema.load(language_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in language_data.items():
        setattr(language, key, value)

    db.session.commit()

    return language_schema.dump(language), 200

@languages_router.delete('/<language_id>')
def delete_language(language_id):
    language = Language.query.get(language_id)

    if not language:
        return 'Language Not Found', 404

    db.session.delete(language)
    db.session.commit()

    return '', 204

    