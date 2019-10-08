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

"""Create volume
"""

from ionosenterprise.client import IonosEnterpriseService, Volume

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = IonosEnterpriseService(
    username='username', password='password')

i = Volume(
    name='Explicitly created volume',
    size=56,
    image='<IMAGE/SNAPSHOT-ID>',
    bus='VIRTIO')

response = client.create_volume(
    datacenter_id=datacenter_id, volume=i)

"""Create snapshot
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'

client = IonosEnterpriseService(
    username='username', password='password')

volume = client.create_snapshot(
    datacenter_id=datacenter_id,
    volume_id=volume_id,
    name='<URLENCODED_SNAPSHOT_NAME>',
    description='<URLENCODED_SNAPSHOT_DESCRIPTION>')

"""Restore Snapshot
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'
snapshot_id = '7df81087-5835-41c6-a10b-3e098593bba4'


client = IonosEnterpriseService(
    username='username', password='password')

response = client.restore_snapshot(
    datacenter_id=datacenter_id,
    volume_id=volume_id,
    snapshot_id=snapshot_id)

"""Update Volume
"""

from ionosenterprise.client import IonosEnterpriseService  # noqa

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'

client = IonosEnterpriseService(
    username='username', password='password')

volume = client.update_volume(
    datacenter_id=datacenter_id,
    volume_id=volume_id,
    size=100,
    name='Resized storage to 100 GB')
