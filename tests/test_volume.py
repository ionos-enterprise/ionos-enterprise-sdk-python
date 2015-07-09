import unittest

from profitbricks.client import ProfitBricksService, Volume

volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
snapshot_id = '7df81087-5835-41c6-a10b-3e098593bba4'


class TestVolume(unittest.TestCase):
    def setUp(self):
        self.volume = ProfitBricksService(
            username='username', password='password')

    def test_list_volumes(self):
        volumes = self.volume.list_volumes(
            datacenter_id=datacenter_id)

        self.assertEqual(len(volumes), 4)
        self.assertEqual(volumes['items'][0]['id'], volume_id)
        self.assertEqual(volumes['items'][0]['properties']['name'], 'my boot volume for server 1')
        self.assertEqual(volumes['items'][0]['properties']['size'], 80)
        self.assertEqual(volumes['items'][0]['properties']['licenceType'], 'WINDOWS')
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
        self.assertEqual(volumes['items'][0]['properties']['bus'], 'VIRTIO')
        self.assertEqual(volumes['items'][0]['properties']['type'], 'HDD')

    def test_get_volume(self):
        volume = self.volume.get_volume(
            datacenter_id=datacenter_id,
            volume_id=volume_id)

        self.assertEqual(volume['properties']['name'], 'my boot volume for server 1')
        self.assertEqual(volume['properties']['size'], 80)
        self.assertEqual(volume['properties']['licenceType'], 'WINDOWS')
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
        self.assertEqual(volume['properties']['bus'], 'VIRTIO')
        self.assertEqual(volume['properties']['type'], 'HDD')

    def test_delete_volume(self):
        volume = self.volume.delete_volume(
            datacenter_id=datacenter_id,
            volume_id=volume_id)

        self.assertTrue(volume)

    def test_update_volume(self):
        volume = self.volume.update_volume(
            datacenter_id=datacenter_id,
            volume_id=volume_id,
            size=100,
            name='Resized storage to 100 GB',
            cpu_hot_unplug=True)

        self.assertEqual(
            volume['properties']['name'], 'Resized storage to 100 GB')
        self.assertEqual(volume['properties']['size'], 100)

    def test_create_volume(self):
        i = Volume(
            name='Explicitly created volume',
            size=56,
            image='<IMAGE/SNAPSHOT-ID>',
            bus='VIRTIO')

        response = self.volume.create_volume(
            datacenter_id=datacenter_id, volume=i)

        self.assertEqual(
            response['properties']['name'], 'my boot volume for server 1')
        self.assertEqual(response['properties']['size'], 80)
        self.assertEqual(response['properties']['licenceType'], 'WINDOWS')
        self.assertFalse(response['properties']['cpuHotPlug'])
        self.assertFalse(response['properties']['cpuHotUnplug'])
        self.assertFalse(response['properties']['ramHotPlug'])
        self.assertFalse(response['properties']['ramHotUnplug'])
        self.assertFalse(response['properties']['nicHotPlug'])
        self.assertFalse(response['properties']['nicHotUnplug'])
        self.assertFalse(response['properties']['discVirtioHotPlug'])
        self.assertFalse(response['properties']['discVirtioHotUnplug'])
        self.assertFalse(response['properties']['discScsiHotPlug'])
        self.assertFalse(response['properties']['discScsiHotUnplug'])
        self.assertEqual(response['properties']['bus'], 'VIRTIO')
        self.assertEqual(response['properties']['type'], 'HDD')

    def test_create_optional_value(self):
        i = Volume(
            name='Explicitly created volume',
            size=56,
            image='<IMAGE/SNAPSHOT-ID>',
            bus='VIRTIO',
            ram_hot_plug=True,
            cpu_hot_unplug=True)

        response = self.volume.create_volume(
            datacenter_id=datacenter_id, volume=i)

        self.assertEqual(
            response['properties']['name'], 'my boot volume for server 1')
        self.assertEqual(response['properties']['size'], 80)
        self.assertEqual(response['properties']['licenceType'], 'WINDOWS')
        self.assertFalse(response['properties']['cpuHotPlug'])
        self.assertFalse(response['properties']['cpuHotUnplug'])
        self.assertFalse(response['properties']['ramHotPlug'])
        self.assertFalse(response['properties']['ramHotUnplug'])
        self.assertFalse(response['properties']['nicHotPlug'])
        self.assertFalse(response['properties']['nicHotUnplug'])
        self.assertFalse(response['properties']['discVirtioHotPlug'])
        self.assertFalse(response['properties']['discVirtioHotUnplug'])
        self.assertFalse(response['properties']['discScsiHotPlug'])
        self.assertFalse(response['properties']['discScsiHotUnplug'])
        self.assertEqual(response['properties']['bus'], 'VIRTIO')
        self.assertEqual(response['properties']['type'], 'HDD')

    def test_create_snapshot(self):
        volume = self.volume.create_snapshot(
            datacenter_id=datacenter_id,
            volume_id=volume_id,
            name='<URLENCODED_SNAPSHOT_NAME>',
            description='<URLENCODED_SNAPSHOT_DESCRIPTION>')

        self.assertEqual(volume['id'], snapshot_id)
        self.assertEqual(
            volume['properties']['name'],
            'Snapshot of storage X on 12.12.12 12:12:12 - updated')
        self.assertEqual(volume['properties']['description'],
                         'description of a snapshot - updated')
        self.assertEqual(volume['properties']['location'], 'de/fkb')
        self.assertEqual(volume['properties']['size'], 28)
        self.assertEqual(volume['properties']['licenceType'], 'WINDOWS')
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

    def test_restore_snapshot(self):
        response = self.volume.restore_snapshot(
            datacenter_id=datacenter_id,
            volume_id=volume_id,
            snapshot_id=snapshot_id)

        self.assertTrue(response)

    def test_remove_snapshot(self):
        volume = self.volume.remove_snapshot(snapshot_id=snapshot_id)

        self.assertTrue(volume)

if __name__ == '__main__':
    unittest.main()
