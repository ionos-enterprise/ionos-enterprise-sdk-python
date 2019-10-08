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
import time

from six import assertRegex

from ionosenterprise.client import Datacenter, IonosEnterpriseService, Server, Volume
from ionosenterprise.errors import ICError, ICNotFoundError

from helpers import configuration
from helpers.resources import resource


class TestDatacenter(unittest.TestCase):
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

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])

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
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            datacenter = Datacenter(name=self.resource['datacenter']['name'])
            self.client.create_datacenter(datacenter)
        except ICError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'location',
                          e.content[0]['message'])

    def test_remove_datacenter(self):
        datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))
        self.client.wait_for_completion(datacenter)

        response = self.client.delete_datacenter(
            datacenter_id=datacenter['id'])

        self.assertTrue(response)
        assertRegex(self, response['requestId'], self.resource['uuid_match'])

    def test_update_datacenter(self):
        datacenter = self.client.update_datacenter(
            datacenter_id=self.datacenter['id'],
            description=self.resource['datacenter']['name']+' - RENAME')
        self.client.wait_for_completion(datacenter)
        time.sleep(10)
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
        self.client.wait_for_completion(datacenter)

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
        self.client.wait_for_completion(datacenter)

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
