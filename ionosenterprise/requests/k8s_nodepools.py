import ionos_cloud_sdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy


class k8s_nodepools:

    @IonosCoreProxy.process_response
    def get_k8s_cluster_nodepool(self, k8s_cluster_id, nodepool_id):
        """
        Retrieve Kubernetes Node Pool

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      nodepool_id: The unique ID of the Kubernetes Node Pool
        :type       nodepool_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.KubernetesApi).k8s_nodepools_find_by_id_with_http_info(k8s_cluster_id,
                                                                                                       nodepool_id, response_type='object')

    @IonosCoreProxy.process_response
    def delete_k8s_cluster_nodepool(self, k8s_cluster_id, nodepool_id):
        """
        Delete Kubernetes Node Pool

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      nodepool_id: The unique ID of the Kubernetes Node Pool
        :type       nodepool_id: ``str``

        """

        return self.get_api_instance(ionos_cloud_sdk.KubernetesApi).k8s_nodepools_delete_with_http_info(k8s_cluster_id,
                                                                                                    nodepool_id)

    @IonosCoreProxy.process_response
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

        kubernetesNodePool = ionos_cloud_sdk.models.KubernetesNodePool(
            properties={
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
        )
        return self.get_api_instance(ionos_cloud_sdk.KubernetesApi).k8s_nodepools_put_with_http_info(k8s_cluster_id, nodepool_id, kubernetesNodePool, response_type='object')

    @IonosCoreProxy.process_response
    def list_k8s_cluster_nodepools(self, k8s_cluster_id, depth=1):
        """
        List Kubernetes Node Pools

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionos_cloud_sdk.KubernetesApi).k8s_nodepools_get_with_http_info(k8s_cluster_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
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
        kubernetes_node_pool_properties = ionos_cloud_sdk.models.KubernetesNodePool(
            properties={
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
        )

        return self.get_api_instance(ionos_cloud_sdk.KubernetesApi).k8s_nodepools_post_with_http_info(k8s_cluster_id, kubernetes_node_pool_properties, response_type='object')
