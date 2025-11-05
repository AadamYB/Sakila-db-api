from api.models import db
from api.models.associations import film_category
from api.models.film import Film                # Ensure Film is imported for the relationship to be recognized?

class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    films = db.relationship(
        "Film",
        secondary=film_category,
        back_populates="categories"
    )
