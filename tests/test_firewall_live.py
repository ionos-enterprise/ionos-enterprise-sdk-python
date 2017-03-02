import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Server, LAN, NIC, FirewallRule
from six import assertRegex


class TestFirewall(unittest.TestCase):
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

        #Create test Firewall Rule
        fwrule=FirewallRule(**self.resource['fwrule'])
        self.fwrule = self.client.create_firewall_rule(
            datacenter_id = self.datacenter['id'],
            server_id = self.server['id'],
            nic_id = self.nic1['id'],
            firewall_rule=fwrule)

        #Create test Firewall Rule 2
        fwrule2 = FirewallRule(**self.resource['fwrule'])
        fwrule2.port_range_start = 8080
        fwrule2.port_range_end = 8080
        fwrule2.name = "8080"
        self.fwrule2 = self.client.create_firewall_rule(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'],
            firewall_rule=fwrule2)
        wait_for_completion(self.client, self.fwrule2, 'create_fwrule2')

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_list_fwrules(self):
        fwrules = self.client.get_firewall_rules(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'])

        self.assertGreater(len(fwrules), 0)
        self.assertIn(fwrules['items'][0]['id'], (self.fwrule['id'], self.fwrule2['id']))
        self.assertEqual(fwrules['items'][0]['type'], 'firewall-rule')

    def test_get_fwrule(self):
        fwrule = self.client.get_firewall_rule(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'],
            firewall_rule_id=self.fwrule2['id'])

        self.assertEqual(fwrule['type'], 'firewall-rule')
        self.assertEqual(fwrule['id'], self.fwrule2['id'])
        self.assertEqual(fwrule['properties']['name'], self.fwrule2['properties']['name'])

    def test_delete_fwrule(self):
        fwrule = self.client.delete_firewall_rule(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'],
            firewall_rule_id=self.fwrule['id'])

        self.assertTrue(fwrule)

    def test_update_fwrule(self):
        fwrule = self.client.update_firewall_rule(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'],
            firewall_rule_id=self.fwrule2['id'],
            name="updated name")

        self.assertEqual(fwrule['type'], 'firewall-rule')
        self.assertEqual(fwrule['properties']['name'], "updated name")

    def test_create_fwrule(self):
        self.assertEqual(self.fwrule['type'], 'firewall-rule')
        self.assertEqual(self.fwrule['properties']['name'], self.resource['fwrule']['name'])

if __name__ == '__main__':
    unittest.main()
