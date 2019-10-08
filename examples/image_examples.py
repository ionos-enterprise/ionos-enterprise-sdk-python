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

"""List Images
"""
from ionosenterprise.client import IonosEnterpriseService

client = IonosEnterpriseService(
    username='username', password='password')

images = client.list_images()

print(images)

"""
Update Image

Valid image parameters are:

* name (str)
* description (str)
* licence_type (one of 'LINUX', 'WINDOWS' or 'UNKNOWN')
* cpu_hot_plug (bool)
* ram_hot_plug (bool)
* nic_hot_plug (bool)
* nic_hot_unplug (bool)
* disc_virtio_hot_plug (bool)
* disc_virtio_hot_unplug (bool)
* disc_scsi_hot_plug (bool)
* disc_scsi_hot_unplug (bool)

"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

client = IonosEnterpriseService(
    username='username', password='password')

image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'
image = client.update_image(
    image_id,
    name='New name',
    description="Centos 7 with NGnix",
    licence_type='LINUX',
    cpu_hot_plug=True,
    ram_hot_plug=True,
    nic_hot_plug=True,
    nic_hot_unplug=True,
    disc_virtio_hot_plug=True,
    disc_virtio_hot_unplug=True)

"""Delete Image
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

client = IonosEnterpriseService(
    username='username', password='password')

image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'

image = client.delete_image(image_id)
