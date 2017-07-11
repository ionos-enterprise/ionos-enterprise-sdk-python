# Copyright 2015-2017 ProfitBricks GmbH
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

from helpers import configuration
from helpers.resources import resource, wait_for_completion, find_image
from profitbricks.client import Datacenter, Volume
from profitbricks.client import ProfitBricksService
from profitbricks.errors import PBError, PBNotFoundError
from six import assertRegex


class TestVolume(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter
        self.datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))
        wait_for_completion(self.client, self.datacenter, 'create_datacenter')

        self.image = find_image(self.client, configuration.IMAGE_NAME)

        # Create test volume
        vol = Volume(**self.resource['volume2'])
        vol.image = self.image['id']

        self.volume = self.client.create_volume(
            datacenter_id=self.datacenter['id'],
            volume=vol)
        wait_for_completion(self.client, self.volume, 'create_volume')

        # Create snapshot1
        self.snapshot1 = self.client.create_snapshot(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'],
            name=self.resource['snapshot']['name'],
            description=self.resource['snapshot']['description'])
        wait_for_completion(self.client, self.snapshot1, 'create_snapshot1',
                            wait_timeout=600)

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

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
        wait_for_completion(self.client, volume, 'create_volume')

        volume = self.client.delete_volume(
            datacenter_id=self.datacenter['id'],
            volume_id=volume['id'])

        self.assertTrue(volume)

    def test_update_volume(self):
        volume = self.client.update_volume(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'],
            size=6,
            name=self.resource['volume2']['name'] + ' - RENAME')
        wait_for_completion(self.client, volume, 'update_volume')

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
        self.assertIsNone(self.snapshot1['properties']['licenceType'])

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
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            volume = Volume(name=self.resource['volume2']['name'])
            self.client.create_volume(datacenter_id=self.datacenter['id'], volume=volume)
        except PBError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'size',
                          e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
