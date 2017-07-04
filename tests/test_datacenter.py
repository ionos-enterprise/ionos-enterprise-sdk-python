import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion
from profitbricks.client import Server, Volume
from six import assertRegex

from profitbricks.client import Datacenter
from profitbricks.client import ProfitBricksService
from profitbricks.errors import PBError, PBNotFoundError


class TestDatacenter(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        self.datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_list_datacenters(self):
        datacenters = self.client.list_datacenters()

        self.assertGreater(len(datacenters), 0)
        self.assertEqual(datacenters['items'][0]['type'], 'datacenter')

    def test_get_datacenter(self):
        datacenter = self.client.get_datacenter(
            datacenter_id=self.datacenter['id'])

        assertRegex(self, datacenter['id'], self.resource['uuid_match'])
        self.assertEqual(datacenter['type'], 'datacenter')
        self.assertEqual(datacenter['id'], self.datacenter['id'])
        self.assertEqual(datacenter['properties']['name'], self.resource['datacenter']['name'])
        self.assertEqual(datacenter['properties']['description'],
                         self.resource['datacenter']['description'])
        self.assertEqual(datacenter['properties']['location'],
                         self.resource['datacenter']['location'])

    def test_get_failure(self):
        try:
            self.client.get_datacenter(datacenter_id='00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            datacenter = Datacenter(name=self.resource['datacenter']['name'])
            self.client.create_datacenter(datacenter)
        except PBError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'location',
                          e.content[0]['message'])


    def test_remove_datacenter(self):
        datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))
        wait_for_completion(self.client, datacenter, 'remove_datacenter')

        response = self.client.delete_datacenter(
            datacenter_id=datacenter['id'])

        self.assertTrue(response)

    def test_update_datacenter(self):
        datacenter = self.client.update_datacenter(
            datacenter_id=self.datacenter['id'],
            description=self.resource['datacenter']['name']+' - RENAME')
        wait_for_completion(self.client, datacenter, 'update_datacenter')
        datacenter = self.client.get_datacenter(datacenter_id=self.datacenter['id'])

        assertRegex(self, datacenter['id'], self.resource['uuid_match'])
        self.assertEqual(datacenter['id'], self.datacenter['id'])
        self.assertEqual(datacenter['properties']['name'], self.resource['datacenter']['name'])
        self.assertEqual(datacenter['properties']['description'],
                         self.resource['datacenter']['name']+' - RENAME')
        self.assertEqual(datacenter['properties']['location'],
                         self.resource['datacenter']['location'])
        self.assertGreater(datacenter['properties']['version'], 1)

    def test_create_simple(self):
        datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))
        wait_for_completion(self.client, datacenter, 'create_datacenter')

        self.assertEqual(datacenter['type'], 'datacenter')
        self.assertEqual(datacenter['properties']['name'], self.resource['datacenter']['name'])
        self.assertEqual(datacenter['properties']['description'],
                         self.resource['datacenter']['description'])
        self.assertEqual(datacenter['properties']['location'],
                         self.resource['datacenter']['location'])

        response = self.client.delete_datacenter(
            datacenter_id=datacenter['id'])
        self.assertTrue(response)

    def test_create_composite(self):
        datacenter_resource = Datacenter(**self.resource['datacenter_composite'])
        datacenter_resource.servers = [Server(**self.resource['server'])]
        datacenter_resource.volumes = [Volume(**self.resource['volume'])]

        datacenter = self.client.create_datacenter(
            datacenter=datacenter_resource)
        wait_for_completion(self.client, datacenter, 'create_datacenter_composite')

        self.assertEqual(datacenter['type'], 'datacenter')
        self.assertEqual(datacenter['properties']['name'],
                         self.resource['datacenter_composite']['name'])
        self.assertEqual(datacenter['properties']['description'],
                         self.resource['datacenter_composite']['description'])
        self.assertEqual(datacenter['properties']['location'],
                         self.resource['datacenter_composite']['location'])
        self.assertGreater(len(datacenter['entities']['servers']), 0)
        self.assertGreater(len(datacenter['entities']['volumes']), 0)

        response = self.client.delete_datacenter(
            datacenter_id=datacenter['id'])
        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
