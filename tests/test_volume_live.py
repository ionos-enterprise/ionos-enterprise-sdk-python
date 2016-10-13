import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion, find_image
from profitbricks.client import Datacenter, Volume
from profitbricks.client import ProfitBricksService
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

        # Create test volume
        self.volume = self.client.create_volume(
            datacenter_id=self.datacenter['id'],
            volume=Volume(**self.resource['volume']))
        wait_for_completion(self.client, self.volume, 'create_volume')

        # Create snapshot1
        self.snapshot1 = self.client.create_snapshot(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'],
            name=self.resource['snapshot']['name'],
            description=self.resource['snapshot']['description'])
        wait_for_completion(self.client, self.snapshot1, 'create_snapshot1',
                            wait_timeout=600)

        self.image = find_image(self.client, configuration.IMAGE_NAME)

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_list_volumes(self):
        volumes = self.client.list_volumes(
            datacenter_id=self.datacenter['id'])

        self.assertGreater(len(volumes), 0)
        assertRegex(self, volumes['items'][0]['id'], self.resource['uuid_match'])
        self.assertEqual(volumes['items'][0]['type'], 'volume')
        self.assertEqual(volumes['items'][0]['properties']['name'], self.resource['volume']['name'])
        self.assertEqual(volumes['items'][0]['properties']['size'], self.resource['volume']['size'])
        self.assertEqual(volumes['items'][0]['properties']['licenceType'], self.resource['volume']['licence_type'])
        self.assertEqual(volumes['items'][0]['properties']['type'], self.resource['volume']['type'])
        self.assertFalse(volumes['items'][0]['properties']['cpuHotPlug'])
        self.assertFalse(volumes['items'][0]['properties']['cpuHotUnplug'])
        self.assertFalse(volumes['items'][0]['properties']['ramHotPlug'])
        self.assertFalse(volumes['items'][0]['properties']['ramHotUnplug'])
        self.assertFalse(volumes['items'][0]['properties']['nicHotPlug'])
        self.assertFalse(volumes['items'][0]['properties']['nicHotUnplug'])
        self.assertFalse(volumes['items'][0]['properties']['discVirtioHotPlug'])
        self.assertFalse(volumes['items'][0]['properties']['discVirtioHotUnplug'])
        self.assertFalse(volumes['items'][0]['properties']['discScsiHotPlug'])
        self.assertFalse(volumes['items'][0]['properties']['discScsiHotUnplug'])
        self.assertIsNone(volumes['items'][0]['properties']['bus'])

    def test_get_volume(self):
        volume = self.client.get_volume(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'])

        self.assertEqual(volume['id'], self.volume['id'])
        self.assertEqual(volume['type'], 'volume')
        self.assertEqual(volume['properties']['name'], self.resource['volume']['name'])
        self.assertEqual(volume['properties']['size'], self.resource['volume']['size'])
        self.assertEqual(volume['properties']['licenceType'], self.resource['volume']['licence_type'])
        self.assertEqual(volume['properties']['type'], self.resource['volume']['type'])
        self.assertFalse(volume['properties']['cpuHotPlug'])
        self.assertFalse(volume['properties']['cpuHotUnplug'])
        self.assertFalse(volume['properties']['ramHotPlug'])
        self.assertFalse(volume['properties']['ramHotUnplug'])
        self.assertFalse(volume['properties']['nicHotPlug'])
        self.assertFalse(volume['properties']['nicHotUnplug'])
        self.assertFalse(volume['properties']['discVirtioHotPlug'])
        self.assertFalse(volume['properties']['discVirtioHotUnplug'])
        self.assertFalse(volume['properties']['discScsiHotPlug'])
        self.assertFalse(volume['properties']['discScsiHotUnplug'])
        self.assertIsNone(volume['properties']['bus'])
        self.assertEqual(volume['properties']['availabilityZone'], self.resource["volume"]["availability_zone"])

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
            name=self.resource['volume']['name'] + ' RENAME')
        wait_for_completion(self.client, volume, 'update_volume')

        volume = self.client.get_volume(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'])

        self.assertEqual(volume['id'], self.volume['id'])
        self.assertEqual(volume['properties']['name'], self.resource['volume']['name'] + ' RENAME')
        self.assertEqual(volume['properties']['size'], 6)

    def test_create_volume(self):
        # Use volume created during volume test setup.
        self.assertEqual(self.volume['properties']['name'], self.resource['volume']['name'])
        self.assertEqual(self.volume['properties']['bus'], self.resource['volume']['bus'])
        self.assertEqual(self.volume['properties']['type'], self.resource['volume']['type'])
        self.assertEqual(self.volume['properties']['size'], self.resource['volume']['size'])
        self.assertEqual(self.volume['properties']['licenceType'], self.resource['volume']['licence_type'])
        self.assertFalse(self.volume['properties']['cpuHotPlug'])
        self.assertFalse(self.volume['properties']['cpuHotUnplug'])
        self.assertFalse(self.volume['properties']['ramHotPlug'])
        self.assertFalse(self.volume['properties']['ramHotUnplug'])
        self.assertFalse(self.volume['properties']['nicHotPlug'])
        self.assertFalse(self.volume['properties']['nicHotUnplug'])
        self.assertFalse(self.volume['properties']['discVirtioHotPlug'])
        self.assertFalse(self.volume['properties']['discVirtioHotUnplug'])
        self.assertFalse(self.volume['properties']['discScsiHotPlug'])
        self.assertFalse(self.volume['properties']['discScsiHotUnplug'])
        self.assertEqual(self.volume['properties']['availabilityZone'], self.resource["volume"]["availability_zone"])

    def test_create_snapshot(self):
        # Use snapshot created during volume test setup.
        self.assertEqual(self.snapshot1['type'], 'snapshot')
        self.assertEqual(self.snapshot1['properties']['name'], self.resource['snapshot']['name'])
        self.assertEqual(self.snapshot1['properties']['description'], self.resource['snapshot']['description'])
        self.assertEqual(self.snapshot1['properties']['location'], configuration.LOCATION)
        self.assertFalse(self.snapshot1['properties']['cpuHotPlug'])
        self.assertFalse(self.snapshot1['properties']['cpuHotUnplug'])
        self.assertFalse(self.snapshot1['properties']['ramHotPlug'])
        self.assertFalse(self.snapshot1['properties']['ramHotUnplug'])
        self.assertFalse(self.snapshot1['properties']['nicHotPlug'])
        self.assertFalse(self.snapshot1['properties']['nicHotUnplug'])
        self.assertFalse(self.snapshot1['properties']['discVirtioHotPlug'])
        self.assertFalse(self.snapshot1['properties']['discVirtioHotUnplug'])
        self.assertFalse(self.snapshot1['properties']['discScsiHotPlug'])
        self.assertFalse(self.snapshot1['properties']['discScsiHotUnplug'])
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

    def test_create_volume_failure(self):
        with self.assertRaises(Exception) as context:
            self.client.create_volume(
                datacenter_id=self.datacenter['id'],
                volume=Volume(image=self.image['id'],
                              **self.resource['volume_failure']))
        exception = ('Passwords/SSH Keys '
                     'are mandatory for public ProfitBricks Images.')

        self.assertIn(exception, str(context.exception))

if __name__ == '__main__':
    unittest.main()
