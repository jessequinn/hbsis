import unittest
from flask_login import current_user

from base import BaseTestCase


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
                data=dict(username='testuser', password='testuser'),
                follow_redirects=True)
            self.assertIn(b'You are logged in', response.data)
            self.assertTrue(current_user.username == 'testuser')
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
                data=dict(username='testuser', password='testuser'),
                follow_redirects=True
            )
            self.assertTrue(current_user.username == 'testuser')
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


class WeatherRegistrationTest(BaseTestCase):
    def test_city_registration_exists(self):
        '''
        Validate that when data conflicts proper response is given.

        :return:
        '''
        with self.client:
            self.client.post(
                '/login',
                data=dict(username='testuser', password='testuser'),
                follow_redirects=True
            )
            self.assertTrue(current_user.username == 'testuser')
            self.assertTrue(current_user.is_active)
            response = self.client.post(
                '/',
                data=dict(city='Toronto', city_id=6167865, country='CA', user_id=1),
                follow_redirects=True
            )
            self.assertIn(b'Toronto has already been registered.', response.data)

    def test_city_registration(self):
        '''
        Validate that a new city is properly registered.

        :return:
        '''
        with self.client:
            self.client.post(
                '/login',
                data=dict(username='testuser', password='testuser'),
                follow_redirects=True
            )
            self.assertTrue(current_user.username == 'testuser')
            self.assertTrue(current_user.is_active)
            response = self.client.post(
                '/',
                data=dict(city='Ottawa', city_id=6094817, country='CA', user_id=1),
                follow_redirects=True
            )
            self.assertIn(b'Ottawa was registered successfully.', response.data)


if __name__ == '__main__':
    unittest.main()
