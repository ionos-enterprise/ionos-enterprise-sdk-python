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

"""List LANs
"""
from ionosenterprise.client import IonosEnterpriseService

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

lans = client.list_lans(datacenter_id=datacenter_id)

print(lans)

"""Create Complex LAN
"""
from ionosenterprise.client import IonosEnterpriseService, LAN  # noqa

lan_id = '4'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

nics = ['<NIC-ID-1>', '<NIC-ID-2>']

i = LAN(
    name='public Lan 4',
    public=True,
    nics=nics)

response = client.create_lan(datacenter_id=datacenter_id, lan=i)

"""Create LAN
"""
from ionosenterprise.client import IonosEnterpriseService, LAN  # noqa

lan_id = '4'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

i = LAN(
    name='public Lan 4',
    public=True)

response = client.create_lan(datacenter_id=datacenter_id, lan=i)

"""Get LAN Members
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

lan_id = '4'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

members = client.get_lan_members(datacenter_id=datacenter_id,
                                 lan_id=lan_id)
