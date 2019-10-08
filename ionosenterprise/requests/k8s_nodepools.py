import json


class k8s_nodepools:
    def get_k8s_cluster_nodepool(self, k8s_cluster_id, nodepool_id):
        """
        Retrieve Kubernetes Node Pool

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      nodepool_id: The unique ID of the Kubernetes Node Pool
        :type       nodepool_id: ``str``

        """

        response = self._perform_request(
            '/k8s/%s/nodepools/%s' %
            (k8s_cluster_id, nodepool_id)
        )

        return response

    def delete_k8s_cluster_nodepool(self, k8s_cluster_id, nodepool_id):
        """
        Delete Kubernetes Node Pool

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      nodepool_id: The unique ID of the Kubernetes Node Pool
        :type       nodepool_id: ``str``

        """

        response = self._perform_request(
            url='/k8s/%s/nodepools/%s' %
            (k8s_cluster_id, nodepool_id),
            method='DELETE'
        )

        return response

    def update_k8s_cluster_nodepool(self,
                                    k8s_cluster_id, nodepool_id,
                                    name, datacenter_id,
                                    node_count, cpu_family,
                                    cores_count, ram_size,
                                    availability_zone,
                                    storage_type, storage_size):
        """
        This will modify the Kubernetes Node Pool.

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      nodepool_id: The unique ID of the Kubernetes Node Pool
        :type       nodepool_id: ``str``

        :param      name: A Kubernetes Node Pool Name. Valid Kubernetes
                          Node Pool name must be 63 characters or less
                          and must be empty or begin and end with an
                          alphanumeric character ([a-z0-9A-Z]) with
                          dashes (-), underscores (_), dots (.), and
                          alphanumerics between.
        :type       name: ``str``

        :param      datacenter_id: A valid uuid of the datacenter on which user has access
        :type       datacenter_id: ``str``

        :param      node_count: Number of nodes part of the Node Pool
        :type       node_count: ``int``

        :param      cpu_family: A valid cpu family name
        :type       cpu_family: ``str``

        :param      cores_count: Number of cores for node
        :type       cores_count: ``int``

        :param      ram_size: RAM size for node, minimum size 2048MB is recommended
        :type       ram_size: ``int``

        :param      availability_zone: The availability zone in which the server should exist
        :type       availability_zone: ``str``

        :param      storage_type: Hardware type of the volume
        :type       storage_type: ``str``

        :param      storage_size: The size of the volume in GB. The size
                                  should be greater than 10GB
        :type       storage_size: ``int``

        """

        data = {
            'properties': {
                'name': name,
                'datacenterId': datacenter_id,
                'nodeCount': node_count,
                'cpuFamily': cpu_family,
                'coresCount': cores_count,
                'ramSize': ram_size,
                'availabilityZone': availability_zone,
                'storageType': storage_type,
                'storageSize': storage_size
            }
        }

        response = self._perform_request(
            url='/k8s/%s/nodepools/%s' % (k8s_cluster_id, nodepool_id),
            method='PUT',
            data=json.dumps(data)
        )

        return response

    def list_k8s_cluster_nodepools(self, k8s_cluster_id, depth=1):
        """
        List Kubernetes Node Pools

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        response = self._perform_request(
            url='/k8s/%s/nodepools?depth=%s' % (k8s_cluster_id, str(depth))
        )

        return response

    def create_k8s_cluster_nodepool(self,
                                    k8s_cluster_id,
                                    name, datacenter_id,
                                    node_count, cpu_family,
                                    cores_count, ram_size,
                                    availability_zone,
                                    storage_type, storage_size):
        """
        This will create a new Kubernetes Node Pool inside a Kubernetes Cluster.

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      nodepool_id: The unique ID of the Kubernetes Node Pool
        :type       nodepool_id: ``str``

        :param      name: A Kubernetes Node Pool Name. Valid Kubernetes
                          Node Pool name must be 63 characters or less
                          and must be empty or begin and end with an
                          alphanumeric character ([a-z0-9A-Z]) with
                          dashes (-), underscores (_), dots (.), and
                          alphanumerics between.
        :type       name: ``str``

        :param      datacenter_id: A valid uuid of the datacenter on which user has access
        :type       datacenter_id: ``str``

        :param      node_count: Number of nodes part of the Node Pool
        :type       node_count: ``int``

        :param      cpu_family: A valid cpu family name
        :type       cpu_family: ``str``

        :param      cores_count: Number of cores for node
        :type       cores_count: ``int``

        :param      ram_size: RAM size for node, minimum size 2048MB is recommended
        :type       ram_size: ``int``

        :param      availability_zone: The availability zone in which the server should exist
        :type       availability_zone: ``str``

        :param      storage_type: Hardware type of the volume
        :type       storage_type: ``str``

        :param      storage_size: The size of the volume in GB. The size
                                  should be greater than 10GB
        :type       storage_size: ``int``

        """

        data = {
            'properties': {
                'name': name,
                'datacenterId': datacenter_id,
                'nodeCount': node_count,
                'cpuFamily': cpu_family,
                'coresCount': cores_count,
                'ramSize': ram_size,
                'availabilityZone': availability_zone,
                'storageType': storage_type,
                'storageSize': storage_size
            }
        }

        response = self._perform_request(
            url='/k8s/%s/nodepools' % k8s_cluster_id,
            method='POST',
            data=json.dumps(data)
        )

        return response
