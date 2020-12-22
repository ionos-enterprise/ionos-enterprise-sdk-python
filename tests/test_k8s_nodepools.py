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

import warnings
import unittest

from helpers import configuration
from helpers.resources import resource

from ionosenterprise.client import IonosEnterpriseService
from ionosenterprise.items import Datacenter


class TestK8sNodepools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning,
                                message="unclosed.*<ssl.SSLSocket.*>")
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test k8s cluster
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['datacenter']))
        cls.k8s_cluster = cls.client.create_k8s_cluster(**cls.resource['k8s_cluster'])

        # Wait for k8s cluster to be active
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_k8s_clusters(),
            fn_check=lambda r: list(filter(
                lambda e: e['id'] == cls.k8s_cluster['id'],
                r['items']
            ))[0]['metadata']['state'] == 'ACTIVE',
            scaleup=10000
        )

        cls.k8s_cluster_nodepool1 = cls.client.create_k8s_cluster_nodepool(
            cls.k8s_cluster['id'],
            datacenter_id=cls.datacenter['id'],
            **cls.resource['k8s_nodepool']
        )

        cls.k8s_cluster_nodepool2 = cls.client.create_k8s_cluster_nodepool(
            cls.k8s_cluster['id'],
            datacenter_id=cls.datacenter['id'],
            **cls.resource['k8s_nodepool']
        )

        # Wait for k8s cluster nodepool 1 to be active
        cls.client.wait_for(
            fn_request=lambda: cls.client.get_k8s_cluster_nodepool(
                cls.k8s_cluster['id'],
                cls.k8s_cluster_nodepool1['id']),
            fn_check=lambda r: r['metadata']['state'] == 'ACTIVE',
            scaleup=10000
        )

        # Wait for k8s cluster nodepool 2 to be active
        cls.client.wait_for(
            fn_request=lambda: cls.client.get_k8s_cluster_nodepool(
                cls.k8s_cluster['id'],
                cls.k8s_cluster_nodepool2['id']),
            fn_check=lambda r: r['metadata']['state'] == 'ACTIVE',
            scaleup=10000
        )

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_k8s_cluster_nodepool(cls.k8s_cluster['id'],
                                               cls.k8s_cluster_nodepool1['id'])
        # Wait for k8s cluster nodepool to be deleted
        cls.client.wait_for(
            fn_request=lambda: cls.client.self.client.list_k8s_cluster_nodepools(cls.k8s_cluster['id']),
            fn_check=lambda r: len(list(filter(
                lambda e: e['id'] == cls.k8s_cluster_nodepool1['id'],
                r['items']
            ))) == 0,
            scaleup=10000
        )
        cls.client.delete_k8s_cluster(cls.k8s_cluster['id'])
        cls.client.delete_datacenter(cls.datacenter['id'])

    def test_list_k8s_nodepools(self):
        k8s_nodepools = self.client.list_k8s_cluster_nodepools(self.k8s_cluster['id'])
        self.assertGreater(len(k8s_nodepools), 0)
        self.assertGreater(len(k8s_nodepools['items']), 0)

    def test_get_k8s_nodepool(self):
        k8s_nodepool = self.client.get_k8s_cluster_nodepool(self.k8s_cluster['id'],
                                                            self.k8s_cluster_nodepool1['id'])
        self.assertEqual(k8s_nodepool['type'], 'nodepool')
        self.assertEqual(k8s_nodepool['id'], self.k8s_cluster_nodepool1['id'])
        self.assertEqual(k8s_nodepool['properties']['name'], self.k8s_cluster_nodepool1['properties']['name'])

    def test_delete_k8s_nodepool(self):
        response = self.client.delete_k8s_cluster_nodepool(self.k8s_cluster['id'],
                                                           self.k8s_cluster_nodepool2['id'])
        print(response)
        self.assertTrue('requestId' in response)

    def test_update_k8s_nodepool(self):
        response = self.client.update_k8s_cluster_nodepool(
            self.k8s_cluster['id'], self.k8s_cluster_nodepool1['id'], 2,
            maintenance_window={
                'dayOfTheWeek': "Monday",
                'time': '17:00:00'},
            auto_scaling={'minNodeCount': '2', 'maxNodeCount': '3'}
        )
        # Wait for k8s cluster nodepool 1 to be active
        self.client.wait_for(
            fn_request=lambda: self.client.get_k8s_cluster_nodepool(
                self.k8s_cluster['id'],
                self.k8s_cluster_nodepool1['id']),
            fn_check=lambda r: r['metadata']['state'] == 'ACTIVE',
            scaleup=10000
        )
        self.assertEqual(response['maintenance_window']['dayOfTheWeek'], 'Monday')
        self.assertEqual(response['node_count'], 2)
        self.assertEqual(response['auto_scaling']['maxNodeCount'], 3)
