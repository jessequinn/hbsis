from flask_testing import TestCase
from project import app, db
from project.models import User, WeatherRegistration


class BaseTestCase(TestCase):
    '''
    Backend setup and destruction.
    '''

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User('testuser', 'testuser'))
        db.session.add(WeatherRegistration('Toronto', 6167865, 'Canada', 1))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
