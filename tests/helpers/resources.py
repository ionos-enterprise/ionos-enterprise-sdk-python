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

import re

from . import configuration


def resource():
    return {
        'locations': ['us/las', 'us/ewr', 'de/fra', 'de/fkb'],
        'licence_type': ['LINUX', 'WINDOWS', 'WINDOWS2016', 'OTHER', 'UNKNOWN'],
        'vm_states': ['RUNNING', 'SHUTOFF'],
        'uuid_match':
            '^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
        'mac_match': re.compile(
            '^([0-9a-f]{2}[:]){5}([0-9a-f]{2})$'),
        'datacenter': {
            'name': 'Python SDK Test',
            'description': 'Python SDK test datacenter',
            'location': configuration.LOCATION
        },

        'datacenter_composite': {
            'name': 'Python SDK Test Composite',
            'description': 'Python SDK test composite datacenter',
            'location': configuration.LOCATION
        },
        'server': {
            'name': 'Python SDK Test',
            'ram': 1024,
            'cores': 1,
            'cpu_family': 'INTEL_XEON',
            'availability_zone': 'ZONE_1'
        },
        'boot_volume': {
            'name': 'Python SDK Test',
            'size': 10,
            'bus': 'VIRTIO',
            'disk_type': 'HDD',
            'image_alias': 'ubuntu:latest',
            'availability_zone': 'ZONE_1'
        },
        'volume': {
            'name': 'Python SDK Test',
            'size': 2,
            'bus': 'VIRTIO',
            'disk_type': 'HDD',
            'licence_type': 'UNKNOWN',
            'availability_zone': 'ZONE_1'
        },
        'volume2': {
            'name': 'Python SDK Test',
            'size': 2,
            'bus': 'VIRTIO',
            'disk_type': 'HDD',
            'availability_zone': 'ZONE_3',
            'ssh_keys': ['ssh-rsa AAAAB3NzaC1']
        },
        'snapshot': {
            'name': 'Python SDK Test',
            'description': 'Python SDK test snapshot',
            'size': 2
        },
        'nic': {
            'name': 'Python SDK Test',
            'dhcp': True,
            'lan': 1,
            'firewall_active': True,
            'nat': False
        },
        'fwrule': {
            'name': 'SSH',
            'protocol': 'TCP',
            'source_mac': '01:23:45:67:89:00',
            'source_ip': None,
            'target_ip': None,
            'port_range_start': 22,
            'port_range_end': 22,
            'icmp_type': None,
            'icmp_code': None,
        },
        'loadbalancer': {
            'name': 'python sdk test',
            'dhcp': True
        },
        'lan': {
            # REST API converts names to lowercase.
            'name': 'python sdk test',
            'public': True,
        },
        'ipblock': {
            # REST API converts names to lowercase.
            'name': 'python sdk test',
            'location': configuration.LOCATION,
            'size': 1
        },
        'group': {
            'name': 'Python SDK Test',
            'create_datacenter': True,
            'create_snapshot': True,
            'reserve_ip': True,
            'access_activity_log': True
        },

        'not_found_error': 'Resource does not exist',
        'missing_attribute_error': "Attribute '%s' is required"
    }


def find_image(conn, name):
    '''
    Find image by partial name and location.
    '''
    for item in conn.list_images()['items']:
        if (item['properties']['location'] == configuration.LOCATION and
                item['properties']['imageType'] == 'HDD' and
                name in item['properties']['name']):
            return item
    return None


def check_detached_cdrom_gone(parent):
    '''
    Check if an attached cdrom is not attached anymore and it throws a PBNotFoundError
    '''
    parent.client.get_attached_cdrom(
        datacenter_id=parent.datacenter['id'],
        server_id=parent.server['id'],
        cdrom_id=parent.test_image1['id'])
