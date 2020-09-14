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
from ionosenterprise.items import Group
from six import assertRegex

from ionosenterprise.client import Datacenter, IonosEnterpriseService, Server, Volume
from ionosenterprise.errors import ICError, ICNotFoundError

from helpers import configuration
from helpers.resources import resource
import warnings

class TestGroup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        group_object = Group(**cls.resource['group'])
        cls.group = cls.client.create_group(group_object)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_group(cls.group['id'])

    def test_list_groups(self):
        response = self.client.list_groups()
        self.assertEqual('groups', response['id'])
        self.assertGreater(len(response['items']), 0)

    def test_get_group(self):
        response = self.client.get_group(self.group['id'])
        self.assertEqual('group', response['type'])
        self.assertEqual(self.group['id'], response['id'])

    def test_update_group(self):
        new_name = "NEW_NAME"
        response = self.client.update_group(self.group['id'], name=new_name)
        self.assertEqual(response['properties']['name'], new_name)