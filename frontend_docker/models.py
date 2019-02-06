from app import db


class WeatherRegistration(db.Model):
    __tablename__ = "registrations"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)

    def __init__(self, id, city, country):
        self.id = id
        self.city = city
        self.country = country

    def __repr__(self):
        return '{} - {}'.format(self.id, self.city)
