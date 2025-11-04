from flask import Blueprint, jsonify, request, url_for
from marshmallow import ValidationError

from api.models import db
from api.models.actor import Actor
from api.schemas.actor import actor_schema, actors_schema

actors_router = Blueprint('actors', __name__, url_prefix='/actors')

@actors_router.get('/')
def read_all_actors():
    actors = Actor.query.all()

    if not actors:
        return 'Actor Not Found', 404
    
    return actors_schema.jsonify(actors), 200

@actors_router.get('/<int:actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get(actor_id)

    if not actor:
        return 'Actor Not Found', 404
    
    return actor_schema.dump(actor), 200

@actors_router.post('/')
def create_actor():
    actor_data = request.json

    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_actor = Actor(**actor_data)
    db.session.add(new_actor)
    db.session.commit()

    return actor_schema.dump(new_actor), 201


@actors_router.patch('/<int:actor_id>')
def update_actor(actor_id):
    actor = Actor.query.get(actor_id)

    if not actor:
        return 'Actor Not Found', 404
    
    actor_data = request.json
    if not actor_data:
        return 'ERROR! Missing Payload', 400

    try:
        actor_schema.load(actor_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in actor_data.items():
        setattr(actor, key, value)

    db.session.commit()

    return actor_schema.dump(actor), 200


@actors_router.delete('/<int:actor_id>')
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    db.session.delete(actor)
    db.session.commit()

    return '', 204
    # NO CONTENT!!


@actors_router.get('/<int:actor_id>/films')
def list_actor_films(actor_id):
    actor = Actor.query.get(actor_id)
    return jsonify([{
        'film_id': f.film_id, 
        'title': f.title,
        'link': {
            'href': url_for('api.films.read_film', film_id=f.film_id, _external=True)
            }
        } 
        for f in actor.films]), 200