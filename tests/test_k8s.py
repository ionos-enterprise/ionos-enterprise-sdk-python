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

from ionosenterprise.client import Datacenter, IonosEnterpriseService

from helpers import configuration
from helpers.resources import resource


class TestK8S(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['k8s_datacenter'])
        )
        print(cls.datacenter)

        # Wait for datacenter to be active
        cls.client.wait_for_completion(cls.datacenter)

        # Create test k8s cluster
        cls.k8s_cluster = cls.client.create_k8s_cluster(**cls.resource['k8s_cluster'])
        print(cls.k8s_cluster)

        # Wait for k8s cluster to be active
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_k8s_clusters(),
            fn_check=lambda r: list(filter(
                lambda e: e['properties']['name'] == cls.resource['k8s_cluster']['name'],
                r['items']
              ))[0]['metadata']['state'] == 'ACTIVE',
            scaleup=10000
        )

        # get cluster config
        cls.k8s_config = cls.client.get_k8s_config(cls.k8s_cluster['id'])
        print(cls.k8s_config)

        # Create test k8s nodepool
        cls.k8s_nodepool = cls.client.create_k8s_cluster_nodepool(
            cls.k8s_cluster['id'],
            datacenter_id=cls.datacenter['id'],
            **cls.resource['k8s_nodepool']
        )
        print(cls.k8s_nodepool)

        # Wait for k8s nodepool to be active
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_k8s_cluster_nodepools(cls.k8s_cluster['id']),
            fn_check=lambda r: list(filter(
                lambda e: e['properties']['name'] == cls.resource['k8s_nodepool']['name'],
                r['items']
              ))[0]['metadata']['state'] == 'ACTIVE',
            scaleup=10000
        )

    def test_get_k8s_cluster_nodepool(self):
        lan = self.client.get_k8s_cluster_nodepool(self.k8s_cluster['id'], self.k8s_nodepool['id'])

        self.assertEqual(lan['type'], 'nodepool')
        self.assertEqual(lan['id'], self.k8s_cluster['id'])
        self.assertEqual(lan['properties']['name'], self.resource['k8s_nodepool']['name'])

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_k8s_cluster_nodepool(cls.k8s_cluster['id'], cls.k8s_nodepool['id'])
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_k8s_cluster_nodepools(cls.k8s_cluster['id']),
            fn_check=lambda r: len(list(filter(
                lambda e: e['properties']['name'] == cls.resource['k8s_nodepool']['name'],
                r['items']
              ))) == 0,
            scaleup=10000
        )

        cls.client.delete_k8s_cluster(cls.k8s_cluster['id'])
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_k8s_clusters(),
            fn_check=lambda r: len(list(filter(
                lambda e: e['properties']['name'] == cls.resource['k8s_cluster']['name'],
                r['items']
              ))) == 0,
            scaleup=10000
        )

        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_datacenters(),
            fn_check=lambda r: len(list(filter(
                lambda e: e['properties']['name'] == cls.resource['k8s_datacenter']['name'],
                r['items']
              ))) == 0,
            scaleup=10000
        )

    def test_get_config(self):
        self.assertEqual(self.k8s_config['type'], 'kubeconfig')
        # self.assertEqual(self.k8s_config['properties'], 'kubeconfig')


if __name__ == '__main__':
    unittest.main()
