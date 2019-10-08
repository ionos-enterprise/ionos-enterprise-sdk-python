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

"""List NICs
"""
from ionosenterprise.client import IonosEnterpriseService

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = IonosEnterpriseService(
    username='username', password='password')

nics = client.list_nics(
    datacenter_id=datacenter_id,
    server_id=server_id)

for n in nics['items']:
    print(n['properties']['name'])

"""Create NIC
"""
from ionosenterprise.client import IonosEnterpriseService, NIC  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = IonosEnterpriseService(
    username='username', password='password')

i = NIC(
    name='nic1',
    ips=['10.2.2.3', '10.2.3.4'],
    dhcp='true',
    lan=1,
    firewall_active=True
    )

response = client.create_nic(
    datacenter_id=datacenter_id,
    server_id=server_id,
    nic=i)

"""Create NIC with FirewallRules
"""
from ionosenterprise.client import IonosEnterpriseService, FirewallRule, NIC  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
nic_id = '<NIC-ID>'

client = IonosEnterpriseService(
    username='username', password='password')

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

i = NIC(
    name='nic1',
    ips=['10.2.2.3', '10.2.3.4'],
    dhcp='true',
    lan=1,
    firewall_active=True,
    firewall_rules=fw_rules
    )

response = client.create_nic(
    datacenter_id=datacenter_id,
    server_id=server_id, nic=i)
