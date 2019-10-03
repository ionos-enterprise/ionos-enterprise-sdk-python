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

from ionosenterprise.client import Datacenter, IonosEnterpriseService, Volume
from ionosenterprise.errors import ICError, ICNotFoundError

from helpers import configuration
from helpers.resources import resource, find_image


class TestVolume(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['datacenter']))
        cls.client.wait_for_completion(cls.datacenter)

        cls.image = find_image(cls.client, configuration.IMAGE_NAME)

        # Create test volume
        vol = Volume(**cls.resource['volume2'])
        vol.image = cls.image['id']

        cls.volume = cls.client.create_volume(
            datacenter_id=cls.datacenter['id'],
            volume=vol)
        cls.client.wait_for_completion(cls.volume)

        # Create snapshot1
        cls.snapshot1 = cls.client.create_snapshot(
            datacenter_id=cls.datacenter['id'],
            volume_id=cls.volume['id'],
            name=cls.resource['snapshot']['name'],
            description=cls.resource['snapshot']['description'])
        cls.client.wait_for_completion(cls.snapshot1, timeout=600)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])

    def test_list_volumes(self):
        volumes = self.client.list_volumes(
            datacenter_id=self.datacenter['id'])

        self.assertGreater(len(volumes), 0)
        assertRegex(self, volumes['items'][0]['id'], self.resource['uuid_match'])
        self.assertEqual(volumes['items'][0]['type'], 'volume')
        self.assertEqual(volumes['items'][0]['properties']['name'],
                         self.resource['volume2']['name'])
        self.assertEqual(volumes['items'][0]['properties']['size'],
                         self.resource['volume2']['size'])
        self.assertEqual(volumes['items'][0]['properties']['type'],
                         self.resource['volume2']['disk_type'])
        self.assertIsNone(volumes['items'][0]['properties']['bus'])

    def test_get_volume(self):
        volume = self.client.get_volume(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'])

        self.assertEqual(volume['id'], self.volume['id'])
        self.assertEqual(volume['type'], 'volume')
        self.assertEqual(volume['properties']['name'], self.resource['volume2']['name'])
        self.assertEqual(volume['properties']['size'], self.resource['volume2']['size'])
        self.assertEqual(volume['properties']['licenceType'],
                         self.image['properties']['licenceType'])
        self.assertEqual(volume['properties']['type'], self.resource['volume2']['disk_type'])
        self.assertIsNone(volume['properties']['bus'])
        self.assertEqual(volume['properties']['availabilityZone'],
                         self.resource['volume2']['availability_zone'])

    def test_delete_volume(self):
        volume = self.client.create_volume(
            datacenter_id=self.datacenter['id'],
            volume=Volume(**self.resource['volume']))
        self.client.wait_for_completion(volume)

        volume = self.client.delete_volume(
            datacenter_id=self.datacenter['id'],
            volume_id=volume['id'])

        self.assertTrue(volume)
        assertRegex(self, volume['requestId'], self.resource['uuid_match'])

    def test_update_volume(self):
        volume = self.client.update_volume(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'],
            size=6,
            name=self.resource['volume2']['name'] + ' - RENAME')
        self.client.wait_for_completion(volume)

        volume = self.client.get_volume(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'])

        self.assertEqual(volume['id'], self.volume['id'])
        self.assertEqual(volume['properties']['name'],
                         self.resource['volume2']['name'] + ' - RENAME')
        self.assertEqual(volume['properties']['size'], 6)

    def test_create_volume(self):
        # Use volume created during volume test setup.
        assertRegex(self, self.volume['id'], self.resource['uuid_match'])
        self.assertEqual(self.volume['properties']['name'], self.resource['volume2']['name'])
        self.assertEqual(self.volume['properties']['bus'], self.resource['volume2']['bus'])
        self.assertEqual(self.volume['properties']['type'], self.resource['volume2']['disk_type'])
        self.assertEqual(self.volume['properties']['size'], self.resource['volume2']['size'])
        self.assertEqual(self.volume['properties']['sshKeys'],
                         self.resource['volume2']['ssh_keys'])
        self.assertEqual(self.volume['properties']['availabilityZone'],
                         self.resource['volume2']['availability_zone'])

    def test_create_snapshot(self):
        # Use snapshot created during volume test setup.
        self.assertEqual(self.snapshot1['type'], 'snapshot')
        self.assertEqual(self.snapshot1['properties']['name'], self.resource['snapshot']['name'])
        self.assertEqual(self.snapshot1['properties']['description'],
                         self.resource['snapshot']['description'])
        self.assertEqual(self.snapshot1['properties']['location'], configuration.LOCATION)
        self.assertIsNone(self.snapshot1['properties']['size'])
        self.assertEqual(self.snapshot1['properties']['licenceType'],
                         self.image['properties']['licenceType'])

    def test_restore_snapshot(self):
        response = self.client.restore_snapshot(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'],
            snapshot_id=self.snapshot1['id'])

        self.assertTrue(response)

    def test_remove_snapshot(self):
        volume = self.client.remove_snapshot(snapshot_id=self.snapshot1['id'])

        self.assertTrue(volume)

    def test_get_failure(self):
        try:
            self.client.get_volume(
                datacenter_id=self.datacenter['id'],
                volume_id='00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            volume = Volume(name=self.resource['volume2']['name'])
            self.client.create_volume(datacenter_id=self.datacenter['id'], volume=volume)
        except ICError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'size',
                          e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
