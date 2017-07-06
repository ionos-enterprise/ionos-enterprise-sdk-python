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
from helpers.resources import resource, wait_for_completion
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Server, LAN, NIC, FirewallRule
from profitbricks.errors import PBError, PBNotFoundError
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

        # Create test Firewall Rule
        fwrule = FirewallRule(**self.resource['fwrule'])
        self.fwrule = self.client.create_firewall_rule(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'],
            firewall_rule=fwrule)
        wait_for_completion(self.client, self.fwrule, 'create_fwrule')

        # Create test Firewall Rule 2
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
            firewall_rule_id=self.fwrule['id'])

        self.assertEqual(fwrule['type'], 'firewall-rule')
        self.assertEqual(fwrule['id'], self.fwrule['id'])
        assertRegex(self, fwrule['id'], self.resource['uuid_match'])
        self.assertEqual(fwrule['properties']['name'], self.fwrule['properties']['name'])
        self.assertEqual(fwrule['properties']['protocol'], self.fwrule['properties']['protocol'])
        self.assertEqual(fwrule['properties']['sourceMac'], self.fwrule['properties']['sourceMac'])
        self.assertIsNone(fwrule['properties']['sourceIp'])
        self.assertIsNone(fwrule['properties']['targetIp'])
        self.assertIsNone(fwrule['properties']['icmpCode'])
        self.assertIsNone(fwrule['properties']['icmpType'])
        self.assertEqual(fwrule['properties']['portRangeStart'],
                         self.fwrule['properties']['portRangeStart'])
        self.assertEqual(fwrule['properties']['portRangeEnd'],
                         self.fwrule['properties']['portRangeEnd'])

    def test_delete_fwrule(self):
        fwrule = self.client.delete_firewall_rule(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'],
            firewall_rule_id=self.fwrule2['id'])

        self.assertTrue(fwrule)

    def test_update_fwrule(self):
        fwrule = self.client.update_firewall_rule(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic_id=self.nic1['id'],
            firewall_rule_id=self.fwrule['id'],
            name=self.resource['fwrule']['name']+' - RENAME')

        self.assertEqual(fwrule['type'], 'firewall-rule')
        self.assertEqual(fwrule['properties']['name'],
                         self.resource['fwrule']['name']+' - RENAME')

    def test_create_fwrule(self):
        self.assertEqual(self.fwrule['type'], 'firewall-rule')
        self.assertEqual(self.fwrule['properties']['name'], self.resource['fwrule']['name'])
        self.assertEqual(self.fwrule['properties']['protocol'], self.resource['fwrule']['protocol'])
        self.assertEqual(self.fwrule['properties']['sourceMac'], self.resource['fwrule']['source_mac'])
        self.assertIsNone(self.fwrule['properties']['sourceIp'])
        self.assertIsNone(self.fwrule['properties']['targetIp'])
        self.assertIsNone(self.fwrule['properties']['icmpCode'])
        self.assertIsNone(self.fwrule['properties']['icmpType'])
        self.assertEqual(self.fwrule['properties']['portRangeStart'],
                         self.resource['fwrule']['port_range_start'])
        self.assertEqual(self.fwrule['properties']['portRangeEnd'],
                         self.resource['fwrule']['port_range_end'])

    def test_get_failure(self):
        try:
            self.client.get_firewall_rule(
                datacenter_id=self.datacenter['id'],
                server_id=self.server['id'],
                nic_id=self.nic1['id'],
                firewall_rule_id='00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            fwrule = FirewallRule(name=self.resource['fwrule']['name'])
            self.client.create_firewall_rule(
                datacenter_id=self.datacenter['id'],
                server_id=self.server['id'],
                nic_id=self.nic1['id'],
                firewall_rule=fwrule)
        except PBError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'protocol',
                          e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
