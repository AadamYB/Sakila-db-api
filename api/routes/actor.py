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

    if not actor:
        return 'Actor Not Found', 404
    
    if not actor.films:
        return 'No Films Found for this Actor', 404
    
    return jsonify([{
        'film_id': f.film_id, 
        'title': f.title,
        'link': {
            'href': url_for('api.films.read_film', film_id=f.film_id, _external=True)
            }
        } 
        for f in actor.films]), 200


@actors_router.get('')
def list_actors_per_page():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per-page', 10, type=int)
    f_name_filter = request.args.get('first_name', None, type=str)
    l_name_filter = request.args.get('last_name', None, type=str)
 
    query = Actor.query

    if f_name_filter:
        query = query.filter(Actor.first_name.ilike(f'%{f_name_filter}%'))
    if l_name_filter:
        query = query.filter(Actor.last_name.ilike(f'%{l_name_filter}%'))

    actor_pagination = query.paginate(page=page, per_page=per_page)
    actors = actor_pagination.items

    
    return jsonify({
        'results': actors_schema.dump(actors),
        'pagination': {
            'count': actor_pagination.total,
            'page': actor_pagination.page,
            'per_page': actor_pagination.per_page,
            'pages': actor_pagination.pages,
            'links': {
                'self_url': url_for('api.actors.list_actors_per_page', page=actor_pagination.page, per_page=per_page, _external=True),
                'next_url': url_for('api.actors.list_actors_per_page', page=actor_pagination.next_num, per_page=per_page, _external=True) if actor_pagination.has_next else None,
                'prev_url': url_for('api.actors.list_actors_per_page', page=actor_pagination.prev_num, per_page=per_page, _external=True) if actor_pagination.has_prev else None,
            }
        }
    }), 200