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

from ionosenterprise.client import Datacenter, IonosEnterpriseService


class TestK8S(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings("ignore", category=ResourceWarning,
                                message="unclosed.*<ssl.SSLSocket.*>")
        cls.resource = resource()
        cls.client = IonosEnterpriseService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        cls.datacenter = cls.client.create_datacenter(
            datacenter=Datacenter(**cls.resource['k8s_datacenter'])
        )

        # Wait for datacenter to be active
        cls.client.wait_for_completion(cls.datacenter)

        # Create test k8s cluster
        cls.k8s_cluster = cls.client.create_k8s_cluster(**cls.resource['k8s_cluster'])

        # Create test k8s cluster for delete test
        cls.k8s_cluster_for_delete_test = cls.client.create_k8s_cluster(
            **cls.resource['k8s_cluster'])

        # Wait for k8s cluster to be active
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_k8s_clusters(),
            fn_check=lambda r: list(filter(
                lambda e: e['id'] == cls.k8s_cluster['id'],
                r['items']
              ))[0]['metadata']['state'] == 'ACTIVE',
            scaleup=10000
        )


        # get cluster config
        cls.k8s_config = cls.client.get_k8s_config(cls.k8s_cluster['id'])

    @classmethod
    def tearDownClass(cls):
        cls.client.delete_k8s_cluster(cls.k8s_cluster['id'])
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_k8s_clusters(),
            fn_check=lambda r: len(list(filter(
                lambda e: e['id'] == cls.k8s_cluster['id'],
                r['items']
              ))) == 0,
            scaleup=10000
        )
        cls.client.delete_datacenter(datacenter_id=cls.datacenter['id'])
        cls.client.wait_for(
            fn_request=lambda: cls.client.list_datacenters(),
            fn_check=lambda r: len(list(filter(
                lambda e: e['id'] == cls.datacenter['id'],
                r['items']
              ))) == 0,
            scaleup=10000
        )

    def test_delete_k8s_cluster(self):
        response = self.client.delete_k8s_cluster(self.k8s_cluster_for_delete_test['id'])
        self.assertIn('requestId', response)

    def test_list_k8s_clusters(self):
        clusters = self.client.list_k8s_clusters()
        self.assertGreater(len(clusters['items']), 0)

    def test_get_k8s_cluster(self):
        cluster = self.client.get_k8s_cluster(self.k8s_cluster['id'])
        self.assertEqual(cluster['id'], self.k8s_cluster['id'])

    def test_get_config(self):
        self.assertEqual(self.k8s_config['type'], 'kubeconfig')

    def test_update_k8s_cluster(self):
        name = "UPDATED_NAME"
        k8s_cluster = self.client.update_k8s_cluster(self.k8s_cluster['id'], name=name)
        # Wait for k8s cluster to be active
        self.client.wait_for(
            fn_request=lambda: self.client.list_k8s_clusters(),
            fn_check=lambda r: list(filter(
                lambda e: e['id'] == self.k8s_cluster['id'],
                r['items']
            ))[0]['metadata']['state'] == 'ACTIVE',
            scaleup=10000
        )
        self.assertEqual(k8s_cluster['properties']['name'], name)



if __name__ == '__main__':
    unittest.main()
