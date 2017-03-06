import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Server, LAN, NIC


class TestNic(unittest.TestCase):
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
        wait_for_completion(self.client, self.datacenter, 'create_datacenter')

        # Create test LAN.
        self.lan = self.client.create_lan(
            datacenter_id=self.datacenter['id'],
            lan=LAN(**self.resource['lan']))
        wait_for_completion(self.client, self.lan, 'create_lan')

        # Create test server.
        self.server = self.client.create_server(
            datacenter_id=self.datacenter['id'],
            server=Server(**self.resource['server']))
        wait_for_completion(self.client, self.server, 'create_server')

        # Create test NIC1.
        nic1 = NIC(**self.resource['nic'])
        nic1.lan = self.lan['id']
        self.nic1 = self.client.create_nic(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic=nic1)
        wait_for_completion(self.client, self.nic1, 'create_nic1')

        # Create test NIC2.
        nic2 = NIC(**self.resource['nic'])
        nic2.lan = self.lan['id']
        self.nic2 = self.client.create_nic(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic=nic2)
        wait_for_completion(self.client, self.nic2, 'create_nic2')

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_list_nics(self):
        nics = self.client.list_nics(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'])

        self.assertGreater(len(nics), 0)
        self.assertIn(nics['items'][0]['id'], (self.nic1['id'], self.nic2['id']))
        self.assertEqual(nics['items'][0]['type'], 'nic')

    def test_get_nic(self):
        nic = self.client.get_nic(datacenter_id=self.datacenter['id'],
                                  server_id=self.server['id'],
                                  nic_id=self.nic1['id'])

        self.assertEqual(nic['type'], 'nic')
        self.assertEqual(nic['id'], self.nic1['id'])
        self.assertEqual(nic['properties']['name'], self.nic1['properties']['name'])

    def test_delete_nic(self):
        nic2 = self.client.delete_nic(datacenter_id=self.datacenter['id'],
                                      server_id=self.server['id'],
                                      nic_id=self.nic2['id'])

        self.assertTrue(nic2)

    def test_update_nic(self):
        nic = self.client.update_nic(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'],
            name=self.resource['nic']['name'] + ' RENAME')

        self.assertEqual(nic['type'], 'nic')
        self.assertEqual(nic['properties']['name'], self.resource['nic']['name'] + ' RENAME')

    def test_create_nic(self):
        self.assertEqual(self.nic1['type'], 'nic')
        self.assertEqual(self.nic1['properties']['name'], self.resource['nic']['name'])


if __name__ == '__main__':
    unittest.main()
