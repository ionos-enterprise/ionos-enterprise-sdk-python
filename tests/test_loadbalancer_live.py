import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, LoadBalancer, LAN, NIC, Server


class TestLoadBalancer(unittest.TestCase):
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

        # Create test LoadBalancer
        loadbalancer=LoadBalancer(**self.resource['loadbalancer'])
        self.loadbalancer=self.client.create_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer=loadbalancer
        )

        wait_for_completion(self.client, self.loadbalancer, 'create_loadbalancer')

        # Create test LoadBalancer
        loadbalancer2 = LoadBalancer(**self.resource['loadbalancer'])
        loadbalancer2.name="Python SDK Test 2"
        self.loadbalancer2 = self.client.create_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer=loadbalancer2
        )

        wait_for_completion(self.client, self.loadbalancer2, 'create_loadbalancer2')

        # Create test LoadBalancer
        loadbalancer3 = LoadBalancer(**self.resource['loadbalancer'])
        loadbalancer3.name = "Python SDK Test 3"
        self.loadbalancer3 = self.client.create_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer=loadbalancer3
        )

        wait_for_completion(self.client, self.loadbalancer3, 'create_loadbalancer3')

        #Associate nic to loadbalancer
        self.associated_nic = self.client.add_loadbalanced_nics(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id'],
            nic_id=self.nic1['id'])

        wait_for_completion(self.client, self.associated_nic, 'associate_nic')

        # Associate nic to loadbalancer2
        self.associated_nic2 = self.client.add_loadbalanced_nics(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer2['id'],
            nic_id=self.nic1['id'])

        wait_for_completion(self.client, self.associated_nic2, 'associate_nic2')

        # Associate nic to loadbalancer3
        self.associated_nic3 = self.client.add_loadbalanced_nics(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer3['id'],
            nic_id=self.nic1['id'])

        wait_for_completion(self.client, self.associated_nic3, 'associate_nic3')

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_list_loadbalancers(self):
        loadbalancers = self.client.list_loadbalancers(
            datacenter_id=self.datacenter['id'])

        self.assertGreater(len(loadbalancers), 0)
        self.assertIn(loadbalancers['items'][0]['id'], (self.loadbalancer['id'], self.loadbalancer2['id'],self.loadbalancer3['id']))
        self.assertEqual(loadbalancers['items'][0]['type'], 'loadbalancer')

    def test_get_loadbalancer(self):
        loadbalancer = self.client.get_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id'])

        self.assertEqual(loadbalancer['type'], 'loadbalancer')
        self.assertEqual(loadbalancer['id'], self.loadbalancer['id'])
        self.assertEqual(loadbalancer['properties']['name'], self.loadbalancer['properties']['name'])

    def test_delete_loadbalancer(self):
        loadbalancer = self.client.delete_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer2['id'])

        self.assertTrue(loadbalancer)

    def test_update_loadbalancer(self):
        loadbalancer = self.client.update_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id'],
            name="updated name")

        self.assertEqual(loadbalancer['type'], 'loadbalancer')
        self.assertEqual(loadbalancer['properties']['name'], "updated name")

    def test_create_loadbalancer(self):
        self.assertEqual(self.loadbalancer['type'], 'loadbalancer')
        self.assertEqual(self.loadbalancer['properties']['name'], self.resource['loadbalancer']['name'])

    def test_associate_nic(self):
        associated_nic=self.client.get_loadbalanced_nic(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id'],
            nic_id=self.nic1['id'])


        self.assertEqual(associated_nic['id'], self.associated_nic['id'])
        self.assertEqual(associated_nic['properties']['name'], self.associated_nic['properties']['name'])

    def test_remove_nic(self):
        remove_nic=self.client.remove_loadbalanced_nic(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer3['id'],
            nic_id=self.nic1['id'])
        self.assertTrue(remove_nic)

    def test_list_balanced_nics(self):
        balanced_nics=self.client.get_loadbalancer_members(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id']
        )

        self.assertGreater(len(balanced_nics), 0)
        self.assertEqual(balanced_nics['items'][0]['id'], self.nic1['id'])
        self.assertEqual(balanced_nics['items'][0]['type'], 'nic')

    def test_get_balanced_nic(self):
        balanced_nic=self.client.get_loadbalanced_nic(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id'],
            nic_id=self.nic1['id'])

        self.assertEqual(balanced_nic['id'], self.nic1['id'])
        self.assertEqual(balanced_nic['type'], 'nic')

if __name__ == '__main__':
    unittest.main()
