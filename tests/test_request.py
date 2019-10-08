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

from ionosenterprise.client import IonosEnterpriseService
from ionosenterprise.errors import ICNotFoundError

from helpers import configuration
from helpers.resources import resource


class TestRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        cls.requests = cls.client.list_requests()
        cls.request = cls.requests['items'][0]

    def test_list_requests(self):
        requests = self.client.list_requests()

        self.assertGreater(len(requests), 0)
        self.assertEqual(requests['items'][0]['type'], 'request')

    def test_get_request(self):
        request = self.client.get_request(request_id=self.request['id'], status=False)

        self.assertEqual(request['type'], 'request')
        self.assertEqual(request['id'], self.request['id'])
        self.assertEqual(request['href'], self.request['href'])

    def test_get_request_status(self):
        request = self.client.get_request(request_id=self.request['id'], status=True)

        self.assertEqual(request['type'], 'request-status')
        self.assertEqual(request['id'], self.request['id'] + '/status')
        self.assertEqual(request['href'], self.request['href'] + '/status')

    def test_get_failure(self):
        try:
            self.client.get_request(request_id='00000000-0000-0000-0000-000000000000',
                                    status=False)
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
