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

from ionosenterprise.client import IPBlock, IonosEnterpriseService
from ionosenterprise.errors import ICError, ICNotFoundError

from helpers import configuration
from helpers.resources import resource


class TestIPBlock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        ipblock1 = IPBlock(**cls.resource['ipblock'])
        ipblock1.size = 2
        cls.ipblock1 = cls.client.reserve_ipblock(ipblock1)

        ipblock2 = IPBlock(**cls.resource['ipblock'])
        cls.ipblock2 = cls.client.reserve_ipblock(ipblock2)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_ipblock(cls.ipblock1['id'])

    def test_list_ipblocks(self):
        ipblocks = self.client.list_ipblocks()

        assertRegex(self, ipblocks['items'][0]['id'], self.resource['uuid_match'])
        self.assertGreater(len(ipblocks['items']), 0)
        self.assertEqual(ipblocks['items'][0]['type'], 'ipblock')
        self.assertGreater(ipblocks['items'][0]['properties']['size'], 0)
        self.assertIn(ipblocks['items'][0]['properties']['location'], self.resource['locations'])

    def test_get_ipblock(self):
        ipblock = self.client.get_ipblock(self.ipblock1['id'])

        assertRegex(self, ipblock['id'], self.resource['uuid_match'])
        self.assertEqual(ipblock['id'], self.ipblock1['id'])
        self.assertEqual(ipblock['type'], 'ipblock')
        self.assertEqual(ipblock['properties']['name'], (self.resource['ipblock']['name']))
        self.assertEqual(ipblock['properties']['size'], 2)
        self.assertEqual(len(ipblock['properties']['ips']), 2)
        self.assertEqual(ipblock['properties']['location'], self.resource['ipblock']['location'])

    def test_delete_ipblock(self):
        ipblock = self.client.delete_ipblock(self.ipblock2['id'])

        self.assertTrue(ipblock)
        assertRegex(self, ipblock['requestId'], self.resource['uuid_match'])

    def test_reserve_ipblock(self):
        ipblock = self.client.reserve_ipblock(IPBlock(**self.resource['ipblock']))

        assertRegex(self, ipblock['id'], self.resource['uuid_match'])
        self.assertEqual(ipblock['properties']['name'], (self.resource['ipblock']['name']))
        self.assertEqual(ipblock['properties']['size'], self.resource['ipblock']['size'])
        self.assertEqual(ipblock['properties']['location'], self.resource['ipblock']['location'])

        self.client.delete_ipblock(ipblock['id'])

    def test_get_failure(self):
        try:
            self.client.get_ipblock('00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_reserve_failure(self):
        try:
            ipblock = IPBlock(name=self.resource['ipblock']['name'], size=1)
            self.client.reserve_ipblock(ipblock)
        except ICError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'location',
                          e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
