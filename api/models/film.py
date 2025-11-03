from api.models import db
from api.models.associations import film_actor
from api.models.language import Language
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Film(db.Model):
    __tablename__ = 'film'

    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_year = db.Column(db.Integer, nullable=True)
    language_id = db.Column(ForeignKey('language.language_id'), nullable=False)
    language = relationship(Language, foreign_keys=[language_id])
    original_language_id = db.Column(ForeignKey('language.language_id'), nullable=True)
    rental_duration = db.Column(db.Integer, default=3, nullable=False)
    rental_rate = db.Column(db.Float, default=4.99, nullable=False)
    length = db.Column(db.Integer, nullable=True)
    replacement_cost = db.Column(db.Float, default=19.99, nullable=False)
    rating = db.Column(db.String(10), default="G", nullable=True)
    special_features = db.Column(db.String(255), nullable=True)

    actors = db.relationship(
        "Actor",
        secondary=film_actor,
        back_populates="films"
    )