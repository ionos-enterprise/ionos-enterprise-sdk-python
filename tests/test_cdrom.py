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
import warnings

from helpers import configuration
from helpers.resources import resource

from ionosenterprise.client import Datacenter, IonosEnterpriseService, Server


class TestCdrom(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        cls.datacenter = cls.client.create_datacenter(Datacenter(**cls.resource['datacenter']))
        cls.client.wait_for_completion(cls.datacenter)

        # Create test server.
        cls.server = cls.client.create_server(cls.datacenter['id'], Server(**cls.resource['server']))
        cls.client.wait_for_completion(cls.server)

        # Use an image ID for CDROM
        images = cls.client.list_images()['items']
        images = list(filter(lambda v: v['properties']['location'] == cls.resource['datacenter']['location']
                             and v['properties']['imageType'] != 'HDD',
                             images))
        cls.image_id = images[0]['id']
        cls.attached_cdrom = cls.client.attach_cdrom(cls.datacenter['id'], cls.server['id'], cls.image_id)
        cls.client.wait_for_completion(cls.attached_cdrom)

    @classmethod
    def tearDownClass(cls):
        cls.client.detach_cdrom(cls.datacenter['id'], cls.server['id'], cls.image_id)
        cls.client.delete_server(cls.datacenter['id'], cls.server['id'])
        cls.client.delete_datacenter(cls.datacenter['id'])

    def test_get_attached_cdroms(self):
        response = self.client.get_attached_cdroms(self.datacenter['id'], self.server['id'])
        self.assertGreater(len(response['items']), 0)

    def test_get_attached_cdrom(self):
        response = self.client.get_attached_cdrom(self.datacenter['id'], self.server['id'], self.image_id)
        self.assertEqual(response['id'], self.image_id)
