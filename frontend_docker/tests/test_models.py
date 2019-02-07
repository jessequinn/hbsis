import unittest
from flask_login import current_user
from project import bcrypt
from project.models import User, WeatherRegistration

from base import BaseTestCase


class RegistrationTest(BaseTestCase):
    '''
    Validate user registration

    :return:
    '''

    def test_user_registration(self):
        '''
        Validate registration of user.

        :return:
        '''
        with self.client:
            response = self.client.post('/register', data=dict(username='testuser2', password='longpassword',
                                                               confirm='longpassword'), follow_redirects=True)
            self.assertIn(b'Welcome to the OpenWeatherMap Interface', response.data)
            self.assertTrue(current_user.username == 'testuser2')
            self.assertTrue(current_user.is_active)

    def test_get_id(self):
        '''
        Validate that correct user id is returned.

        :return:
        '''
        with self.client:
            self.client.post('/login', data=dict(username="testuser", password='testuser'), follow_redirects=True)
            self.assertTrue(current_user.id == 1)

    def test_password(self):
        '''
        Validate password.

        :return:
        '''
        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'testuser'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'incorrect'))

    def test_city_id(self):
        '''
        Validate correct city id.

        :return:
        '''
        weatherRegistration = WeatherRegistration.query.filter_by(city_id=6167865).first()
        self.assertTrue(str(weatherRegistration) == '6167865 - 1')


if __name__ == '__main__':
    unittest.main()
