#!/usr/bin/python3

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

# pylint: disable=pointless-string-statement,reimported,wrong-import-position

import os
"""List Datacenters
"""
from ionosenterprise.client import IonosEnterpriseService

client = IonosEnterpriseService(
    username=os.getenv('IONOS_USERNAME'), password=os.getenv('IONOS_PASSWORD'))

datacenters = client.list_datacenters()

for d in datacenters['items']:
    vdc = client.get_datacenter(d['id'])
    name = vdc['properties']['name']
    datacenter_id = vdc['id']
    break

"""Get Datacenter
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

datacenter = client.get_datacenter(
    datacenter_id=datacenter_id)

"""Create Simple Datacenter
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Datacenter, Volume, Server  # noqa

i = Datacenter(
    name='dc1',
    description='My New Datacenter',
    location='de/fkb'
)

response = client.create_datacenter(datacenter=i)

"""Create Complex Datacenter
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Datacenter, LAN, NIC, LoadBalancer, FirewallRule  # noqa

image_id = 'df8382a1-0f40-11e6-ab6b-52540005ab80'

fwrule1 = FirewallRule(
    name='Open SSH port',
    protocol='TCP',
    source_mac='01:23:45:67:89:00',
    port_range_start=22,
    port_range_end=22
)

fwrule2 = FirewallRule(
    name='Allow PING',
    protocol='ICMP',
    icmp_type=8,
    icmp_code=0
)

fw_rules = [fwrule1, fwrule2]

nic1 = NIC(
    name='nic1',
    ips=['10.2.2.3'],
    dhcp='true',
    lan=1,
    firewall_active=True,
    firewall_rules=fw_rules
)

nic2 = NIC(
    name='nic2',
    ips=['10.2.3.4'],
    dhcp='true',
    lan=1,
    firewall_active=True,
    firewall_rules=fw_rules
)

nics = [nic1, nic2]

volume1 = Volume(
    name='volume1',
    size=56,
    image=image_id,
    bus='VIRTIO',
    image_password="test1234"
)

volume2 = Volume(
    name='volume2',
    size=56,
    image=image_id,
    bus='VIRTIO',
    image_password="test1234"
)

volumes = [volume2]

server1 = Server(
    name='My New Server1',
    ram=4096,
    cores=4,
    nics=nics,
    create_volumes=[volume1]
)

servers = [server1]

lan1 = LAN(
    name='public Lan 4',
    public=True
)

lan2 = LAN(
    name='public Lan 5',
    public=True
)

lans = [lan1, lan2]

loadbalancer1 = LoadBalancer(
    name='LB01',
    ip='10.2.2.5',
    dhcp=False)

loadbalancers = [loadbalancer1]

d = Datacenter(
    name='My New Datacenter',
    description='Production environment',
    location='de/fkb',
    servers=servers,
    volumes=volumes,
    lans=lans,
    loadbalancers=loadbalancers
)

response = client.create_datacenter(datacenter=d)

del_response = client.delete_datacenter(response['id'])
