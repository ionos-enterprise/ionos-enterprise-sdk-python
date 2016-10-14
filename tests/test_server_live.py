import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion
from profitbricks.client import Datacenter, Server, Volume, NIC, FirewallRule
from profitbricks.client import ProfitBricksService
from six import assertRegex

class TestServer(unittest.TestCase):
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

        # Create test volume1.
        self.volume1 = self.client.create_volume(
            datacenter_id=self.datacenter['id'],
            volume=Volume(**self.resource['volume']))
        wait_for_completion(self.client, self.volume1, 'create_volume')

        # Create test volume2 (attach volume test).
        self.volume2 = self.client.create_volume(
            datacenter_id=self.datacenter['id'],
            volume=Volume(**self.resource['volume']))
        wait_for_completion(self.client, self.volume2, 'create_volume')

        # Create test server.
        server = Server(**self.resource['server'])
        server.attach_volumes = [self.volume1['id']]
        self.server = self.client.create_server(
            datacenter_id=self.datacenter['id'],
            server=server)
        wait_for_completion(self.client, self.server, 'create_server')

        # Create test NIC.
        self.nic = self.client.create_nic(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            nic=NIC(**self.resource['nic']))
        wait_for_completion(self.client, self.nic, 'create_nic')

        # Find an Ubuntu image for testing.
        for item in self.client.list_images()['items']:
            if configuration.IMAGE_NAME in item['properties']['name'] and item['properties']['location'] == configuration.LOCATION:
                self.image = item

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_list(self):
        servers = self.client.list_servers(datacenter_id=self.datacenter['id'])

        self.assertGreater(len(servers), 0)
        self.assertEqual(servers['items'][0]['type'], 'server')
        self.assertTrue(self, len(servers['items'])>0)
        assertRegex(self, servers['items'][0]['id'], self.resource['uuid_match'])

    def test_get(self):
        server = self.client.get_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id']
        )

        self.assertEqual(server['type'], 'server')
        self.assertEqual(server['id'], self.server['id'])
        self.assertEqual(server['properties']['name'], self.resource['server']['name'])
        self.assertEqual(server['properties']['cores'], self.resource['server']['cores'])
        self.assertEqual(server['properties']['ram'], self.resource['server']['ram'])

    def test_delete(self):
        server = self.client.create_server(
            datacenter_id=self.datacenter['id'],
            server=Server(**self.resource['server'])
        )
        wait_for_completion(self.client, server, 'create_server')

        response = self.client.delete_server(
            datacenter_id=self.datacenter['id'],
            server_id=server['id']
        )

        self.assertTrue(response)

    def test_update(self):
        server = self.client.update_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            name=self.resource['server']['name'] + ' RENAME')
        wait_for_completion(self.client, server, 'update_server')
        server = self.client.get_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id']
        )

        self.assertEqual(server['id'], self.server['id'])
        self.assertEqual(server['properties']['name'], self.resource['server']['name'] + ' RENAME')
        self.assertEqual(server['properties']['cores'], self.resource['server']['cores'])
        self.assertEqual(server['properties']['ram'], self.resource['server']['ram'])

    def test_create_simple(self):
        # Use server created dring server test setup
        assertRegex(self, self.server['id'], self.resource['uuid_match'])
        self.assertEqual(self.server['type'], 'server')
        self.assertEqual(self.server['properties']['name'], self.resource['server']['name'])
        self.assertEqual(self.server['properties']['cores'], self.resource['server']['cores'])
        self.assertEqual(self.server['properties']['ram'], self.resource['server']['ram'])
        self.assertIsNone(self.server['properties']['availabilityZone'])
        self.assertIsNone(self.server['properties']['vmState'])

    def test_create_complex(self):
        fwrule = FirewallRule(**self.resource['fwrule'])
        nic = NIC(firewall_rules=[fwrule], **self.resource['nic'])
        volume = Volume(image=self.image['id'],
                        image_password='secretpassword123',
                        ssh_keys=['ssh-rsa AAAAB3NzaC1'],
                        **self.resource['volume'])

        server = Server(
            nics=[nic],
            create_volumes=[volume],
            **self.resource['server'])

        composite_server = self.client.create_server(
            datacenter_id=self.datacenter['id'],
            server=server)
        wait_for_completion(self.client, composite_server, 'create_server', wait_timeout=600)

        composite_server = self.client.get_server(
            datacenter_id=self.datacenter['id'],
            server_id=composite_server['id'])

        assertRegex(self, composite_server['id'], self.resource['uuid_match'])
        self.assertEqual(composite_server['properties']['name'], self.resource['server']['name'])
        self.assertEqual(composite_server['properties']['cores'], self.resource['server']['cores'])
        self.assertEqual(composite_server['properties']['ram'], self.resource['server']['ram'])
        self.assertEqual(composite_server['properties']['availabilityZone'], 'AUTO')
        self.assertIn(composite_server['properties']['vmState'], self.resource['vm_states'])

    def test_start_server(self):
        server = self.client.start_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'])

        self.assertTrue(server)

    def test_stop_server(self):
        server = self.client.stop_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'])

        self.assertTrue(server)

    def test_reboot_server(self):
        server = self.client.reboot_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'])

        self.assertTrue(server)

    def test_get_attached_volumes(self):
        servers = self.client.get_attached_volumes(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'])

        self.assertGreater(len(servers), 0)
        self.assertEqual(servers['items'][0]['id'], self.volume1['id'])
        self.assertEqual(servers['items'][0]['properties']['name'], self.resource['volume']['name'])
        self.assertEqual(servers['items'][0]['properties']['size'], self.resource['volume']['size'])
        self.assertEqual(servers['items'][0]['properties']['bus'], self.resource['volume']['bus'])
        self.assertEqual(servers['items'][0]['properties']['type'], self.resource['volume']['type'])
        self.assertEqual(servers['items'][0]['properties']['licenceType'], 'UNKNOWN')
        self.assertIsNone(servers['items'][0]['properties']['image'])
        self.assertIsNone(servers['items'][0]['properties']['imagePassword'])
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
        server = self.client.get_attached_volume(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            volume_id=self.volume1['id'])

        self.assertEqual(server['id'], self.volume1['id'])
        self.assertEqual(server['properties']['name'], self.resource['volume']['name'])
        self.assertEqual(server['properties']['size'], self.resource['volume']['size'])
        self.assertEqual(server['properties']['bus'], self.resource['volume']['bus'])
        self.assertEqual(server['properties']['type'], self.resource['volume']['type'])
        self.assertEqual(server['properties']['licenceType'], self.resource['volume']['licence_type'])
        self.assertIsNone(server['properties']['image'])
        self.assertIsNone(server['properties']['imagePassword'])
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

    def test_attach_volume(self):
        volume = self.client.attach_volume(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            volume_id=self.volume2['id'])
        wait_for_completion(self.client, volume, 'attach_volume')

        self.assertEqual(volume['id'], self.volume2['id'])
        self.assertEqual(volume['properties']['name'], self.resource['volume']['name'])
        self.assertEqual(volume['properties']['size'], self.resource['volume']['size'])
        self.assertEqual(volume['properties']['type'], self.resource['volume']['type'])
        self.assertEqual(volume['properties']['licenceType'], self.resource['volume']['licence_type'])
        self.assertIsNone(volume['properties']['bus'])
        self.assertIsNone(volume['properties']['image'])
        self.assertIsNone(volume['properties']['imagePassword'])
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

        response = self.client.detach_volume(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            volume_id=self.volume2['id'])

    def test_detach_volume(self):
        volume = self.client.detach_volume(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            volume_id=self.volume1['id'])

        self.assertTrue(volume)

if __name__ == '__main__':
    unittest.main()
