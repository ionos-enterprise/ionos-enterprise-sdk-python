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

from ionosenterprise.client import Datacenter, Group, IonosEnterpriseService
from ionosenterprise.errors import ICError, ICNotFoundError

from helpers import configuration
from helpers.resources import resource, check_detached_cdrom_gone
import warnings

class TestShare(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['datacenter']))
        cls.client.wait_for_completion(cls.datacenter)

        # Create test group.
        cls.group = cls.client.create_group(Group(**cls.resource['group']))
        cls.client.wait_for_completion(cls.group)

        cls.share_1 = cls.client.add_share(cls.group['id'], cls.datacenter['id'])
        cls.client.wait_for_completion(cls.share_1)

        cls.share_2 = cls.client.add_share(cls.group['id'], cls.datacenter['id'])
        cls.client.wait_for_completion(cls.share_2)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_datacenter(cls.datacenter['id'])
        cls.client.delete_group(cls.group['id'])
        cls.client.delete_share(cls.share_1['id'])

    def test_list_shares(self):
        response = self.client.list_shares(self.group['id'])
        self.assertGreater(len(response['items']), 0)

    def test_get_share(self):
        response = self.client.get_share(self.group['id'], self.share_1['id'])
        self.assertEqual(response['type'], 'share')

    def test_update_share(self):
        response = self.client.update_share(self.group['id'], self.datacenter['id'], edit_privilege=True,
    share_privilege=True)
        self.assertEqual(response['properties']['edit_privilege'], True)
        self.assertEqual(response['properties']['share_privilege'], True)

    def test_delete_share(self):
        response = self.client.delete_share(self.group['id'], self.datacenter['id'])
        self.assertIn('request_id', response)

if __name__ == '__main__':
    unittest.main()
