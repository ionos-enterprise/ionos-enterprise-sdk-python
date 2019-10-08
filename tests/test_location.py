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


class TestLocation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

    def test_list_locations(self):
        locations = self.client.list_locations()

        self.assertEqual(len(locations), 4)
        for location in locations['items']:
            self.assertEqual(location['type'], 'location')
            self.assertIn(location['id'], self.resource['locations'])

    def test_get_location(self):
        location = self.client.get_location(configuration.LOCATION)

        self.assertEqual(location['type'], 'location')
        self.assertEqual(location['id'], configuration.LOCATION)

    def test_get_failure(self):
        try:
            self.client.get_location(location_id='00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
