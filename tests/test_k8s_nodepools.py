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
from ionosenterprise.client import IonosEnterpriseService

from helpers import configuration
from helpers.resources import resource


class TestK8sNodepools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test k8s cluster
        cls.datacenter = cls.client.create_datacenter(**cls.resource['datacenter'])
        cls.k8s_cluster = cls.client.create_k8s_cluster(**cls.resource['k8s_cluster'])

        cls.k8s_cluster_nodepool1 = cls.client.create_k8s_cluster_nodepool(
            cls.k8s_cluster['id'],
            'k8s_cluster_nodepool1',
            cls.datacenter['id'],
            2,
            'INTEL_XEON',
            1,
            2048,
            'AUTO',
            'HDD',
            11,
            k8s_version='1.17.8',
            maintenance_window={
                'dayOfTheWeek': "Monday",
                'time': '17:00:00'},
            auto_scaling={'minNodeCount': 2, 'maxNodeCount': 3},
            lan_ids=[],
            labels={'l1': 'v1', 'l2': 'v2'},
            annotations={'au': 'va1', 'a2': 'va2'}
        )
        cls.k8s_cluster_nodepool2 = cls.client.create_k8s_cluster_nodepool(
            cls.k8s_cluster['id'],
            'k8s_cluster_nodepool2',
            cls.datacenter['id'],
            2,
            'INTEL_XEON',
            1,
            2048,
            'AUTO',
            'HDD',
            11,
            k8s_version='1.17.8',
            maintenance_window={
                'dayOfTheWeek': "Monday",
                'time': '17:00:00'},
            auto_scaling={'minNodeCount': 2, 'maxNodeCount': 3},
            lan_ids=[],
            labels={'l1': 'v1', 'l2': 'v2'},
            annotations={'au': 'va1', 'a2': 'va2'}
        )

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_datacenter(cls.k8s_nodepool1['id'])
        cls.client.delete_k8s_cluster_nodepool(cls.k8s_cluster['id'], cls.k8s_nodepool1['id'])
        cls.client.delete_k8s_cluster(cls.k8s_cluster['id'])

    def test_list_k8s_nodepools(self):
        k8s_nodepools = self.client.list_k8s_cluster_nodepools(self.k8s_cluster['id'])
        self.assertGreater(len(k8s_nodepools), 0)
        self.assertGreater(len(k8s_nodepools['items']), 0)

    def test_get_k8s_nodepool(self):
        k8s_nodepool = self.client.get_k8s_cluster_nodepool(self.k8s_cluster['id'], self.k8s_cluster_nodepool1['id'])
        self.assertEqual(k8s_nodepool['type'], 'nodepool')
        self.assertEqual(k8s_nodepool['id'], self.k8s_cluster_nodepool1['id'])
        self.assertEqual(k8s_nodepool['properties']['name'], self.k8s_cluster_nodepool1['name'])

    def test_delete_k8s_nodepool(self):
        response = self.client.delete_k8s_cluster_nodepool(self.k8s_cluster['id'], self.k8s_cluster_nodepool2['id'])
        self.assertTrue('requestId' in response)

    def test_update_k8s_nodepool(self):
        response = self.client.update_k8s_cluster_nodepool(
            self.k8s_cluster['id'], self.k8s_cluster_nodepool1['id'], 2,
            k8s_version='1.17.8',
            maintenance_window={
                'dayOfTheWeek': "Monday",
                'time': '17:00:00'},
            auto_scaling={'minNodeCount': 2, 'maxNodeCount': 3},
            lan_ids=[],
            labels={'l1-updated': 'v1-updated', 'l2-updated': 'v2-updated'},
            annotations={'au-updated': 'va1-updated', 'a2-updated': 'va2-updated'}
        )
        self.assertEqual(response['maintenance_window']['dayOfTheWeek'], 'Monday')
        self.assertEqual(response['k8s_version'], '1.17.8')
        self.assertEqual(response['annotations']['au-updated'], 'va1-updated')


