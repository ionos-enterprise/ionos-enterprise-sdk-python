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

from ionosenterprise.client import Datacenter, Volume, Snapshot, IonosEnterpriseService
from ionosenterprise.errors import ICNotFoundError

from helpers import configuration
from helpers.resources import resource


class TestSnapshot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['datacenter']))
        cls.client.wait_for_completion(cls.datacenter)

        # Create test volume
        volume = Volume(**cls.resource['volume'])
        cls.volume = cls.client.create_volume(
            datacenter_id=cls.datacenter['id'],
            volume=volume
        )

        cls.client.wait_for_completion(cls.volume)

        # Create test volume1
        volume1 = Volume(**cls.resource['volume'])
        cls.volume1 = cls.client.create_volume(
            datacenter_id=cls.datacenter['id'],
            volume=volume1
        )

        cls.client.wait_for_completion(cls.volume1)

        # Create test snapshot
        snapshot = Snapshot(**cls.resource['snapshot'])
        cls.snapshot1 = cls.client.create_snapshot(
            datacenter_id=cls.datacenter['id'],
            volume_id=cls.volume['id'],
            name=snapshot.name,
            description=snapshot.description)

        cls.client.wait_for_completion(cls.snapshot1)

        # Create test snapshot2
        cls.snapshot2 = cls.client.create_snapshot(
            datacenter_id=cls.datacenter['id'],
            volume_id=cls.volume['id'],
            name="python sdk test snapshot",
            description="snapshot test description")

        cls.client.wait_for_completion(cls.snapshot2)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_snapshot(snapshot_id=cls.snapshot1['id'])
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])

    def test_list_snapshots(self):
        snapshots = self.client.list_snapshots()

        self.assertGreater(len(snapshots['items']), 0)
        self.assertEqual(snapshots['items'][0]['type'], 'snapshot')

    def test_get_snapshot(self):
        snapshot = self.client.get_snapshot(snapshot_id=self.snapshot1['id'])

        self.assertEqual(snapshot['type'], 'snapshot')
        self.assertEqual(snapshot['id'], self.snapshot1['id'])
        self.assertEqual(snapshot['properties']['name'], self.resource['snapshot']['name'])
        self.assertTrue(snapshot['properties']['description'],
                        self.resource['snapshot']['description'])
        self.assertEqual(snapshot['properties']['location'], configuration.LOCATION)
        self.assertEqual(snapshot['properties']['size'], self.volume['properties']['size'])
        self.assertEqual(snapshot['properties']['cpuHotPlug'],
                         self.volume['properties']['cpuHotPlug'])
        self.assertEqual(snapshot['properties']['cpuHotUnplug'],
                         self.volume['properties']['cpuHotUnplug'])
        self.assertEqual(snapshot['properties']['ramHotPlug'],
                         self.volume['properties']['ramHotPlug'])
        self.assertEqual(snapshot['properties']['ramHotUnplug'],
                         self.volume['properties']['ramHotUnplug'])
        self.assertEqual(snapshot['properties']['nicHotPlug'],
                         self.volume['properties']['nicHotPlug'])
        self.assertEqual(snapshot['properties']['nicHotUnplug'],
                         self.volume['properties']['nicHotUnplug'])
        self.assertEqual(snapshot['properties']['discVirtioHotPlug'],
                         self.volume['properties']['discVirtioHotPlug'])
        self.assertEqual(snapshot['properties']['discVirtioHotUnplug'],
                         self.volume['properties']['discVirtioHotUnplug'])
        self.assertEqual(snapshot['properties']['discScsiHotPlug'],
                         self.volume['properties']['discScsiHotPlug'])
        self.assertEqual(snapshot['properties']['discScsiHotUnplug'],
                         self.volume['properties']['discScsiHotUnplug'])
        self.assertEqual(snapshot['properties']['licenceType'],
                         self.volume['properties']['licenceType'])

    def test_delete_snapshot(self):
        snapshot = self.client.delete_snapshot(snapshot_id=self.snapshot2['id'])

        self.assertTrue(snapshot)
        assertRegex(self, snapshot['requestId'], self.resource['uuid_match'])

    def test_update_snapshot(self):
        snapshot = self.client.update_snapshot(
            snapshot_id=self.snapshot1['id'],
            name=self.resource['snapshot']['name'] + ' - RENAME',
            description=self.resource['snapshot']['description'] + ' - RENAME')

        self.client.wait_for_completion(snapshot)

        self.assertEqual(snapshot['type'], 'snapshot')
        self.assertEqual(snapshot['properties']['name'],
                         self.resource['snapshot']['name'] + ' - RENAME')
        self.assertEqual(snapshot['properties']['description'],
                         self.resource['snapshot']['description'] + ' - RENAME')

    def test_create_snapshot(self):
        self.assertEqual(self.snapshot1['type'], 'snapshot')
        self.assertEqual(self.snapshot1['properties']['name'],
                         self.resource['snapshot']['name'])
        self.assertEqual(self.snapshot1['properties']['description'],
                         self.resource['snapshot']['description'])

    def test_get_failure(self):
        try:
            self.client.get_snapshot('00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_failure(self):
        try:
            self.client.create_snapshot(
                datacenter_id='00000000-0000-0000-0000-000000000000',
                volume_id=self.volume['id'],
                name=self.resource['snapshot']['name'])
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
