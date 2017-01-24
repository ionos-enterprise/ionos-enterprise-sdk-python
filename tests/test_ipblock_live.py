import unittest

from helpers import configuration
from helpers.resources import resource
from profitbricks.client import IPBlock
from profitbricks.client import ProfitBricksService
from six import assertRegex


class TestIPBlock(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        ipblock1 = IPBlock(**self.resource['ipblock'])
        self.ipblock1 = self.client.reserve_ipblock(ipblock1)

        ipblock2 = IPBlock(**self.resource['ipblock'])
        self.ipblock2 = self.client.reserve_ipblock(ipblock2)

    @classmethod
    def tearDownClass(self):
        self.client.delete_ipblock(self.ipblock1['id'])

    def test_list_ipblocks(self):
        ipblocks = self.client.list_ipblocks()

        assertRegex(self, ipblocks['items'][0]['id'], self.resource['uuid_match'])
        self.assertGreater(len(ipblocks), 0)
        assertRegex(self, ipblocks['items'][0]['id'], self.resource['uuid_match'])
        self.assertGreater(ipblocks['items'][0]['properties']['size'], 0)
        self.assertIn(ipblocks['items'][0]['properties']['location'], self.resource['locations'])

    def test_get_ipblock(self):
        ipblock = self.client.get_ipblock(self.ipblock1['id'])

        assertRegex(self, ipblock['id'], self.resource['uuid_match'])
        self.assertEqual(ipblock['id'], self.ipblock1['id'])
        self.assertEqual(ipblock['properties']['name'], (self.resource['ipblock']['name']))
        self.assertEqual(ipblock['properties']['size'], self.resource['ipblock']['size'])
        self.assertEqual(ipblock['properties']['location'], self.resource['ipblock']['location'])

    def test_delete_ipblock(self):
        ipblock = self.client.delete_ipblock(self.ipblock2['id'])

        self.assertTrue(ipblock)

    def test_reserve_ipblock(self):
        ipblock = self.client.reserve_ipblock(IPBlock(**self.resource['ipblock']))

        assertRegex(self, ipblock['id'], self.resource['uuid_match'])
        self.assertEqual(ipblock['properties']['name'], (self.resource['ipblock']['name']))
        self.assertEqual(ipblock['properties']['size'], self.resource['ipblock']['size'])
        self.assertEqual(ipblock['properties']['location'], self.resource['ipblock']['location'])

        self.client.delete_ipblock(ipblock['id'])


if __name__ == '__main__':
    unittest.main()
