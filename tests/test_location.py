import unittest

from helpers import configuration
from helpers.resources import resource
from profitbricks.client import ProfitBricksService
from profitbricks.errors import PBNotFoundError


class TestLocation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

    def test_list_locations(self):
        locations = self.client.list_locations()

        self.assertEqual(len(locations), 4)
        for location in locations['items']:
            self.assertEqual(location['type'], 'location')
            self.assertIn(location['id'], self.resource['locations'])

    def test_get_location(self):
        location = self.client.get_location(configuration.LOCATION)

        self.assertEqual(location['type'], 'location')
        self.assertEqual(location['id'], configuration.LOCATION)

    def test_get_failure(self):
        try:
            self.client.get_location(location_id='00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
