# Copyright 2015-2017 IONOS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from time import sleep
import unittest

from six import assertRegex

from ionosenterprise.client import Datacenter, LoadBalancer, LAN, NIC, Server, IonosEnterpriseService
from ionosenterprise.errors import ICError, ICNotFoundError

from helpers import configuration
from helpers.resources import resource


class TestLoadBalancer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['datacenter']))
        cls.client.wait_for_completion(cls.datacenter)

        # Create test LAN.
        cls.lan = cls.client.create_lan(
            datacenter_id=cls.datacenter['id'],
            lan=LAN(**cls.resource['lan']))
        cls.client.wait_for_completion(cls.lan)

        # Create test server.
        cls.server = cls.client.create_server(
            datacenter_id=cls.datacenter['id'],
            server=Server(**cls.resource['server']))
        cls.client.wait_for_completion(cls.server)

        # Create test NIC1.
        nic1 = NIC(**cls.resource['nic'])
        nic1.lan = cls.lan['id']
        cls.nic1 = cls.client.create_nic(
            datacenter_id=cls.datacenter['id'],
            server_id=cls.server['id'],
            nic=nic1)
        cls.client.wait_for_completion(cls.nic1)

        # Create test NIC2.
        # nic2 = NIC(**cls.resource['nic'])
        # nic2.lan = cls.lan['id']
        # cls.nic2 = cls.client.create_nic(
        #     datacenter_id=cls.datacenter['id'],
        #     server_id=cls.server['id'],
        #     nic=nic2)
        # cls.client.wait_for_completion(cls.nic2)

        # Create test LoadBalancer
        loadbalancer = LoadBalancer(**cls.resource['loadbalancer'])
        loadbalancer.balancednics = [cls.nic1['id']]
        cls.loadbalancer = cls.client.create_loadbalancer(
            datacenter_id=cls.datacenter['id'],
            loadbalancer=loadbalancer
        )

        cls.client.wait_for_completion(cls.loadbalancer)

        # Create test LoadBalancer2
        loadbalancer2 = LoadBalancer(**cls.resource['loadbalancer'])
        loadbalancer2.name = "Python SDK Test 2"
        cls.loadbalancer2 = cls.client.create_loadbalancer(
            datacenter_id=cls.datacenter['id'],
            loadbalancer=loadbalancer2
        )

        cls.client.wait_for_completion(cls.loadbalancer2)

        # Create test LoadBalancer3
        loadbalancer3 = LoadBalancer(**cls.resource['loadbalancer'])
        loadbalancer3.balancednics = [cls.nic1['id']]
        loadbalancer3.name = "Python SDK Test 3"
        cls.loadbalancer3 = cls.client.create_loadbalancer(
            datacenter_id=cls.datacenter['id'],
            loadbalancer=loadbalancer3
        )

        cls.client.wait_for_completion(cls.loadbalancer3)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])

    def test_list_loadbalancers(self):
        loadbalancers = self.client.list_loadbalancers(
            datacenter_id=self.datacenter['id'])

        self.assertGreater(len(loadbalancers), 0)
        self.assertIn(loadbalancers['items'][0]['id'],
                      (self.loadbalancer['id'],
                       self.loadbalancer2['id'],
                       self.loadbalancer3['id']))
        self.assertEqual(loadbalancers['items'][0]['type'], 'loadbalancer')

    def test_get_loadbalancer(self):
        loadbalancer = self.client.get_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id'])

        self.assertEqual(loadbalancer['type'], 'loadbalancer')
        self.assertEqual(loadbalancer['id'], self.loadbalancer['id'])
        assertRegex(self, loadbalancer['id'], self.resource['uuid_match'])
        self.assertEqual(loadbalancer['properties']['name'],
                         self.loadbalancer['properties']['name'])
        self.assertEqual(loadbalancer['properties']['dhcp'],
                         self.loadbalancer['properties']['dhcp'])
        self.assertIsNotNone(loadbalancer['properties']['ip'])

    def test_delete_loadbalancer(self):
        loadbalancer = self.client.delete_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer2['id'])

        self.assertTrue(loadbalancer)
        assertRegex(self, loadbalancer['requestId'], self.resource['uuid_match'])

    def test_update_loadbalancer(self):
        loadbalancer = self.client.update_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id'],
            name=self.resource['loadbalancer']['name']+' - RENAME')

        self.assertEqual(loadbalancer['type'], 'loadbalancer')
        self.assertEqual(loadbalancer['properties']['name'],
                         self.resource['loadbalancer']['name']+' - RENAME')

    def test_create_loadbalancer(self):
        self.assertEqual(self.loadbalancer['type'], 'loadbalancer')
        self.assertIsNotNone(self.loadbalancer['entities']['balancednics'])
        self.assertEqual(self.loadbalancer['properties']['name'],
                         self.resource['loadbalancer']['name'])
        self.assertEqual(self.loadbalancer['properties']['dhcp'],
                         self.resource['loadbalancer']['dhcp'])

    def test_associate_nic(self):
        associated_nic = self.client.add_loadbalanced_nics(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer2['id'],
            nic_id=self.nic1['id'])

        self.client.wait_for_completion(associated_nic)

        self.assertEqual(associated_nic['id'], self.nic1['id'])
        self.assertEqual(associated_nic['properties']['name'],
                         self.nic1['properties']['name'])

    def test_remove_nic(self):
        remove_nic = self.client.remove_loadbalanced_nic(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer3['id'],
            nic_id=self.nic1['id'])
        self.assertTrue(remove_nic)
        sleep(30)

    def test_list_balanced_nics(self):
        balanced_nics = self.client.get_loadbalancer_members(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id']
        )

        self.assertGreater(len(balanced_nics['items']), 0)
        self.assertEqual(balanced_nics['items'][0]['id'], self.nic1['id'])
        self.assertEqual(balanced_nics['items'][0]['type'], 'nic')

    def test_get_balanced_nic(self):
        balanced_nic = self.client.get_loadbalanced_nic(
            datacenter_id=self.datacenter['id'],
            loadbalancer_id=self.loadbalancer['id'],
            nic_id=self.nic1['id'])

        self.assertEqual(balanced_nic['id'], self.nic1['id'])
        self.assertEqual(balanced_nic['type'], 'nic')
        self.assertEqual(balanced_nic['properties']['name'], self.nic1['properties']['name'])
        self.assertEqual(balanced_nic['properties']['dhcp'], self.nic1['properties']['dhcp'])
        self.assertIsInstance(balanced_nic['properties']['nat'], bool)
        self.assertIsInstance(balanced_nic['properties']['firewallActive'], bool)
        self.assertGreater(len(balanced_nic['properties']['ips']), 0)
        self.assertIsInstance(balanced_nic['properties']['lan'], int)
        assertRegex(self, balanced_nic['properties']['mac'], self.resource['mac_match'])

    def test_get_failure(self):
        try:
            self.client.get_loadbalancer(
                datacenter_id=self.datacenter['id'],
                loadbalancer_id='00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            self.client.create_loadbalancer(
                datacenter_id=self.datacenter['id'],
                loadbalancer=LoadBalancer())
        except ICError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'lan',
                          e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
