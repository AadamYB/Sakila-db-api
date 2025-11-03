from api.models import db
from api.models.associations import film_actor
from api.models.film import Film                # Ensure Film is imported for the relationship to be recognized?

class Actor(db.Model):
    __tablename__ = 'actor'

    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    films = db.relationship(
        "Film",
        secondary=film_actor,
        back_populates="actors"
    )