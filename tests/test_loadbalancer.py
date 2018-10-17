# Copyright 2015-2017 ProfitBricks GmbH
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

import unittest

from helpers import configuration
from helpers.resources import resource
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, LoadBalancer, LAN, NIC, Server
from profitbricks.errors import PBError, PBNotFoundError
from six import assertRegex
from time import sleep


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
        self.client.wait_for_completion(self.datacenter)

        # Create test LAN.
        self.lan = self.client.create_lan(
            datacenter_id=self.datacenter['id'],
            lan=LAN(**self.resource['lan']))
        self.client.wait_for_completion(self.lan)

        # Create test server.
        self.server = self.client.create_server(
            datacenter_id=self.datacenter['id'],
            server=Server(**self.resource['server']))
        self.client.wait_for_completion(self.server)

        # Create test NIC1.
        nic1 = NIC(**self.resource['nic'])
        nic1.lan = self.lan['id']
        self.nic1 = self.client.create_nic(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic=nic1)
        self.client.wait_for_completion(self.nic1)

        # Create test NIC2.
        # nic2 = NIC(**self.resource['nic'])
        # nic2.lan = self.lan['id']
        # self.nic2 = self.client.create_nic(
        #     datacenter_id=self.datacenter['id'],
        #     server_id=self.server['id'],
        #     nic=nic2)
        # self.client.wait_for_completion(self.nic2)

        # Create test LoadBalancer
        loadbalancer = LoadBalancer(**self.resource['loadbalancer'])
        loadbalancer.balancednics = [self.nic1['id']]
        self.loadbalancer = self.client.create_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer=loadbalancer
        )

        self.client.wait_for_completion(self.loadbalancer)

        # Create test LoadBalancer2
        loadbalancer2 = LoadBalancer(**self.resource['loadbalancer'])
        loadbalancer2.name = "Python SDK Test 2"
        self.loadbalancer2 = self.client.create_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer=loadbalancer2
        )

        self.client.wait_for_completion(self.loadbalancer2)

        # Create test LoadBalancer3
        loadbalancer3 = LoadBalancer(**self.resource['loadbalancer'])
        loadbalancer3.balancednics = [self.nic1['id']]
        loadbalancer3.name = "Python SDK Test 3"
        self.loadbalancer3 = self.client.create_loadbalancer(
            datacenter_id=self.datacenter['id'],
            loadbalancer=loadbalancer3
        )

        self.client.wait_for_completion(self.loadbalancer3)

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

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
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            self.client.create_loadbalancer(
                datacenter_id=self.datacenter['id'],
                loadbalancer=LoadBalancer())
        except PBError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'lan',
                          e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
