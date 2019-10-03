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
"""List IPBlocks
"""
from ionosenterprise.client import IonosEnterpriseService

client = IonosEnterpriseService(
    username=os.getenv('IONOS_USERNAME'), password=os.getenv('IONOS_PASSWORD'))

ipblocks = client.list_ipblocks()

print(ipblocks)

"""Reserve IPBlock
"""
from ionosenterprise.client import IonosEnterpriseService, IPBlock  # noqa

i = IPBlock(name='py-test', location='de/fra', size=1)

ipblock = client.reserve_ipblock(i)

"""Release IPBlock
"""
from ionosenterprise.client import IonosEnterpriseService  # noqa

ipblock_id = ipblock['id']


ipblock = client.delete_ipblock(ipblock_id)
