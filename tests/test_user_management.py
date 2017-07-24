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

import unittest
from random import randint

from helpers import configuration
from helpers.resources import resource, find_image
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, IPBlock, User, Group, Volume
from profitbricks.errors import PBError, PBNotFoundError


class TestUserManagement(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create datacenter resource
        self.datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))
        self.client.wait_for_completion(self.datacenter)

        # Create volume resource
        volume = Volume(**self.resource['volume'])
        self.volume = self.client.create_volume(
            datacenter_id=self.datacenter['id'],
            volume=volume
        )

        self.client.wait_for_completion(self.volume)

        self.image = find_image(self.client, configuration.IMAGE_NAME)

        # Create snapshot resource
        self.snapshot = self.client.create_snapshot(
            datacenter_id=self.datacenter['id'],
            volume_id=self.volume['id'],
            name=self.resource['snapshot']['name'])

        self.client.wait_for_completion(self.snapshot)

        # Reserve IP block resource
        self.ipblock = self.client.reserve_ipblock(IPBlock(**self.resource['ipblock']))

        # Create User 1
        self.user_dict1 = User(
            firstname='John',
            lastname='Doe',
            email='no-reply%s@example.com' % randint(0, 9999999999999),
            password='secretpassword123%s' % randint(0, 99999999),
            administrator=True,
            force_sec_auth=False)
        self.user1 = self.client.create_user(user=self.user_dict1)

        # Create User 2
        self.user_dict2 = User(
            firstname='John',
            lastname='Doe',
            email='no-reply%s@example.com' % randint(0, 9999999999999),
            password='secretpassword123%s' % randint(0, 99999999))
        self.user2 = self.client.create_user(user=self.user_dict2)

        # Create User 3
        self.user_dict3 = User(
            firstname='John',
            lastname='Doe',
            email='no-reply%s@example.com' % randint(0, 9999999999999),
            password='secretpassword123%s' % randint(0, 99999999))
        self.user3 = self.client.create_user(user=self.user_dict3)

        # Create Group 1
        group = Group(**self.resource['group'])
        self.group1 = self.client.create_group(group)

        # Create Group 2
        group.name = self.resource['group']['name'] + ' 2'
        self.group2 = self.client.create_group(group)

        # Create Group 3
        group.name = self.resource['group']['name'] + ' 3'
        self.group3 = self.client.create_group(group)

        # Create Share 1
        self.share1 = self.client.add_share(
            group_id=self.group3['id'],
            resource_id=self.datacenter['id'],
            edit_privilege=True,
            share_privilege=True)

        # Create Share 2
        self.share2 = self.client.add_share(
            group_id=self.group3['id'],
            resource_id=self.ipblock['id'],
            edit_privilege=True,
            share_privilege=True)

    @classmethod
    def tearDownClass(self):
        self.client.delete_snapshot(snapshot_id=self.snapshot['id'])
        self.client.delete_user(user_id=self.user1['id'])
        self.client.delete_user(user_id=self.user3['id'])
        self.client.delete_group(group_id=self.group1['id'])
        self.client.delete_group(group_id=self.group3['id'])
        self.client.delete_ipblock(ipblock_id=self.ipblock['id'])
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_create_user(self):
        self.assertEqual(self.user1['type'], 'user')
        self.assertEqual(self.user1['properties']['firstname'], self.user_dict1.firstname)
        self.assertEqual(self.user1['properties']['lastname'], self.user_dict1.lastname)
        self.assertEqual(self.user1['properties']['email'], self.user_dict1.email)
        self.assertEqual(self.user1['properties']['administrator'], self.user_dict1.administrator)
        self.assertEqual(self.user1['properties']['forceSecAuth'], self.user_dict1.force_sec_auth)

    def test_list_users(self):
        users = self.client.list_users()

        self.assertGreater(len(users['items']), 0)
        self.assertEqual(users['items'][0]['type'], 'user')

    def test_get_user(self):
        user = self.client.get_user(user_id=self.user1['id'])

        self.assertEqual(user['type'], 'user')
        self.assertEqual(user['id'], self.user1['id'])
        self.assertEqual(user['properties']['firstname'], self.user1['properties']['firstname'])
        self.assertEqual(user['properties']['lastname'], self.user1['properties']['lastname'])
        self.assertEqual(user['properties']['email'], self.user1['properties']['email'])
        self.assertEqual(user['properties']['administrator'],
                         self.user1['properties']['administrator'])
        self.assertEqual(user['properties']['forceSecAuth'],
                         self.user1['properties']['forceSecAuth'])
        self.assertFalse(user['properties']['secAuthActive'])

    def test_delete_user(self):
        user = self.client.delete_user(user_id=self.user2['id'])

        self.assertTrue(user)

    def test_update_user(self):
        user = self.client.update_user(
            user_id=self.user1['id'],
            firstname=self.user1['properties']['firstname'],
            lastname=self.user1['properties']['lastname'],
            email=self.user1['properties']['email'],
            administrator=False,
            force_sec_auth=self.user1['properties']['forceSecAuth']
        )

        self.assertEqual(user['type'], 'user')
        self.assertEqual(user['id'], self.user1['id'])
        self.assertEqual(user['properties']['firstname'], self.user1['properties']['firstname'])
        self.assertEqual(user['properties']['lastname'], self.user1['properties']['lastname'])
        self.assertEqual(user['properties']['email'], self.user1['properties']['email'])
        self.assertFalse(user['properties']['administrator'])
        self.assertEqual(user['properties']['forceSecAuth'],
                         self.user1['properties']['forceSecAuth'])

    def test_create_user_failure(self):
        try:
            user = User(
                firstname='John',
                lastname='Doe',
                password='secretpassword123')
            self.client.create_user(user)
        except PBError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'email',
                          e.content[0]['message'])

    def test_get_user_failure(self):
        try:
            self.client.get_user('00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_group(self):
        self.assertEqual(self.group1['type'], 'group')
        self.assertEqual(self.group1['properties']['name'], self.resource['group']['name'])
        self.assertEqual(self.group1['properties']['createDataCenter'],
                         self.resource['group']['create_datacenter'])
        self.assertEqual(self.group1['properties']['createSnapshot'],
                         self.resource['group']['create_snapshot'])
        self.assertEqual(self.group1['properties']['reserveIp'],
                         self.resource['group']['reserve_ip'])
        self.assertEqual(self.group1['properties']['accessActivityLog'],
                         self.resource['group']['access_activity_log'])

    def test_list_groups(self):
        groups = self.client.list_groups()

        self.assertGreater(len(groups['items']), 0)
        self.assertEqual(groups['items'][0]['type'], 'group')

    def test_get_group(self):
        group = self.client.get_group(group_id=self.group1['id'])

        self.assertEqual(group['type'], 'group')
        self.assertEqual(group['id'], self.group1['id'])
        self.assertEqual(group['properties']['name'], self.group1['properties']['name'])
        self.assertEqual(group['properties']['createDataCenter'],
                         self.group1['properties']['createDataCenter'])
        self.assertEqual(group['properties']['createSnapshot'],
                         self.group1['properties']['createSnapshot'])
        self.assertEqual(group['properties']['reserveIp'],
                         self.group1['properties']['reserveIp'])
        self.assertEqual(group['properties']['accessActivityLog'],
                         self.group1['properties']['accessActivityLog'])

    def test_delete_group(self):
        group = self.client.delete_group(group_id=self.group2['id'])

        self.assertTrue(group)

    def test_update_group(self):
        group = self.client.update_group(
            group_id=self.group1['id'],
            name=self.resource['group']['name'] + ' - RENAME',
            create_datacenter=False
        )

        self.assertEqual(group['type'], 'group')
        self.assertEqual(group['id'], self.group1['id'])
        self.assertEqual(group['properties']['name'],
                         self.resource['group']['name'] + ' - RENAME')
        self.assertFalse(group['properties']['createDataCenter'])

    def test_create_group_failure(self):
        try:
            self.client.create_group(Group(create_datacenter=True))
        except PBError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'name',
                          e.content[0]['message'])

    def test_get_group_failure(self):
        try:
            self.client.get_group('00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_add_share(self):
        self.assertEqual(self.share1['type'], 'resource')
        self.assertTrue(self.share1['properties']['editPrivilege'])
        self.assertTrue(self.share1['properties']['sharePrivilege'])

    def test_list_shares(self):
        shares = self.client.list_shares(group_id=self.group3['id'])

        self.assertGreater(len(shares['items']), 0)
        self.assertEqual(shares['items'][0]['type'], 'resource')

    def test_get_share(self):
        share = self.client.get_share(group_id=self.group3['id'],
                                      resource_id=self.datacenter['id'])

        self.assertEqual(share['id'], self.datacenter['id'])
        self.assertEqual(share['type'], 'resource')
        self.assertTrue(share['properties']['editPrivilege'])
        self.assertTrue(share['properties']['sharePrivilege'])

    def test_update_share(self):
        share = self.client.update_share(group_id=self.group3['id'],
                                         resource_id=self.ipblock['id'],
                                         edit_privilege=False)

        self.assertEqual(share['id'], self.ipblock['id'])
        self.assertEqual(share['type'], 'resource')
        self.assertFalse(share['properties']['editPrivilege'])

    def test_remove_share(self):
        share = self.client.delete_share(group_id=self.group3['id'],
                                         resource_id=self.datacenter['id'])

        self.assertTrue(share)

    def test_get_share_failure(self):
        try:
            self.client.get_share(group_id=self.group3['id'],
                                  resource_id='00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_share_failure(self):
        try:
            self.client.add_share(group_id=self.group3['id'],
                                  resource_id='00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_list_group_users(self):
        users = self.client.list_group_users(group_id=self.group3['id'])

        self.assertGreater(len(users['items']), 0)
        self.assertEqual(users['items'][0]['type'], 'user')

    def test_add_group_user(self):
        user = self.client.add_group_user(group_id=self.group3['id'],
                                          user_id=self.user3['id'])

        self.assertEqual(user['id'], self.user3['id'])
        self.assertEqual(user['type'], 'user')

    def test_remove_group_user(self):
        user = self.client.remove_group_user(group_id=self.group3['id'],
                                             user_id=self.user3['id'])

        self.assertTrue(user)

    def test_list_resources(self):
        resources = self.client.list_resources()

        self.assertGreater(len(resources['items']), 0)
        self.assertEqual(resources['id'], 'resources')
        self.assertEqual(resources['type'], 'collection')

    def test_list_datacenter_resources(self):
        resources = self.client.list_resources(resource_type='datacenter')

        self.assertGreater(len(resources['items']), 0)
        self.assertEqual(resources['id'], 'resources')
        self.assertEqual(resources['items'][0]['type'], 'datacenter')

    def test_list_image_resources(self):
        resources = self.client.list_resources(resource_type='image')

        self.assertGreater(len(resources['items']), 0)
        self.assertEqual(resources['id'], 'resources')
        self.assertEqual(resources['items'][0]['type'], 'image')

    def test_list_snapshot_resources(self):
        resources = self.client.list_resources(resource_type='snapshot')

        self.assertGreater(len(resources['items']), 0)
        self.assertEqual(resources['id'], 'resources')
        self.assertEqual(resources['items'][0]['type'], 'snapshot')

    def test_list_ipblock_resources(self):
        resources = self.client.list_resources(resource_type='ipblock')

        self.assertGreater(len(resources['items']), 0)
        self.assertEqual(resources['id'], 'resources')
        self.assertEqual(resources['items'][0]['type'], 'ipblock')

    def test_list_resources_failure(self):
        try:
            self.client.list_resources(resource_type='unknown')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_get_datacenter_resource(self):
        resource = self.client.get_resource(resource_type='datacenter',
                                            resource_id=self.datacenter['id'])

        self.assertEqual(resource['id'], self.datacenter['id'])
        self.assertEqual(resource['type'], 'datacenter')

    def test_get_image_resource(self):
        resource = self.client.get_resource(resource_type='image',
                                            resource_id=self.image['id'])

        self.assertEqual(resource['id'], self.image['id'])
        self.assertEqual(resource['type'], 'image')

    def test_get_snapshot_resource(self):
        resource = self.client.get_resource(resource_type='snapshot',
                                            resource_id=self.snapshot['id'])

        self.assertEqual(resource['id'], self.snapshot['id'])
        self.assertEqual(resource['type'], 'snapshot')

    def test_list_ipblock_resources2(self):
        resource = self.client.get_resource(resource_type='ipblock',
                                            resource_id=self.ipblock['id'])

        self.assertEqual(resource['id'], self.ipblock['id'])
        self.assertEqual(resource['type'], 'ipblock')

    def test_get_resource_failure(self):
        try:
            self.client.get_resource(resource_type='datacenter',
                                     resource_id='00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
