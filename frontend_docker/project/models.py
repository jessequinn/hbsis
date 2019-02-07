from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from project import db, bcrypt


class WeatherRegistration(db.Model):
    __tablename__ = "registrations"

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    city_id = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, city, city_id, country, user_id):
        self.city = city
        self.city_id = city_id
        self.country = country
        self.user_id = user_id

    def __repr__(self):
        # return '{} - {} - {} - {} - {}'.format(self.id, self.city, self.city_id, self.country, self.user_id)
        return '{} - {}'.format(self.city_id, self.user_id)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.Binary(60), nullable=False)
    registrations = relationship("WeatherRegistration", backref="user")

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '{}'.format(self.username)

    def is_authenticated(self):
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
