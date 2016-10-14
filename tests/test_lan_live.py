import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Server, LAN, NIC
from six import assertRegex


class TestLan(unittest.TestCase):
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


def test_list_lans(self):
    lans = self.client.list_lans(datacenter_id=self.datacenter['id'])

    self.assertGreater(len(lans), 0)
    self.assertEqual(lans['items'][0]['type'], 'lan')
    self.assertIn(lans['items'][0]['id'], ('1', '2', '3'))
    self.assertEqual(lans['items'][0]['properties']['name'], self.resource['lan']['name'])
    self.assertTrue(lans['items'][0]['properties']['public'], self.resource['lan']['public'])


def test_get_lan(self):
    lan = self.client.get_lan(datacenter_id=self.datacenter['id'], lan_id=self.lan['id'])

    self.assertEqual(lan['type'], 'lan')
    self.assertEqual(lan['id'], self.lan['id'])
    self.assertEqual(lan['properties']['name'], self.resource['lan']['name'])
    self.assertTrue(lan['properties']['public'], self.resource['lan']['public'])


def test_delete_lan(self):
    lan = self.client.create_lan(
        datacenter_id=self.datacenter['id'],
        lan=LAN(**self.resource['lan']))

    wait_for_completion(self.client, lan, 'create_lan')

    lan = self.client.delete_lan(datacenter_id=self.datacenter['id'], lan_id=lan['id'])

    self.assertTrue(lan)


def test_update_lan(self):
    lan = self.client.update_lan(
        datacenter_id=self.datacenter['id'],
        lan_id=self.lan['id'],
        name=self.resource['lan']['name'] + ' RENAME',
        public=False)

    self.assertEqual(lan['type'], 'lan')
    self.assertEqual(lan['properties']['name'], self.resource['lan']['name'] + ' RENAME')
    self.assertFalse(lan['properties']['public'])


def test_create_lan(self):
    self.assertEqual(self.lan['id'], '1')
    self.assertEqual(self.lan['type'], 'lan')
    self.assertEqual(self.lan['properties']['name'], self.resource['lan']['name'])
    self.assertEqual(self.lan['properties']['public'], self.resource['lan']['public'])


def test_create_complex_lan(self):
    resource = NIC(**self.resource['nic'])

    nic1 = self.client.create_nic(
        datacenter_id=self.datacenter['id'],
        server_id=self.server['id'],
        nic=resource)
    wait_for_completion(self.client, nic1, 'create_nic1')
    self.assertFalse(nic1['properties']['nat'])
    self.assertEqual(nic1['properties']['name'], 'Python SDK Test')
    self.assertTrue(nic1['properties']['dhcp'])
    self.assertEqual(nic1['properties']['lan'], 1)
    self.assertTrue(nic1['properties']['firewallActive'])

    nics = [nic1['id']]
    lan = LAN(nics=nics, **self.resource['lan'])

    response = self.client.create_lan(
        datacenter_id=self.datacenter['id'],
        lan=lan)
    wait_for_completion(self.client, response, 'create_lan')

    self.assertEqual(response['type'], 'lan')
    self.assertEqual(response['properties']['name'], self.resource['lan']['name'])
    self.assertTrue(response['properties']['public'])


def test_get_lan_members(self):
    members = self.client.get_lan_members(
        datacenter_id=self.datacenter['id'],
        lan_id=self.lan['id'])

    self.assertGreater(len(members), 0)
    self.assertEqual(members['items'][0]['type'], 'nic')
    self.assertEqual(members['items'][0]['properties']['name'], self.resource['nic']['name'])
    assertRegex(self, members['items'][0]['properties']['mac'], self.resource['mac_match'])


if __name__ == '__main__':
    unittest.main()
