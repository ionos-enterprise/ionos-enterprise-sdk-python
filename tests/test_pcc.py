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
import uuid

from ionosenterprise.client import IonosEnterpriseService, PrivateCrossConnect

from helpers import configuration
from helpers.resources import resource


class TestPcc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        pccModel1 = PrivateCrossConnect(name="TEST NAME 1", description="TEST DESCRIPTION 1")
        cls.pcc1 = cls.client.create_pcc(pccModel1)
        pccModel2 = PrivateCrossConnect(name="TEST NAME 2", description="TEST DESCRIPTION 2")
        cls.pcc2 = cls.client.create_pcc(pccModel2)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_pcc(cls.pcc1['id'])

    def test_list_pccs(self):
        pccs = self.client.list_pccs()
        self.assertGreater(len(pccs), 0)
        self.assertGreater(len(pccs['items']), 1)

    def test_get_pcc(self):
        pcc = self.client.get_pcc(self.pcc1['id'])
        self.assertTrue('id' in pcc)
        self.assertEqual(pcc['type'], 'pcc')

    def test_delete_pccs(self):
        response = self.client.delete_pcc(self.pcc2['id'])
        self.assertTrue('requestId' in response)

    def test_update_pcc(self):
        pcc = self.client.update_pcc(self.pcc1['id'], name="TEST NAME 1 - UPDATED", description="TEST DESCRIPTION 1 - UPDATED")
        self.assertEqual(pcc['properties']['name'], "TEST NAME 1 - UPDATED")
        self.assertEqual(pcc['properties']['description'], "TEST DESCRIPTION 1 - UPDATED")

