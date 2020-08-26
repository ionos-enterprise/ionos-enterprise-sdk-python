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

from ionosenterprise.client import IonosEnterpriseService, BackupUnit

from helpers import configuration
from helpers.resources import resource


class TestBackupunit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        backupunitModel1 = BackupUnit("TEST 1", password="TEST PASSWORD 1", email="TEST@TEST-EMAIL1.COM")
        cls.backupunit1 = cls.client.create_backupunit(backupunitModel1)
        backupunitModel2 = BackupUnit("TEST 2", password="TEST PASSWORD 2", email="TEST@TEST-EMAIL2.COM")
        cls.backupunit2 = cls.client.create_backupunit(backupunitModel2)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_backupunit(cls.backupunit1['id'])

    def test_list_backupunits(self):
        backupunits = self.client.list_backupunits()
        self.assertGreater(len(backupunits), 0)
        self.assertGreater(len(backupunits['items']), 1)

    def test_get_backupunit(self):
        backupunit = self.client.get_backupunit(self.backupunit1['id'])
        self.assertTrue('id' in backupunit)
        self.assertEqual(backupunit['type'], 'backupunit')

    def test_delete_backupunits(self):
        response = self.client.delete_backupunit(self.backupunit2['id'])
        self.assertTrue('requestId' in response)

    def test_update_backupunit(self):
        backupunit = self.client.update_backupunit(self.backupunit1['id'], email="TEST@TEST-EMAIL-UPDATED.COM")
        self.assertEqual(backupunit['properties']['email'], "TEST@TEST-EMAIL-UPDATED.COM")

    def test_update_backupunit_put(self):
        backupunit = self.client.update_backupunit_put(self.backupunit1['id'], email="TEST@TEST-EMAIL-UPDATED-PUT.COM")
        self.assertEqual(backupunit['properties']['email'], "TEST@TEST-EMAIL-UPDATED-PUT.COM")

    def test_get_ssourl(self):
        ssoUrl = self.client.get_ssourl(self.backupunit1['id'])
        self.assertTrue('ssoUrl' in ssoUrl)
