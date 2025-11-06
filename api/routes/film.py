from flask import Blueprint, jsonify, request, url_for
from marshmallow import ValidationError

from api.models import db
from api.models.film import Film
from api.schemas.film import film_schema, films_schema

from api.models.category import Category

films_router = Blueprint('films', __name__, url_prefix='/films')

@films_router.get('/')
def read_all_films():
    films = Film.query.all()
    return films_schema.jsonify(films), 200

@films_router.get('/<int:film_id>')
def read_film(film_id):
    film = Film.query.get(film_id)
    return film_schema.dump(film), 200

@films_router.post('/')
def create_film():
    film_data = request.json

    try:
        film_schema.load(film_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_film = Film(**film_data)
    db.session.add(new_film)
    db.session.commit()

    return film_schema.dump(new_film), 201

@films_router.patch('/<int:film_id>')
def update_film(film_id):
    film = Film.query.get(film_id)

    if not film:
        return 'Film Not Found', 404

    film_data = request.json
    if not film_data:
        return 'ERROR! Missing Payload', 400

    try:
        film_schema.load(film_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in film_data.items():
        setattr(film, key, value)

    db.session.commit()

    return film_schema.dump(film), 200


@films_router.delete('/<int:film_id>')
def delete_film(film_id):
    film = Film.query.get(film_id)

    if not film:
        return 'Film Not Found', 404

    db.session.delete(film)
    db.session.commit()

    return '', 204

@films_router.get('/<int:film_id>/actors')
def list_film_actors(film_id):
    film = Film.query.get(film_id)
    if not film:
        return 'Film Not Found', 404
    
    if not film.actors:
        return 'No Actors Found for this Film', 404
    
    return jsonify([{
        'actor_id': a.actor_id,
        'first_name': a.first_name,
        'last_name': a.last_name,
        'link': {
            'href': url_for('api.actors.read_actor', actor_id=a.actor_id, _external=True)
            }
        }
        for a in film.actors]), 200

@films_router.get('')
def list_films_per_page():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per-page', 10, type=int)
    title_filter = request.args.get('title', None, type=str)
    rating_filter = request.args.get('rating', None, type=str)
    release_year_filter = request.args.get('release_year', None, type=int)
    language_id_filter = request.args.get('language_id', None, type=int)
    category_filter = request.args.get('category', None, type=str)

    query = Film.query
    if title_filter:
        query = query.filter(Film.title.ilike(f'%{title_filter}%'))
    if rating_filter:
        query = query.filter(Film.rating == rating_filter)
    if release_year_filter:
        query = query.filter(Film.release_year == release_year_filter)
    if language_id_filter:
        query = query.filter(Film.language_id == language_id_filter)

    if category_filter:
        query = query.join(Film.categories).filter_by(Category.name.ilike(f'%{category_filter}%'))

    film_pagination = query.paginate(page=page, per_page=per_page)
    films = film_pagination.items

    
    return jsonify({
        'results': films_schema.dump(films),
        'pagination': {
            'count': film_pagination.total,
            'page': film_pagination.page,
            'per_page': film_pagination.per_page,
            'pages': film_pagination.pages,
            'links': {
                'self_url': url_for('api.films.list_films_per_page', page=film_pagination.page, per_page=per_page, _external=True),
                'next_url': url_for('api.films.list_films_per_page', page=film_pagination.next_num, per_page=per_page, _external=True) if film_pagination.has_next else None,
                'prev_url': url_for('api.films.list_films_per_page', page=film_pagination.prev_num, per_page=per_page, _external=True) if film_pagination.has_prev else None,
            }
        }
    }), 200

@films_router.get('/recommendations')
def recommended_films():
    x = request.args.get('top', None, type=int)
    if x is None or x <= 0:
        x = 5
    
    top_x_films = Film.query.order_by(Film.rating.desc()).limit(x).all()
    
    return films_schema.dump(top_x_films), 200