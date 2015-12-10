import unittest

from profitbricks.client import ProfitBricksService

location_id = 'location_id'


class TestLocation(unittest.TestCase):
    def setUp(self):
        self.location = ProfitBricksService(
            username='username', password='password')

    def test_list_locations(self):
        locations = self.location.list_locations()

        self.assertEqual(len(locations), 4)
        self.assertEqual(locations['items'][0]['id'], 'de/fra')
        self.assertEqual(
            locations['items'][0]['properties']['name'], 'Europe / Germany / Frankfurt')

    def test_get_location(self):
        location = self.location.get_location(location_id)

        self.assertEqual(location['id'], 'de/fra')
        self.assertEqual(
            location['properties']['name'], 'Europe / Germany / Frankfurt')

if __name__ == '__main__':
    unittest.main()
