from project.main.views import datetimefilter

from base import BaseTestCase


class HelperTests(BaseTestCase):
    def test_datetimefilter(self):
        '''
        Validate jinja datetime filter.

        :return:
        '''

        date = datetimefilter(1549465200)  # UTC timestamp
        self.assertEqual(date, 'Wednesday')
