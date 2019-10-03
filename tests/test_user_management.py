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

import unittest
from random import randint

from six import assertRegex

from ionosenterprise.client import Datacenter, IPBlock, User, Group, Volume, IonosEnterpriseService
from ionosenterprise.errors import ICError, ICNotFoundError

from helpers import configuration
from helpers.resources import resource, find_image


class TestUserManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create datacenter resource
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['datacenter']))
        cls.client.wait_for_completion(cls.datacenter)

        # Create volume resource
        volume = Volume(**cls.resource['volume'])
        cls.volume = cls.client.create_volume(
            datacenter_id=cls.datacenter['id'],
            volume=volume
        )

        cls.client.wait_for_completion(cls.volume)

        cls.image = find_image(cls.client, configuration.IMAGE_NAME)

        # Create snapshot resource
        cls.snapshot = cls.client.create_snapshot(
            datacenter_id=cls.datacenter['id'],
            volume_id=cls.volume['id'],
            name=cls.resource['snapshot']['name'])

        cls.client.wait_for_completion(cls.snapshot)

        # Reserve IP block resource
        cls.ipblock = cls.client.reserve_ipblock(IPBlock(**cls.resource['ipblock']))

        # Create User 1
        cls.user_dict1 = User(
            firstname='John',
            lastname='Doe',
            email='no-reply%s@example.com' % randint(0, 9999999999999),
            password='secretpassword123%s' % randint(0, 99999999),
            administrator=True,
            force_sec_auth=False)
        cls.user1 = cls.client.create_user(user=cls.user_dict1)

        # Create User 2
        cls.user_dict2 = User(
            firstname='John',
            lastname='Doe',
            email='no-reply%s@example.com' % randint(0, 9999999999999),
            password='secretpassword123%s' % randint(0, 99999999))
        cls.user2 = cls.client.create_user(user=cls.user_dict2)

        # Create User 3
        cls.user_dict3 = User(
            firstname='John',
            lastname='Doe',
            email='no-reply%s@example.com' % randint(0, 9999999999999),
            password='secretpassword123%s' % randint(0, 99999999))
        cls.user3 = cls.client.create_user(user=cls.user_dict3)

        # Create Group 1
        group = Group(**cls.resource['group'])
        cls.group1 = cls.client.create_group(group)

        # Create Group 2
        group.name = cls.resource['group']['name'] + ' 2'
        cls.group2 = cls.client.create_group(group)

        # Create Group 3
        group.name = cls.resource['group']['name'] + ' 3'
        cls.group3 = cls.client.create_group(group)

        # Create Share 1
        cls.share1 = cls.client.add_share(
            group_id=cls.group3['id'],
            resource_id=cls.datacenter['id'],
            edit_privilege=True,
            share_privilege=True)

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_share(group_id=cls.group3['id'],
                                resource_id=cls.datacenter['id'])
        cls.client.delete_snapshot(snapshot_id=cls.snapshot['id'])
        cls.client.delete_user(user_id=cls.user1['id'])
        cls.client.delete_user(user_id=cls.user3['id'])
        cls.client.delete_group(group_id=cls.group1['id'])
        cls.client.delete_group(group_id=cls.group3['id'])
        cls.client.delete_ipblock(ipblock_id=cls.ipblock['id'])
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])

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
        assertRegex(self, user['requestId'], self.resource['uuid_match'])

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
        except ICError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'email',
                          e.content[0]['message'])

    def test_get_user_failure(self):
        try:
            self.client.get_user('00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
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

    def test_delete_group(self):
        group = self.client.delete_group(group_id=self.group2['id'])

        self.assertTrue(group)
        assertRegex(self, group['requestId'], self.resource['uuid_match'])

    def test_create_group_failure(self):
        try:
            self.client.create_group(Group(create_datacenter=True))
        except ICError as e:
            self.assertIn(self.resource['missing_attribute_error'] % 'name',
                          e.content[0]['message'])

    def test_get_group_failure(self):
        try:
            self.client.get_group('00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
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
                                         resource_id=self.datacenter['id'],
                                         share_privilege=False)

        self.assertEqual(share['id'], self.datacenter['id'])
        self.assertEqual(share['type'], 'resource')
        self.assertFalse(share['properties']['sharePrivilege'])

    def test_get_share_failure(self):
        try:
            self.client.get_share(group_id=self.group3['id'],
                                  resource_id='00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_create_share_failure(self):
        try:
            self.client.add_share(group_id=self.group3['id'],
                                  resource_id='00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
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
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

    def test_get_datacenter_resource(self):
        data_center = self.client.get_resource(resource_type='datacenter',
                                               resource_id=self.datacenter['id'])

        self.assertEqual(data_center['id'], self.datacenter['id'])
        self.assertEqual(data_center['type'], 'datacenter')

    def test_get_image_resource(self):
        image = self.client.get_resource(resource_type='image',
                                         resource_id=self.image['id'])

        self.assertEqual(image['id'], self.image['id'])
        self.assertEqual(image['type'], 'image')

    def test_get_snapshot_resource(self):
        snapshot = self.client.get_resource(resource_type='snapshot',
                                            resource_id=self.snapshot['id'])

        self.assertEqual(snapshot['id'], self.snapshot['id'])
        self.assertEqual(snapshot['type'], 'snapshot')

    def test_list_ipblock_resources2(self):
        ipblock = self.client.get_resource(resource_type='ipblock',
                                           resource_id=self.ipblock['id'])

        self.assertEqual(ipblock['id'], self.ipblock['id'])
        self.assertEqual(ipblock['type'], 'ipblock')

    def test_get_resource_failure(self):
        try:
            self.client.get_resource(resource_type='datacenter',
                                     resource_id='00000000-0000-0000-0000-000000000000')
        except ICNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])


if __name__ == '__main__':
    unittest.main()
