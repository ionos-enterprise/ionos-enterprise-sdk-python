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
import time

from six import assertRegex

from ionosenterprise.client import Datacenter, Server, Volume, NIC, FirewallRule, IonosEnterpriseService
from ionosenterprise.errors import ICError, ICNotFoundError

from helpers import configuration
from helpers.resources import resource, check_detached_cdrom_gone


class TestServer(unittest.TestCase):
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

        # Create test volume1.
        cls.volume1 = cls.client.create_volume(
            datacenter_id=cls.datacenter['id'],
            volume=Volume(**cls.resource['volume']))
        cls.client.wait_for_completion(cls.volume1)

        # Create test volume2 (attach volume test).
        cls.volume2 = cls.client.create_volume(
            datacenter_id=cls.datacenter['id'],
            volume=Volume(**cls.resource['volume']))
        cls.client.wait_for_completion(cls.volume2)

        # Create test server.
        server = Server(**cls.resource['server'])
        server.attach_volumes = [cls.volume1['id']]
        cls.server = cls.client.create_server(
            datacenter_id=cls.datacenter['id'],
            server=server)
        cls.client.wait_for_completion(cls.server)

        # Create test NIC.
        cls.nic = cls.client.create_nic(
            datacenter_id=cls.datacenter['id'],
            server_id=cls.server['id'],
            nic=NIC(**cls.resource['nic']))
        cls.client.wait_for_completion(cls.nic)

        # Find an Ubuntu image for testing.
        for item in cls.client.list_images()['items']:
            if (configuration.IMAGE_NAME in item['properties']['name'] and
                    item['properties']['location'] == configuration.LOCATION):
                cls.image = item
        # Find a cdrom image
        images = cls.client.list_images(depth=5)
        usedIndex = 0
        for index, image in enumerate(images['items']):
            if (image['metadata']['state'] == "AVAILABLE"
                    and image['properties']['public'] is True
                    and image['properties']['imageType'] == "CDROM"
                    and image['properties']['location'] == configuration.LOCATION
                    and image['properties']['licenceType'] == "LINUX"):
                if usedIndex == 0:
                    cls.test_image1 = image
                    usedIndex = index
                else:
                    cls.test_image2 = image
                    break
        # Create test cdrom
        cls.cdrom = cls.client.attach_cdrom(
            datacenter_id=cls.datacenter['id'],
            server_id=cls.server['id'],
            cdrom_id=cls.test_image1['id'])
        cls.client.wait_for_completion(cls.cdrom)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])

    def test_list_servers(self):
        servers = self.client.list_servers(datacenter_id=self.datacenter['id'])

        self.assertGreater(len(servers), 0)
        self.assertEqual(servers['items'][0]['type'], 'server')
        self.assertTrue(self, len(servers['items']) > 0)
        assertRegex(self, servers['items'][0]['id'], self.resource['uuid_match'])

    def test_get_server(self):
        server = self.client.get_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id']
        )

        self.assertEqual(server['type'], 'server')
        self.assertEqual(server['id'], self.server['id'])
        self.assertEqual(server['properties']['name'], self.resource['server']['name'])
        self.assertEqual(server['properties']['cores'], self.resource['server']['cores'])
        self.assertEqual(server['properties']['ram'], self.resource['server']['ram'])
        self.assertEqual(server['properties']['availabilityZone'],
                         self.resource['server']['availability_zone'])
        self.assertEqual(server['properties']['cpuFamily'], self.resource['server']['cpu_family'])
        # assertRegex(self, server['properties']['bootVolume']['id'], self.resource['uuid_match'])

    def test_get_failure(self):
        try:
            self.client.get_server(
                datacenter_id=self.datacenter['id'],
                server_id='00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_delete_server(self):
        server = self.client.create_server(
            datacenter_id=self.datacenter['id'],
            server=Server(**self.resource['server'])
        )
        self.client.wait_for_completion(server)

        response = self.client.delete_server(
            datacenter_id=self.datacenter['id'],
            server_id=server['id']
        )

        self.assertTrue(response)
        assertRegex(self, response['requestId'], self.resource['uuid_match'])

    def test_update_server(self):
        server = self.client.update_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            name=self.resource['server']['name'] + ' RENAME')
        self.client.wait_for_completion(server)
        server = self.client.get_server(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id']
        )

        self.assertEqual(server['id'], self.server['id'])
        self.assertEqual(server['properties']['name'], self.resource['server']['name'] + ' RENAME')
        self.assertEqual(server['properties']['cores'], self.resource['server']['cores'])
        self.assertEqual(server['properties']['ram'], self.resource['server']['ram'])

    def test_create_server(self):
        # Use server created during server test setup
        assertRegex(self, self.server['id'], self.resource['uuid_match'])
        self.assertEqual(self.server['type'], 'server')
        self.assertEqual(self.server['properties']['name'], self.resource['server']['name'])
        self.assertEqual(self.server['properties']['cores'], self.resource['server']['cores'])
        self.assertEqual(self.server['properties']['ram'], self.resource['server']['ram'])
        self.assertEqual(self.server['properties']['availabilityZone'],
                         self.resource['server']['availability_zone'])
        self.assertEqual(self.server['properties']['cpuFamily'],
                         self.resource['server']['cpu_family'])
        # assertRegex(self, server['properties']['bootVolume']['id'], self.resource['uuid_match'])
        # self.assertIsNone(self.server['properties']['availabilityZone'])
        self.assertIsNone(self.server['properties']['vmState'])

    def test_create_failure(self):
        try:
            server = Server(
                name=self.resource['server']['name'],
                ram=self.resource['server']['ram']
            )
            self.client.create_server(datacenter_id=self.datacenter['id'], server=server)
        except ICError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'cores',
                          e.content[0]['message'])

    def test_create_composite(self):
        fwrule = FirewallRule(**self.resource['fwrule'])
        nic = NIC(firewall_rules=[fwrule], **self.resource['nic'])
        volume = Volume(image=self.image['id'],
                        image_password='secretpassword123',
                        ssh_keys=['ssh-rsa AAAAB3NzaC1'],
                        **self.resource['volume'])
        volume.availability_zone = 'ZONE_3'

        server = Server(
            nics=[nic],
            create_volumes=[volume],
            **self.resource['server'])

        composite_server = self.client.create_server(
            datacenter_id=self.datacenter['id'],
            server=server)
        self.client.wait_for_completion(composite_server, timeout=600)

        composite_server = self.client.get_server(
            datacenter_id=self.datacenter['id'],
            server_id=composite_server['id'])

        assertRegex(self, composite_server['id'], self.resource['uuid_match'])
        self.assertEqual(composite_server['properties']['name'], self.resource['server']['name'])
        self.assertEqual(composite_server['properties']['cores'], self.resource['server']['cores'])
        self.assertEqual(composite_server['properties']['ram'], self.resource['server']['ram'])
        self.assertEqual(composite_server['properties']['availabilityZone'], 'ZONE_1')
        self.assertIn(composite_server['properties']['vmState'], self.resource['vm_states'])
        self.assertGreater(len(composite_server['entities']['volumes']['items']), 0)
        self.assertGreater(len(composite_server['entities']['nics']['items']), 0)

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
        volumes = self.client.get_attached_volumes(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'])

        self.assertGreater(len(volumes['items']), 0)
        self.assertEqual(volumes['items'][0]['type'], 'volume')
        self.assertEqual(volumes['items'][0]['id'], self.volume1['id'])
        self.assertEqual(volumes['items'][0]['properties']['name'],
                         self.resource['volume']['name'])
        self.assertEqual(volumes['items'][0]['properties']['size'],
                         self.resource['volume']['size'])
        self.assertEqual(volumes['items'][0]['properties']['bus'],
                         self.resource['volume']['bus'])
        self.assertEqual(volumes['items'][0]['properties']['type'],
                         self.resource['volume']['disk_type'])
        self.assertEqual(volumes['items'][0]['properties']['licenceType'], 'UNKNOWN')
        self.assertIsNone(volumes['items'][0]['properties']['image'])
        self.assertIsNone(volumes['items'][0]['properties']['imagePassword'])
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

    def test_get_attached_volume(self):
        volume = self.client.get_attached_volume(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            volume_id=self.volume1['id'])

        self.assertEqual(volume['id'], self.volume1['id'])
        self.assertEqual(volume['properties']['name'], self.resource['volume']['name'])
        self.assertEqual(volume['properties']['size'], self.resource['volume']['size'])
        self.assertEqual(volume['properties']['bus'], self.resource['volume']['bus'])
        self.assertEqual(volume['properties']['type'], self.resource['volume']['disk_type'])
        self.assertEqual(volume['properties']['licenceType'],
                         self.resource['volume']['licence_type'])
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

    def test_attach_volume(self):
        volume = self.client.attach_volume(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            volume_id=self.volume2['id'])
        self.client.wait_for_completion(volume)

        self.assertEqual(volume['id'], self.volume2['id'])
        self.assertEqual(volume['properties']['name'], self.resource['volume']['name'])
        self.assertEqual(volume['properties']['size'], self.resource['volume']['size'])
        self.assertEqual(volume['properties']['type'], self.resource['volume']['disk_type'])
        self.assertEqual(volume['properties']['licenceType'],
                         self.resource['volume']['licence_type'])
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

        self.client.detach_volume(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            volume_id=self.volume2['id'])

    def test_detach_volume(self):
        volume = self.client.detach_volume(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            volume_id=self.volume1['id'])

        self.assertTrue(volume)

    def test_list_cdroms(self):
        cdroms = self.client.get_attached_cdroms(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'])

        self.assertGreater(len(cdroms['items']), 0)

    def test_attach_cdrom(self):
        attached_cdrom = self.client.attach_cdrom(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            cdrom_id=self.test_image2['id'])

        self.client.wait_for_completion(attached_cdrom, timeout=600)
        self.assertEqual(attached_cdrom['id'], self.test_image2['id'])
        self.assertEqual(attached_cdrom['properties']['name'],
                         self.test_image2['properties']['name'])

    def test_get_cdrom(self):
        attached_cdrom = self.client.attach_cdrom(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            cdrom_id=self.test_image1['id'])

        self.client.wait_for_completion(attached_cdrom, timeout=600)
        cdrom = self.client.get_attached_cdrom(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            cdrom_id=attached_cdrom['id'])
        self.assertEqual(cdrom['id'], attached_cdrom['id'])
        self.assertEqual(cdrom['properties']['name'], attached_cdrom['properties']['name'])

    def test_detach_cdrom(self):
        detached_cd = self.client.detach_cdrom(
            datacenter_id=self.datacenter['id'],
            server_id=self.server['id'],
            cdrom_id=self.cdrom['id'])
        time.sleep(15)

        self.assertTrue(detached_cd)

        try:
            check_detached_cdrom_gone(self)
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
