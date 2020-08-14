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

from ionosenterprise.client import IonosEnterpriseService, User

from helpers import configuration
from helpers.resources import resource


class TestS3key(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        user = User(
            firstname="TEST FIRST NAME",
            lastname="TEST FIRST NAME",
            email="%s@TEST-EMAIL.COM" % uuid.uuid1(),
            password="TEST PASSWORD"
        )
        # Create user
        cls.user = cls.client.create_user(user)
        cls.client.wait_for_completion(cls.user)
        # Create test s3keys.
        cls.s3key1 = cls.client.create_s3key(cls.user['id'])
        cls.s3key2 = cls.client.create_s3key(cls.user['id'])


    @classmethod
    def tearDownClass(cls):
        cls.client.delete_s3key(cls.user['id'], cls.s3key1['id'])
        cls.client.delete_user(cls.user['id'])

    def test_list_s3keys(self):
        s3keys = self.client.list_s3keys(self.user['id'])
        self.assertGreater(len(s3keys), 0)
        self.assertEqual(len(s3keys['items']), 2) # one inactive key is created when user is created

    def test_get_s3key(self):
        s3key = self.client.get_s3key(self.user['id'], self.s3key1['id'])
        self.assertTrue('id' in s3key)
        self.assertEqual(s3key['type'], 's3key')

    def test_delete_s3keys(self):
        response = self.client.delete_s3key(self.user['id'], self.s3key2['id'])
        self.assertTrue('requestId' in response)

    def test_update_s3key(self):
        s3key = self.client.update_s3key(
            self.user['id'], self.s3key1['id'],
            active = False
        )
        self.assertFalse(s3key['properties']['active'])

    def test_get_s3ssourl(self):
        ssoUrl = self.client.get_s3ssourl(self.user['id'])
        self.assertTrue('ssoUrl' in ssoUrl)

