import unittest
from flask_login import current_user
from flask_testing import TestCase

from project import app, db
from project.main.views import datetimefilter
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
        db.session.add(User('test', 'test'))
        db.session.add(WeatherRegistration(6167865, 'Toronto', 'Canada', 1))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class HelperTests(BaseTestCase):
    def test_datetimefilter(self):
        '''
        Validate jinja datetime filter.

        :return:
        '''

        date = datetimefilter(1549465200)  # UTC timestamp
        self.assertEqual(date, 'Wednesday')


class RegistrationTests(BaseTestCase):
    def test_city_registration(self):
        self.client.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)


class LoginTests(BaseTestCase):
    '''
    A set of login/logout tests.
    '''

    def test_login_page_response_code(self):
        '''
        Check response code from login screen.

        :return:
        '''

        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_response(self):
        '''
        Check response data from login screen.

        :return:
        '''
        response = self.client.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    def test_correct_login(self):
        '''
        Validate login credentials and redirected page and response.

        :return:
        '''
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username='test', password='test'),
                follow_redirects=True)
            self.assertIn(b'You are logged in', response.data)
            self.assertTrue(current_user.username == 'test')
            self.assertTrue(current_user.is_active)

    def test_incorrect_login(self):
        '''
        Validate incorrect credentials and error response.

        :return:
        '''
        response = self.client.post(
            '/login',
            data=dict(username='incorrect', password='incorrect'),
            follow_redirects=True
        )
        self.assertIn(b'Invalid log in credentials', response.data)

    def test_logout(self):
        '''
        Validate logout.

        :return:
        '''
        with self.client:
            self.client.post(
                '/login',
                data=dict(username='test', password='test'),
                follow_redirects=True
            )
            self.assertTrue(current_user.username == 'test')
            self.assertTrue(current_user.is_active)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out', response.data)
            self.assertFalse(current_user.is_active)

    def test_main_route_requires_login(self):
        '''
        Validate routing works if not logged in.

        :return:
        '''
        response = self.client.get('/', follow_redirects=True)
        self.assertTrue(b'Please log in' in response.data)

    def test_main_route_requires_logout(self):
        '''
        Validate routing works if not logged in.

        :return:
        '''
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in', response.data)


class RegistrationTest(BaseTestCase):
    '''
    Validate user registration

    :return:
    '''
    def test_registration(self):
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(username='testuser', password='testuser', confirm='testuser'),
                follow_redirects=True
            )
            self.assertIn(b'Welcome to the OpenWeatherMap Interface', response.data)
            self.assertTrue(current_user.username == 'testuser')
            self.assertTrue(current_user.is_active)


if __name__ == '__main__':
    unittest.main()
