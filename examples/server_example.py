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

# pylint: disable=reimported,wrong-import-position

"""Create Simple Server
"""

from ionosenterprise.client import IonosEnterpriseService
from ionosenterprise.client import Server

server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

i = Server(
    name='server',
    ram=4096,
    cores=4
    )

response = client.create_server(
    datacenter_id=datacenter_id,
    server=i)

"""Create Complex Server
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Server, NIC, Volume  # noqa

server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
image_id = '226ed8c0-a2fe-11e4-b187-5f1f641608c8'

client = IonosEnterpriseService(
    username='username', password='password')

nic1 = NIC(
    name='nic1',
    ips=['10.2.2.5'],
    dhcp='true',
    lan=1,
    firewall_active=True,
    )

nic2 = NIC(
    name='nic2',
    ips=['10.2.3.6'],
    dhcp='true',
    lan=1,
    firewall_active=True,
    )

volume1 = Volume(
    name='volume6',
    size=56,
    image=image_id,
    bus='VIRTIO'
    )

volume2 = Volume(
    name='volume7',
    size=56,
    image=image_id,
    bus='VIRTIO'
    )

nics = [nic1, nic2]
create_volumes = [volume1, volume2]

i = Server(
    name='server11',
    ram=4096,
    cores=4,
    nics=nics,
    create_volumes=create_volumes
    )

response = client.create_server(
    datacenter_id=datacenter_id, server=i)

"""Create Server with Existing Volume
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Server  # noqa

server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba044'

client = IonosEnterpriseService(
    username='username', password='password')

attach_volumes = [volume_id]

i = Server(
    name='server1',
    ram=4096,
    cores=4,
    attach_volumes=attach_volumes
    )

response = client.create_server(
    datacenter_id=datacenter_id, server=i)

"""Create Server with New Volumes
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Server, Volume  # noqa

server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba044'

datacenter_id = 'c4fd1f8a-65e0-42cb-b8fa-ff7e87c3071b'
image_id = '27500669-d81b-11e4-aea4-52540066fee9'

client = IonosEnterpriseService(
    username='username', password='password')

volume1 = Volume(
    name='volume11',
    size=56,
    image=image_id,
    bus='VIRTIO'
    )

volume2 = Volume(
    name='volume21',
    size=56,
    image=image_id,
    bus='VIRTIO'
    )

create_volumes = [volume1, volume2]

i = Server(
    name='server12',
    ram=4096,
    cores=4,
    create_volumes=create_volumes
    )

response = client.create_server(
    datacenter_id=datacenter_id, server=i)

"""Create Server with NICs Only
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Server, NIC  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

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
    name='server87',
    ram=4096,
    cores=4,
    nics=nics
    )

response = client.create_server(
    datacenter_id=datacenter_id, server=i)

"""Create Server with Two Existing Volumes
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Server  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id1 = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
volume_id2 = '800e1cab-99b2-4c30-ba8c-1d273ddba024'

client = IonosEnterpriseService(
    username='username', password='password')

attach_volumes = [volume_id1, volume_id2]

i = Server(
    name='server1',
    ram=4096,
    cores=4,
    attach_volumes=attach_volumes
    )

response = client.create_server(
    datacenter_id=datacenter_id,
    server=i)

"""Create Server with Boot Volume
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Server  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id1 = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
volume_id2 = '800e1cab-99b2-4c30-ba8c-1d273ddba024'
boot_volume_id = '800e1cab-99b2-4c30-ba8c-1d273ddba024'

client = IonosEnterpriseService(
    username='username', password='password')

i = Server(
    name='server14',
    ram=4096,
    cores=4,
    boot_volume_id=boot_volume_id
    )

response = client.create_server(
    datacenter_id=datacenter_id,
    server=i)

"""Create Server with Existing Volumes and NICs
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa
from ionosenterprise.client import Server, NIC  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id1 = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
volume_id2 = '800e1cab-99b2-4c30-ba8c-1d273ddba024'
boot_volume_id = '800e1cab-99b2-4c30-ba8c-1d273ddba024'

client = IonosEnterpriseService(
    username='username', password='password')

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

response = client.create_server(
    datacenter_id=datacenter_id,
    server=i)

"""Start Server
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = IonosEnterpriseService(
    username='username', password='password')

server = client.start_server(
    datacenter_id=datacenter_id,
    server_id=server_id)

"""Stop Server
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = IonosEnterpriseService(
    username='username', password='password')

server = client.stop_server(
    datacenter_id=datacenter_id,
    server_id=server_id)

"""Reboot Server
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = IonosEnterpriseService(
    username='username', password='password')

server = client.reboot_server(
    datacenter_id=datacenter_id,
    server_id=server_id)

"""List Servers
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

servers = client.list_servers(datacenter_id=datacenter_id)

"""Delete Server
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = IonosEnterpriseService(
    username='username', password='password')

server = client.delete_server(
    datacenter_id=datacenter_id,
    server_id=server_id)

"""Update Server
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = IonosEnterpriseService(
    username='username', password='password')

server = client.update_server(
    datacenter_id=datacenter_id,
    server_id=server_id,
    cores=35,
    ram=2048)
