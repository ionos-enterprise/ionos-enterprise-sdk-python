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

# pylint: disable=pointless-string-statement

import os

from ionosenterprise.client import IonosEnterpriseService, Group, User

# Instantiate IonosEnterprise connection
client = IonosEnterpriseService(
    username=os.getenv('IONOS_USERNAME'),
    password=os.getenv('IONOS_PASSWORD'))

"""Create a group
"""
request = Group(
    name='demo-group',
    create_datacenter=True,
    create_snapshot=False,
    reserve_ip=True,
    access_activity_log=False)

group = client.create_group(request)

"""List groups
"""
groups = client.list_groups()

"""Create a user
"""
user_request = User(
    firstname='John',
    lastname='Doe',
    email='demo-user@example.com',
    password='SecretPassword123',
    administrator=True,
    force_sec_auth=False)

user = client.create_user(user_request)

"""List users
"""
users = client.list_users()

"""Add user to group
"""
# gu = client.add_group_user(group_id=group['id'], user_id=user['id'])
# print json.dumps(gu, indent=4)

"""List group users
"""
gus = client.list_group_users(group_id=group['id'])

"""Delete group
"""
response = client.delete_group(group['id'])

"""Delete user
"""
response = client.delete_user(user['id'])

"""List all resources
"""
# listing all resources under an admin user may take a while
resources = client.list_resources()

"""List ipblock resources
"""
ipblock_resources = client.list_resources(resource_type='ipblock')
