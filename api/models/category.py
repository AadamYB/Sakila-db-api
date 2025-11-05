from api.models import db
from api.models.associations import film_category

class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    films = db.relationship(
        "Film",
        secondary=film_category,
        back_populates="categories"
    )
