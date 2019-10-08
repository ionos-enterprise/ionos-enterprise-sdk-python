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

'''
This example will do the following:

- create a datacenter (name and location in variables datacenter_name and datacenter_location)
- wait for the datacenter to be active
- create a k8s cluster (cluster name in variable cluster_name)
- wait for the k8s cluster to be active
- retrieve the k8s cluster configuration
- create a k8s nodepool in the newly created k8s cluster
  (name and properties in variables pool_name and pool_properties)
- wait for the k8s nodepool to be active
- delete the k8s nodepool
- wait for the k8s nodepool to be deleted
- delete the k8s cluster
- wait for the k8s cluster to be deleted
- delete the datacenter
- wait for the datacenter to be deleted
'''

import os
import json
from ionosenterprise.client import IonosEnterpriseService, Datacenter


# ************* START CONFIG used for test **************
# ************* Update as needed           **************

datacenter_name = 'datacenter1'
datacenter_location = 'de/fra'
cluster_name = 'cluster1'
pool_name = 'pool1'
pool_properties = {
  'node_count': 4,
  'cpu_family': 'AMD_OPTERON',
  'cores_count': 2,
  'ram_size': 4096,
  'availability_zone': 'AUTO',
  'storage_type': 'SSD',
  'storage_size': 100
}

# ************* END CONFIG used for test   **************

username = os.getenv('IONOS_USERNAME', 'my_username')
password = os.getenv('IONOS_PASSWORD', 'my_password')

client = IonosEnterpriseService(
  username=username,
  password=password,
)

print('Creating datacenter named: %s in location: %s' % (datacenter_name, datacenter_location))
datacenter_props = {
  'name': datacenter_name,
  'location': datacenter_location
}
datacenter = client.create_datacenter(datacenter=Datacenter(**datacenter_props))
print('Request completed!')

print('Waiting for the datacenter to be active!')
datacenters = client.wait_for(
  fn_request=lambda: client.list_datacenters(),
  fn_check=lambda r: list(filter(
      lambda e: e['properties']['name'] == datacenter_name,
      r['items']
    ))[0]['metadata']['state'] == 'AVAILABLE',
  console_print='.',
  scaleup=10000
)
print('Datacenter active!')

datacenter_id = datacenter['id']

print('Using datacenter with ID: %s' % datacenter_id)

print('Creating K8S cluster named: %s' % cluster_name)
resp = client.create_k8s_cluster(cluster_name)
print('Request completed!')

print('Waiting for the cluster to be active!')
clusters = client.wait_for(
  fn_request=lambda: client.list_k8s_clusters(),
  fn_check=lambda r: list(filter(
      lambda e: e['properties']['name'] == cluster_name,
      r['items']
    ))[0]['metadata']['state'] == 'ACTIVE',
  console_print='.',
  scaleup=10000
)
print('Cluster active!')

my_cluster = list(filter(lambda e: e['properties']['name'] == cluster_name, clusters['items']))[0]
print(json.dumps(my_cluster, indent=4))

print('Getting cluster config!')
resp = client.get_k8s_config(my_cluster['id'])
print('Request completed!')

print(json.dumps(resp, indent=4))

print('Creating K8S nodepool named: %s' % pool_name)
resp = client.create_k8s_cluster_nodepool(
  my_cluster['id'],
  name=pool_name,
  datacenter_id=datacenter_id,
  **pool_properties
)
print('Request completed!')

print('Waiting for the nodepool to be active!')
pools = client.wait_for(
  fn_request=lambda: client.list_k8s_cluster_nodepools(my_cluster['id']),
  fn_check=lambda r: list(filter(
      lambda e: e['properties']['name'] == pool_name,
      r['items']
    ))[0]['metadata']['state'] == 'ACTIVE',
  console_print='.',
  scaleup=10000
)
print('Nodepool active!')

my_pool = list(filter(lambda e: e['properties']['name'] == pool_name, pools['items']))[0]
print(json.dumps(my_pool, indent=4))

print('Deleting K8S nodepool named: %s' % pool_name)
client.delete_k8s_cluster_nodepool(my_cluster['id'], my_pool['id'])
print('Request completed!')

print('Waiting for the nodepool to be deleted!')
clusters = client.wait_for(
  fn_request=lambda: client.list_k8s_cluster_nodepools(my_cluster['id']),
  fn_check=lambda r: len(list(filter(
      lambda e: e['properties']['name'] == pool_name,
      r['items']
    ))) == 0,
  console_print='.',
  scaleup=10000
)
print('Nodepool deleted!')

print('Deleting K8S cluster named: %s' % cluster_name)
client.delete_k8s_cluster(my_cluster['id'])
print('Request completed!')

print('Waiting for the cluster to be deleted!')
clusters = client.wait_for(
  fn_request=lambda: client.list_k8s_clusters(),
  fn_check=lambda r: len(list(filter(
      lambda e: e['properties']['name'] == cluster_name,
      r['items']
    ))) == 0,
  console_print='.',
  scaleup=10000
)
print('Cluster deleted!')

print('Deleting datacenter named: %s in location: %s' % (datacenter_name, datacenter_location))
client.delete_datacenter(datacenter_id)
print('Request completed!')

print('Waiting for the datacenter to be deleted!')
clusters = client.wait_for(
  fn_request=lambda: client.list_datacenters(),
  fn_check=lambda r: len(list(filter(
      lambda e: e['properties']['name'] == datacenter_name,
      r['items']
    ))) == 0,
  console_print='.',
  scaleup=10000
)
print('Datacenter deleted!')
