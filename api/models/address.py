from api.models import db

class Address(db.Model):
    __tablename__ = 'address'

    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    address2 = db.Column(db.String(255), nullable=True)
    district = db.Column(db.String(255), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(25), nullable=False)
    location = db.Column(db.LargeBinary, nullable=False)
