import unittest

from profitbricks.client import ProfitBricksService


class TestProvisioningRequest(unittest.TestCase):
    def setUp(self):
        self.provisioning_request = ProfitBricksService(
            username='username', password='password')

    def test_list_requests(self):
        prov_requests = self.provisioning_request.list_requests()

        self.assertEqual(len(prov_requests), 4)
        self.assertEqual(
            prov_requests['items'][0]['id'],
            '59359eae-cdcd-406f-900b-58b3ad9d8de9')

    def test_get_request(self):
        request_id = '59359eae-cdcd-406f-900b-58b3ad9d8de9'
        prov_request = self.provisioning_request.get_request(request_id)

        self.assertEqual(prov_request['metadata']['createdBy'], 'User X')

    def test_get_request_with_status(self):
        request_id = '59359eae-cdcd-406f-900b-58b3ad9d8de9'
        prov_request = self.provisioning_request.get_request(
            request_id, status=True)

        self.assertEqual(
            prov_request['metadata']['requestStatus'], 'RUNNING')

if __name__ == '__main__':
    unittest.main()
