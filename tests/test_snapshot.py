import unittest

from profitbricks.client import ProfitBricksService

snapshot_id = '7df81087-5835-41c6-a10b-3e098593bba4'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'


class TestServer(unittest.TestCase):
    def setUp(self):
        self.snapshot = ProfitBricksService(
            username='username', password='password')

    def test_list_snapshots(self):
        snapshots = self.snapshot.list_snapshots()

        self.assertEqual(len(snapshots), 4)
        self.assertEqual(snapshots['items'][0]['id'], snapshot_id)
        self.assertEqual(
            snapshots['items'][0]['properties']['name'],
            'Snapshot of storage X on 12.12.12 12:12:12')

        self.assertEqual(
            snapshots['items'][0]['properties']['description'],
            'description of a snapshot')

        self.assertEqual(
            snapshots['items'][0]['properties']['location'], 'de/fkb')

        self.assertEqual(
            snapshots['items'][0]['properties']['size'], 28)

    def test_get_snapshot(self):
        snapshot = self.snapshot.get_snapshot(
            snapshot_id=snapshot_id)

        self.assertEqual(snapshot['id'], snapshot_id)
        self.assertEqual(
            snapshot['properties']['name'],
            'Snapshot of storage X on 12.12.12 12:12:12')

        self.assertEqual(
            snapshot['properties']['description'],
            'description of a snapshot')

        self.assertEqual(
            snapshot['properties']['location'], 'de/fkb')

        self.assertEqual(
            snapshot['properties']['size'], 28)

    def test_delete_snapshot(self):
        snapshot = self.snapshot.delete_snapshot(
            snapshot_id=snapshot_id)

        self.assertTrue(snapshot)

    def test_update_snapshot(self):
        snapshot = self.snapshot.update_snapshot(
            snapshot_id='7df81087-5835-41c6-a10b-3e098593bbd2',
            name='New name')

        self.assertEqual(snapshot['id'], '7df81087-5835-41c6-a10b-3e098593bbd2')
        self.assertEqual(snapshot['properties']['name'], 'New name')

        self.assertEqual(
            snapshot['properties']['description'],
            'description of a snapshot - updated')

        self.assertEqual(
            snapshot['properties']['location'], 'de/fkb')

        self.assertEqual(
            snapshot['properties']['size'], 28)

if __name__ == '__main__':
    unittest.main()
