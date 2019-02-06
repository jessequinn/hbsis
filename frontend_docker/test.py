import unittest

from project import app
from project.main.views import datetimefilter

class TestFrontend(unittest.TestCase):

    def test_login_page_response_code(self):
        '''
        Check response code from login screen.

        :return:
        '''
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_response(self):
        '''
        Check response data from login screen.

        :return:
        '''
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    def test_correct_login(self):
        '''
        Validate login credentials and redirected page and response.

        :return:
        '''
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)
        self.assertIn(b'You are logged in', response.data)

    def test_incorrect_login(self):
        '''
        Validate incorrect credentials and error response.

        :return:
        '''
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='incorrect', password='incorrect'),
            follow_redirects=True)
        self.assertIn(b'Invalid Credentials', response.data)

    def test_logout(self):
        '''
        Validate logout.

        :return:
        '''
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out', response.data)

    def test_main_route_requires_login(self):
        '''
        Validate routing works if not logged in.

        :return:
        '''
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'Please login' in response.data)

    def test_datetimefilter(self):
        '''
        Validate jinja datetime filter

        :return:
        '''

        date = datetimefilter(1549465200)  # UTC timestamp
        self.assertEqual(date, 'Wednesday')

    def test_city_registration(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
