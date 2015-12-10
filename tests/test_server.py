import unittest

from profitbricks.client import ProfitBricksService
from profitbricks.client import Server, NIC, Volume

server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = ProfitBricksService(
            username='username', password='password')

    def test_list_servers(self):
        servers = self.server.list_servers(datacenter_id=datacenter_id)

        self.assertEqual(len(servers), 4)
        self.assertEqual(servers['items'][0]['id'], server_id)
        self.assertEqual(servers['items'][0]['properties']['name'], 'New Server')
        self.assertEqual(servers['items'][0]['properties']['cores'], '4')
        self.assertEqual(servers['items'][0]['properties']['ram'], '4096')
        self.assertEqual(servers['items'][0]['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(servers['items'][0]['properties']['vmState'], 'SHUTOFF')
        self.assertEqual(servers['items'][0]['properties']['bootVolume'], None)
        self.assertEqual(servers['items'][0]['properties']['bootCdrom'], None)

    def test_get_server(self):
        server = self.server.get_server(
            datacenter_id=datacenter_id,
            server_id=server_id)

        self.assertEqual(server['id'], server_id)
        self.assertEqual(server['properties']['name'], 'New Server')
        self.assertEqual(server['properties']['cores'], '4')
        self.assertEqual(server['properties']['ram'], '4096')
        self.assertEqual(server['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(server['properties']['vmState'], 'SHUTOFF')
        self.assertEqual(server['properties']['bootVolume'], None)
        self.assertEqual(server['properties']['bootCdrom'], None)

    def test_delete_server(self):
        server = self.server.delete_server(
            datacenter_id=datacenter_id,
            server_id=server_id)

        self.assertTrue(server)

    def test_update_server(self):
        server = self.server.update_server(
            datacenter_id=datacenter_id,
            server_id=server_id,
            cores=16)

        self.assertEqual(server['id'], server_id)
        self.assertEqual(server['properties']['name'], 'server1 - updated')
        self.assertEqual(server['properties']['cores'], '16')
        self.assertEqual(server['properties']['ram'], '4096')
        self.assertEqual(server['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(server['properties']['bootVolume']['id'], '<ID-OF-ANOTHER-STORAGE>')
        self.assertEqual(server['properties']['bootCdrom'], None)

    def test_create_complex(self):
        nic1 = NIC(
            name='nic1',
            ips=['10.2.2.3'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            )

        nic2 = NIC(
            name='nic2',
            ips=['10.2.3.4'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            )

        volume1 = Volume(
            name='volume1',
            size=56,
            image='<IMAGE/SNAPSHOT-ID>',
            bus='VIRTIO'
            )

        volume2 = Volume(
            name='volume2',
            size=56,
            image='<IMAGE/SNAPSHOT-ID>',
            bus='VIRTIO'
            )

        nics = [nic1, nic2]
        create_volumes = [volume1, volume2]

        i = Server(
            name='server1',
            ram=4096,
            cores=4,
            nics=nics,
            create_volumes=create_volumes
            )

        response = self.server.create_server(
            datacenter_id=datacenter_id, server=i)

        self.assertEqual(response['id'], server_id)
        self.assertEqual(response['properties']['name'], 'New Server')
        self.assertEqual(response['properties']['cores'], '4')
        self.assertEqual(response['properties']['ram'], '4096')
        self.assertEqual(
            response['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(response['properties']['vmState'], 'SHUTOFF')

    def test_create_with_existing_volume(self):

        volume_id = '<NEW-STORAGE-ID>'

        attach_volumes = [volume_id]

        i = Server(
            name='server1',
            ram=4096,
            cores=4,
            attach_volumes=attach_volumes
            )

        response = self.server.create_server(
            datacenter_id=datacenter_id, server=i)

        self.assertEqual(response['id'], server_id)
        self.assertEqual(response['properties']['name'], 'New Server')
        self.assertEqual(response['properties']['cores'], '4')
        self.assertEqual(response['properties']['ram'], '4096')
        self.assertEqual(
            response['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(response['properties']['vmState'], 'SHUTOFF')

    def test_create_with_volumes_only(self):
        volume1 = Volume(
            name='volume1',
            size=56,
            image='<IMAGE/SNAPSHOT-ID>',
            bus='VIRTIO'
            )

        volume2 = Volume(
            name='volume2',
            size=56,
            image='<IMAGE/SNAPSHOT-ID>',
            bus='VIRTIO'
            )

        create_volumes = [volume1, volume2]

        i = Server(
            name='server1',
            ram=4096,
            cores=4,
            create_volumes=create_volumes
            )

        response = self.server.create_server(
            datacenter_id=datacenter_id, server=i)

        self.assertEqual(response['id'], server_id)
        self.assertEqual(response['properties']['name'], 'New Server')
        self.assertEqual(response['properties']['cores'], '4')
        self.assertEqual(response['properties']['ram'], '4096')
        self.assertEqual(response['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(response['properties']['vmState'], 'SHUTOFF')

    def test_create_with_nics_only(self):
        nic1 = NIC(
            name='nic1',
            ips=['10.2.2.3'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            )

        nic2 = NIC(
            name='nic2',
            ips=['10.2.3.4'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            )

        nics = [nic1, nic2]

        i = Server(
            name='server1',
            ram=4096,
            cores=4,
            nics=nics
            )

        response = self.server.create_server(
            datacenter_id=datacenter_id, server=i)

        self.assertEqual(response['id'], server_id)
        self.assertEqual(response['properties']['name'], 'New Server')
        self.assertEqual(response['properties']['cores'], '4')
        self.assertEqual(response['properties']['ram'], '4096')
        self.assertEqual(response['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(response['properties']['vmState'], 'SHUTOFF')

    def test_create_simple(self):
        i = Server(
            name='server1',
            ram=4096,
            cores=4
            )

        response = self.server.create_server(
            datacenter_id=datacenter_id,
            server=i)

        self.assertEqual(response['id'], server_id)
        self.assertEqual(response['properties']['name'], 'New Server')
        self.assertEqual(response['properties']['cores'], '4')
        self.assertEqual(response['properties']['ram'], '4096')
        self.assertEqual(response['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(response['properties']['vmState'], 'SHUTOFF')

    def test_create_with_two_existing_volumes(self):
        volume_id1 = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
        volume_id2 = '800e1cab-99b2-4c30-ba8c-1d273ddba024'

        attach_volumes = [volume_id1, volume_id2]

        i = Server(
            name='server1',
            ram=4096,
            cores=4,
            attach_volumes=attach_volumes
            )

        response = self.server.create_server(
            datacenter_id=datacenter_id,
            server=i)

        self.assertEqual(response['id'], server_id)
        self.assertEqual(response['properties']['name'], 'New Server')
        self.assertEqual(response['properties']['cores'], '4')
        self.assertEqual(response['properties']['ram'], '4096')
        self.assertEqual(response['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(response['properties']['vmState'], 'SHUTOFF')

    def test_create_with_boot_volume(self):
        volume_id1 = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
        volume_id2 = '800e1cab-99b2-4c30-ba8c-1d273ddba024'
        boot_volume_id = '800e1cab-99b2-4c30-ba8c-1d273ddba024'

        attach_volumes = [volume_id1, volume_id2]

        i = Server(
            name='server1',
            ram=4096,
            cores=4,
            boot_volume_id=boot_volume_id,
            attach_volumes=attach_volumes
            )

        response = self.server.create_server(
            datacenter_id=datacenter_id,
            server=i)

        self.assertEqual(response['id'], server_id)
        self.assertEqual(response['properties']['name'], 'New Server')
        self.assertEqual(response['properties']['cores'], '4')
        self.assertEqual(response['properties']['ram'], '4096')
        self.assertEqual(response['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(response['properties']['vmState'], 'SHUTOFF')

    def test_create_with_nics_and_existing_volume(self):
        volume_id1 = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
        volume_id2 = '800e1cab-99b2-4c30-ba8c-1d273ddba024'
        boot_volume_id = '800e1cab-99b2-4c30-ba8c-1d273ddba024'

        attach_volumes = [volume_id1, volume_id2]

        nic1 = NIC(
            name='nic1',
            ips=['10.2.2.3'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            )

        nic2 = NIC(
            name='nic2',
            ips=['10.2.3.4'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            )

        nics = [nic1, nic2]

        i = Server(
            name='server1',
            ram=4096,
            cores=4,
            boot_volume_id=boot_volume_id,
            attach_volumes=attach_volumes,
            nics=nics
            )

        response = self.server.create_server(
            datacenter_id=datacenter_id,
            server=i)

        self.assertEqual(response['id'], server_id)
        self.assertEqual(response['properties']['name'], 'New Server')
        self.assertEqual(response['properties']['cores'], '4')
        self.assertEqual(response['properties']['ram'], '4096')
        self.assertEqual(response['properties']['availabilityZone'], 'ZONE_1')
        self.assertEqual(response['properties']['vmState'], 'SHUTOFF')

    def test_get_attached_volumes(self):
        servers = self.server.get_attached_volumes(
            datacenter_id=datacenter_id,
            server_id=server_id)

        self.assertEqual(len(servers), 4)
        self.assertEqual(servers['items'][0]['id'], '700e1cab-99b2-4c30-ba8c-1d273ddba025')
        self.assertEqual(servers['items'][0]['properties']['name'], 'my boot volume for server 1')
        self.assertEqual(servers['items'][0]['properties']['size'], 80)
        self.assertEqual(servers['items'][0]['properties']['bus'], 'VIRTIO')
        self.assertEqual(servers['items'][0]['properties']['image'], None)
        self.assertEqual(servers['items'][0]['properties']['imagePassword'], None)
        self.assertEqual(servers['items'][0]['properties']['type'], 'HDD')
        self.assertEqual(servers['items'][0]['properties']['licenceType'], 'WINDOWS')
        self.assertFalse(servers['items'][0]['properties']['cpuHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['cpuHotUnplug'])
        self.assertFalse(servers['items'][0]['properties']['ramHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['ramHotUnplug'])
        self.assertFalse(servers['items'][0]['properties']['nicHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['nicHotUnplug'])
        self.assertFalse(servers['items'][0]['properties']['discVirtioHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['discVirtioHotUnplug'])
        self.assertFalse(servers['items'][0]['properties']['discScsiHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['discScsiHotUnplug'])

    def test_get_attached_volume(self):
        volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'

        server = self.server.get_attached_volume(
            datacenter_id=datacenter_id,
            server_id=server_id,
            volume_id=volume_id)

        self.assertEqual(server['id'], volume_id)
        self.assertEqual(server['properties']['name'], 'my boot volume for server 1')
        self.assertEqual(server['properties']['size'], 80)
        self.assertEqual(server['properties']['bus'], 'VIRTIO')
        self.assertEqual(server['properties']['image'], None)
        self.assertEqual(server['properties']['imagePassword'], None)
        self.assertEqual(server['properties']['type'], 'HDD')
        self.assertEqual(server['properties']['licenceType'], 'WINDOWS')
        self.assertFalse(server['properties']['cpuHotPlug'])
        self.assertFalse(server['properties']['cpuHotUnplug'])
        self.assertFalse(server['properties']['ramHotPlug'])
        self.assertFalse(server['properties']['ramHotUnplug'])
        self.assertFalse(server['properties']['nicHotPlug'])
        self.assertFalse(server['properties']['nicHotUnplug'])
        self.assertFalse(server['properties']['discVirtioHotPlug'])
        self.assertFalse(server['properties']['discVirtioHotUnplug'])
        self.assertFalse(server['properties']['discScsiHotPlug'])
        self.assertFalse(server['properties']['discScsiHotUnplug'])

    def test_detach_volume(self):
        volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'

        server = self.server.detach_volume(
            datacenter_id=datacenter_id,
            server_id=server_id,
            volume_id=volume_id)

        self.assertTrue(server)

    def test_attach_volume(self):
        volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'

        server = self.server.attach_volume(
            datacenter_id=datacenter_id,
            server_id=server_id,
            volume_id=volume_id)

        self.assertEqual(server['id'], volume_id)
        self.assertEqual(server['properties']['name'], 'my boot volume for server 1')
        self.assertEqual(server['properties']['size'], 80)
        self.assertEqual(server['properties']['bus'], 'VIRTIO')
        self.assertEqual(server['properties']['image'], None)
        self.assertEqual(server['properties']['imagePassword'], None)
        self.assertEqual(server['properties']['type'], 'HDD')
        self.assertEqual(server['properties']['licenceType'], 'WINDOWS')
        self.assertFalse(server['properties']['cpuHotPlug'])
        self.assertFalse(server['properties']['cpuHotUnplug'])
        self.assertFalse(server['properties']['ramHotPlug'])
        self.assertFalse(server['properties']['ramHotUnplug'])
        self.assertFalse(server['properties']['nicHotPlug'])
        self.assertFalse(server['properties']['nicHotUnplug'])
        self.assertFalse(server['properties']['discVirtioHotPlug'])
        self.assertFalse(server['properties']['discVirtioHotUnplug'])
        self.assertFalse(server['properties']['discScsiHotPlug'])
        self.assertFalse(server['properties']['discScsiHotUnplug'])

    def test_get_attached_cdroms(self):
        servers = self.server.get_attached_cdroms(
            datacenter_id=datacenter_id,
            server_id=server_id)

        self.assertEqual(len(servers), 4)
        self.assertEqual(servers['items'][0]['id'], '7df81087-5835-41c6-a10b-3e098593bbd2')
        self.assertEqual(servers['items'][0]['properties']['name'], 'Ubuntu 14.04')
        self.assertEqual(servers['items'][0]['properties']['size'], 28)
        self.assertEqual(servers['items'][0]['properties']['description'],
                         'Ubuntu image description')
        self.assertEqual(servers['items'][0]['properties']['location'], 'de/fkb')
        self.assertEqual(servers['items'][0]['properties']['imageType'], 'CDROM')
        self.assertEqual(servers['items'][0]['properties']['licenceType'], 'UNKNOWN')
        self.assertFalse(servers['items'][0]['properties']['public'])
        self.assertFalse(servers['items'][0]['properties']['cpuHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['cpuHotUnplug'])
        self.assertFalse(servers['items'][0]['properties']['ramHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['ramHotUnplug'])
        self.assertFalse(servers['items'][0]['properties']['nicHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['nicHotUnplug'])
        self.assertFalse(servers['items'][0]['properties']['discVirtioHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['discVirtioHotUnplug'])
        self.assertFalse(servers['items'][0]['properties']['discScsiHotPlug'])
        self.assertFalse(servers['items'][0]['properties']['discScsiHotUnplug'])

    def test_get_attached_cdrom(self):
        cdrom_id = '7df81087-5835-41c6-a10b-3e098593bbd2'

        server = self.server.get_attached_cdrom(
            datacenter_id=datacenter_id,
            server_id=server_id,
            cdrom_id=cdrom_id)

        self.assertEqual(server['id'], cdrom_id)
        self.assertEqual(server['properties']['name'], 'Ubuntu 14.04')
        self.assertEqual(server['properties']['size'], 28)
        self.assertEqual(server['properties']['description'], 'Ubuntu image description')
        self.assertEqual(server['properties']['location'], 'de/fkb')
        self.assertEqual(server['properties']['imageType'], 'CDROM')
        self.assertEqual(server['properties']['licenceType'], 'UNKNOWN')
        self.assertFalse(server['properties']['public'])
        self.assertFalse(server['properties']['cpuHotPlug'])
        self.assertFalse(server['properties']['cpuHotUnplug'])
        self.assertFalse(server['properties']['ramHotPlug'])
        self.assertFalse(server['properties']['ramHotUnplug'])
        self.assertFalse(server['properties']['nicHotPlug'])
        self.assertFalse(server['properties']['nicHotUnplug'])
        self.assertFalse(server['properties']['discVirtioHotPlug'])
        self.assertFalse(server['properties']['discVirtioHotUnplug'])
        self.assertFalse(server['properties']['discScsiHotPlug'])
        self.assertFalse(server['properties']['discScsiHotUnplug'])

    def test_detach_cdrom(self):
        cdrom_id = '7df81087-5835-41c6-a10b-3e098593bbd2'

        server = self.server.detach_cdrom(
            datacenter_id=datacenter_id,
            server_id=server_id,
            cdrom_id=cdrom_id)

        self.assertTrue(server)

    def test_attach_cdrom(self):
        cdrom_id = '7df81087-5835-41c6-a10b-3e098593bbd2'

        server = self.server.attach_cdrom(
            datacenter_id=datacenter_id,
            server_id=server_id,
            cdrom_id=cdrom_id)

        self.assertEqual(server['id'], cdrom_id)
        self.assertEqual(server['properties']['name'], 'Ubuntu 14.04')
        self.assertEqual(server['properties']['size'], 28)
        self.assertEqual(server['properties']['description'], 'Ubuntu image description')
        self.assertEqual(server['properties']['location'], 'de/fkb')
        self.assertEqual(server['properties']['imageType'], 'CDROM')
        self.assertEqual(server['properties']['licenceType'], 'UNKNOWN')
        self.assertFalse(server['properties']['public'])
        self.assertFalse(server['properties']['cpuHotPlug'])
        self.assertFalse(server['properties']['cpuHotUnplug'])
        self.assertFalse(server['properties']['ramHotPlug'])
        self.assertFalse(server['properties']['ramHotUnplug'])
        self.assertFalse(server['properties']['nicHotPlug'])
        self.assertFalse(server['properties']['nicHotUnplug'])
        self.assertFalse(server['properties']['discVirtioHotPlug'])
        self.assertFalse(server['properties']['discVirtioHotUnplug'])
        self.assertFalse(server['properties']['discScsiHotPlug'])
        self.assertFalse(server['properties']['discScsiHotUnplug'])

    def test_start_server(self):
        server = self.server.start_server(
            datacenter_id=datacenter_id,
            server_id=server_id)

        self.assertTrue(server)

    def test_stop_server(self):
        server = self.server.stop_server(
            datacenter_id=datacenter_id,
            server_id=server_id)

        self.assertTrue(server)

    def test_reboot_server(self):
        server = self.server.reboot_server(
            datacenter_id=datacenter_id,
            server_id=server_id)

        self.assertTrue(server)

if __name__ == '__main__':
    unittest.main()
