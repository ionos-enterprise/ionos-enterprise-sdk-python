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

import unittest

from six import assertRegex

from ionosenterprise.client import Datacenter, Server, LAN, NIC, IonosEnterpriseService, PrivateCrossConnect
from ionosenterprise.errors import ICNotFoundError

from helpers import configuration
from helpers.resources import resource

import uuid


class TestLan(unittest.TestCase):
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

        # Create pcc.
        pcc = PrivateCrossConnect(name="TEST NAME - %s" % uuid.uuid1(), description="TEST DESCRIPTION 1")

        cls.pcc = cls.client.create_pcc(pcc)
        cls.client.wait_for_completion(cls.pcc)

        # Create test LAN.
        lan_properties = cls.resource['lan']
        lan_properties['pcc_id'] = cls.pcc['id']
        cls.lan = cls.client.create_lan(
            datacenter_id=cls.datacenter['id'],
            lan=LAN(**lan_properties))
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
        nic2 = NIC(**cls.resource['nic'])
        nic2.lan = cls.lan['id']
        cls.nic2 = cls.client.create_nic(
            datacenter_id=cls.datacenter['id'],
            server_id=cls.server['id'],
            nic=nic2)
        cls.client.wait_for_completion(cls.nic2)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_nic(cls.datacenter['id'], cls.server['id'], cls.nic1['id'])
        cls.client.delete_nic(cls.datacenter['id'], cls.server['id'], cls.nic2['id'])
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])

    def test_list_lans(self):
        lans = self.client.list_lans(datacenter_id=self.datacenter['id'])

        self.assertGreater(len(lans), 0)
        self.assertEqual(lans['items'][0]['type'], 'lan')
        self.assertIn(lans['items'][0]['id'], ('1', '2', '3'))
        self.assertEqual(lans['items'][0]['properties']['name'], self.resource['lan']['name'])
        self.assertEqual(lans['items'][0]['properties']['public'], self.resource['lan']['public'])

    def test_get_lan(self):
        lan = self.client.get_lan(datacenter_id=self.datacenter['id'], lan_id=self.lan['id'])

        self.assertEqual(lan['type'], 'lan')
        self.assertEqual(lan['id'], self.lan['id'])
        self.assertEqual(lan['properties']['name'], self.resource['lan']['name'])
        self.assertEqual(lan['properties']['public'], self.resource['lan']['public'])

    def test_remove_lan(self):
        lan = self.client.create_lan(
            datacenter_id=self.datacenter['id'],
            lan=LAN(**self.resource['lan']))

        self.client.wait_for_completion(lan)

        lan = self.client.delete_lan(datacenter_id=self.datacenter['id'], lan_id=lan['id'])

        self.assertTrue(lan)
        assertRegex(self, lan['requestId'], self.resource['uuid_match'])

    def test_update_lan(self):
        lan = self.client.update_lan(
            datacenter_id=self.datacenter['id'],
            lan_id=self.lan['id'],
            name=self.resource['lan']['name'] + ' - RENAME',
            public=False)

        self.assertEqual(lan['type'], 'lan')
        self.assertEqual(lan['properties']['name'], self.resource['lan']['name'] + ' - RENAME')
        self.assertFalse(lan['properties']['public'])

    def test_create_lan(self):
        self.assertEqual(self.lan['id'], '1')
        self.assertEqual(self.lan['type'], 'lan')
        self.assertEqual(self.lan['properties']['name'], self.resource['lan']['name'])
        self.assertEqual(self.lan['properties']['public'], self.resource['lan']['public'])

    def test_create_complex_lan(self):
        nic_resource = NIC(**self.resource['nic'])

        nic1 = self.client.create_nic(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic=nic_resource)
        self.client.wait_for_completion(nic1)
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
        self.client.wait_for_completion(response)

        self.assertEqual(response['type'], 'lan')
        self.assertEqual(response['properties']['name'], self.resource['lan']['name'])
        self.assertFalse(response['properties']['public'])

    def test_get_lan_members(self):
        members = self.client.get_lan_members(
            datacenter_id=self.datacenter['id'],
            lan_id=self.lan['id'])

        self.assertGreater(len(members), 0)
        self.assertEqual(members['items'][0]['type'], 'nic')
        self.assertEqual(members['items'][0]['properties']['name'], self.resource['nic']['name'])
        assertRegex(self, members['items'][0]['properties']['mac'], self.resource['mac_match'])

    def test_get_failure(self):
        try:
            self.client.get_lan(datacenter_id=self.datacenter['id'], lan_id=0)
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            self.client.create_lan(
                datacenter_id='00000000-0000-0000-0000-000000000000', lan=LAN())
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
