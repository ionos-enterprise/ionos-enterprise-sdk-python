import unittest

from helpers import configuration
from helpers.resources import resource
from profitbricks.client import ProfitBricksService
from profitbricks.errors import PBNotFoundError


class TestRequest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        self.requests = self.client.list_requests()
        self.request = self.requests['items'][0]

    def test_list_requests(self):
        requests = self.client.list_requests()

        self.assertGreater(len(requests), 0)
        self.assertEqual(requests['items'][0]['type'], 'request')

    def test_get_request(self):
        request = self.client.get_request(request_id=self.request['id'], status=False)

        self.assertEqual(request['type'], 'request')
        self.assertEqual(request['id'], self.request['id'])
        self.assertEqual(request['href'], self.request['href'])

    def test_get_request_status(self):
        request = self.client.get_request(request_id=self.request['id'], status=True)

        self.assertEqual(request['type'], 'request-status')
        self.assertEqual(request['id'], self.request['id'] + '/status')
        self.assertEqual(request['href'], self.request['href'] + '/status')

    def test_get_failure(self):
        try:
            self.client.get_request(request_id='00000000-0000-0000-0000-000000000000', status=False)
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
