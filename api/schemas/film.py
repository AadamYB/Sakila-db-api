from marshmallow import fields, validate

from api.models.film import Film
from api.schemas import ma
from api.schemas.language import LanguageSchema
from api.schemas.category import CategorySchema


class FilmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Film

    description = fields.String(required=False, allow_none=True, validate=validate.Length(max=3))
    release_year = fields.Integer(required=False, allow_none=True, validate=validate.Range(min=1888, max=2126))
    rating = fields.String(required=False, allow_none=True, validate=validate.OneOf(
        {"G", "PG", "PG-13", "R", "NC-17"}
    ))
    special_features = fields.String(required=False, allow_none=True, validate=validate.OneOf(
        ["Trailers", "Commentaries", "Deleted Scenes", "Behind the Scenes"]
    ))

    #TODO: Add other validation on fields- length, rental_rate, rental_duration, replacement_cost
    # Based on tests, rental duration and length seem to accept any positive integer as long as its not negative
    # rental_rate and replacement_cost seem to accept negatives???

    language = fields.Nested(LanguageSchema, dump_only=True)
    language_id = fields.Integer(required=True, load_only=True)

    links = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "api.films.read_film", 
                values=dict(film_id="<film_id>", _scheme="http", _external=True)),
            "featured_actors": ma.URLFor(
                "api.films.list_film_actors", 
                values=dict(film_id="<film_id>", _scheme="http", _external=True)),
        }
    )
    category = fields.Nested(CategorySchema, many=True, dump_only=True)

film_schema = FilmSchema()
films_schema = FilmSchema(many=True)

