import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Volume, Snapshot


class TestLan(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        self.datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))
        wait_for_completion(self.client, self.datacenter, 'create_datacenter')

        # Create test volume
        volume = Volume(**self.resource['volume'])
        self.volume = self.client.create_volume(
            datacenter_id=self.datacenter['id'],
            volume=volume
        )

        wait_for_completion(self.client, self.volume, 'create_volume')

        # Create test volume1
        volume1 = Volume(**self.resource['volume'])
        self.volume1 = self.client.create_volume(
            datacenter_id=self.datacenter['id'],
            volume=volume1
        )

        wait_for_completion(self.client, self.volume1, 'create_volume1')

        # Create test snapshot1
        snapshot = Snapshot(**self.resource['snapshot'])
        self.snapshot1 = self.client.create_snapshot(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'],
            name=snapshot.name,
            description=snapshot.description)

        wait_for_completion(self.client, self.snapshot1, 'create_snapshot1')

        # Create test snapshot2
        self.snapshot2 = self.client.create_snapshot(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'],
            name="python sdk test volume",
            description="volume test description")

        wait_for_completion(self.client, self.snapshot2, 'create_snapshot2')

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_list_snapshots(self):
        snapshots = self.client.list_snapshots()

        self.assertGreater(len(snapshots), 0)
        self.assertEqual(snapshots['items'][0]['type'], 'snapshot')

    def test_get_snapshot(self):
        snapshot = self.client.get_snapshot(snapshot_id=self.snapshot1['id'])

        self.assertEqual(snapshot['type'], 'snapshot')
        self.assertEqual(snapshot['id'], self.snapshot1['id'])
        self.assertEqual(snapshot['properties']['name'], self.resource['snapshot']['name'])
        self.assertTrue(snapshot['properties']['description'],
                        self.resource['snapshot']['description'])

    def test_delete_snapshot(self):
        snapshot = self.client.delete_snapshot(snapshot_id=self.snapshot2['id'])

        self.assertTrue(snapshot)

    def test_update_snapshot(self):
        snapshot = self.client.update_snapshot(
            snapshot_id=self.snapshot1['id'],
            name=self.resource['snapshot']['name'] + ' RENAME',
            description=self.resource['snapshot']['description'] + ' RENAME')

        self.assertEqual(snapshot['type'], 'snapshot')
        self.assertEqual(snapshot['properties']['name'],
                         self.resource['snapshot']['name'] + ' RENAME')
        self.assertEqual(snapshot['properties']['description'],
                         self.resource['snapshot']['description'] + ' RENAME')

    def test_create_snapshot(self):
        self.assertEqual(self.snapshot1['type'], 'snapshot')
        self.assertEqual(self.snapshot1['properties']['name'],
                         self.resource['snapshot']['name'])
        self.assertEqual(self.snapshot1['properties']['description'],
                         self.resource['snapshot']['description'])


if __name__ == '__main__':
    unittest.main()
