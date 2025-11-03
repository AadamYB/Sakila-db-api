from api.models import db

class Language(db.Model):
    language_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)