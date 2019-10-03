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

from ionosenterprise.client import IonosEnterpriseService, Datacenter, Volume
from ionosenterprise.errors import ICError, ICNotAuthorizedError, ICNotFoundError, ICValidationError

from helpers import configuration
from helpers.resources import resource


class TestErrors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['datacenter']))

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])

    def test_ic_not_found(self):
        try:
            self.client.get_datacenter("fake_id")
        except ICError as err:
            self.assertTrue(isinstance(err, ICNotFoundError))

    def test_ic_unauthorized_error(self):
        try:
            self.client = IonosEnterpriseService(
                username=configuration.USERNAME + "1",
                password=configuration.PASSWORD,
                headers=configuration.HEADERS)
            self.client.list_datacenters()

        except ICError as err:
            self.assertTrue(isinstance(err, ICNotAuthorizedError))

    def test_ic_validation_error(self):
        try:
            i = Volume(
                name='Explicitly created volume',
                size=5,
                disk_type='HDD',
                image='fake_image_id',
                bus='VIRTIO')
            self.client.create_volume(datacenter_id=self.datacenter['id'], volume=i)
        except ICError as err:
            self.assertTrue(isinstance(err, ICValidationError))


if __name__ == '__main__':
    unittest.main()
