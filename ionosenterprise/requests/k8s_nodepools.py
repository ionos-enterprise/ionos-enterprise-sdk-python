import ionoscloud
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
        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_nodepools_find_by_id_with_http_info(k8s_cluster_id,
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

        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_nodepools_delete_with_http_info(k8s_cluster_id,
                                                                                                    nodepool_id)

    @IonosCoreProxy.process_response
    def update_k8s_cluster_nodepool(self,
                                    k8s_cluster_id, nodepool_id, node_count,
                                    maintenance_window=None, auto_scaling=None, lan_ids=None, public_ips=None):
        """
        This will modify the Kubernetes Node Pool.
        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``
        :param      nodepool_id: The unique ID of the Kubernetes Node Pool
        :type       nodepool_id: ``str``
        :param      node_count: Number of nodes part of the Node Pool
        :type       node_count: ``int``
        :param      maintenance_window: MaintenanceWindow
        :type       maintenance_window: ``dict, e.g. {'dayOfTheWeek':'', 'time':''}``
                        dayOfTheWeek: The day of the week for a maintenance window.
                        dayOfTheWeek: ``str`` ["Monday",
                                            "Tuesday",
                                            "Wednesday",
                                            "Thursday",
                                            "Friday",
                                            "Saturday",
                                            "Sunday"]
                        time: The time to use for a maintenance window. Accepted formats are: HH:mm:ss; HH:mm:ss"Z";
                            HH:mm:ssZ. This time may varies by 15 minutes.
                        time: ``string``
        :param      auto_scaling: AutoScaling object
        :type       auto_scaling: ``dict`` {'minNodeCount': 2, 'maxNodeCount': 3}
                        minNodeCount": The minimum number of worker nodes that the managed node group can scale in.
                            Should be set together with 'maxNodeCount'.
                            Value for this attribute must be greater than equal to 1 and less than equal to maxNodeCount.
                        minNodeCount" : ``integer``
                        maxNodeCount: The maximum number of worker nodes that the managed node pool can scale-out.
                                Should be set together with 'minNodeCount'.
                                Value for this attribute must be greater than equal to 1 and minNodeCount.
                        maxNodeCount: ``integer``

        :param      lan_ids: array of additional LANs attached to worker nodes
        :type       lan_ids: ``list of ints``

        :param      public_ips: Optional array of reserved public IP addresses to be used by the nodes.
                        IPs must be from same location as the data center used for the node pool.
                        The array must contain one extra IP than maximum number of nodes could be.
                        (nodeCount+1 if fixed node amount or maxNodeCount+1 if auto scaling is used).
                        The extra provided IP Will be used during rebuilding of nodes.
        :type       public_ips: ``list``
        """

        properties = {node_count: node_count}

        if maintenance_window is not None:
            properties['maintenance_window'] = maintenance_window
        if auto_scaling is not None:
            properties['auto_scaling'] = auto_scaling
        if lan_ids is not None:
            properties['lans'] = [{'id': lan_id} for lan_id in lan_ids]
        if public_ips is not None:
            properties['public_ips'] = public_ips

        kubernetesNodePool = ionoscloud.models.KubernetesNodePool(
            properties=ionoscloud.models.KubernetesNodePoolProperties(
                **properties
            )
        )
        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_nodepools_put_with_http_info(k8s_cluster_id, nodepool_id, kubernetesNodePool, response_type='object')

    @IonosCoreProxy.process_response
    def list_k8s_cluster_nodepools(self, k8s_cluster_id, depth=1):
        """
        List Kubernetes Node Pools

        :param      k8s_cluster_id: The unique ID of the Kubernetes Cluster
        :type       k8s_cluster_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_nodepools_get_with_http_info(k8s_cluster_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def create_k8s_cluster_nodepool(self,
                                    k8s_cluster_id,
                                    name, datacenter_id,
                                    node_count, cpu_family,
                                    cores_count, ram_size,
                                    availability_zone,
                                    storage_type, storage_size,
                                    k8s_version=None, maintenance_window=None, auto_scaling=None,
                                    lan_ids=None, labels=None, annotations=None, public_ips=None):
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
        :param      k8s_version: Kubernetes version
        :type       k8s_version: ``str``
        :param      maintenance_window: MaintenanceWindow
        :type       maintenance_window: ``dict, e.g. {'dayOfTheWeek':'', 'time':''}``
                        dayOfTheWeek: The day of the week for a maintenance window.
                        dayOfTheWeek: ``str`` ["Monday",
                                            "Tuesday",
                                            "Wednesday",
                                            "Thursday",
                                            "Friday",
                                            "Saturday",
                                            "Sunday"]
                        time: The time to use for a maintenance window. Accepted formats are: HH:mm:ss; HH:mm:ss"Z";
                            HH:mm:ssZ. This time may varies by 15 minutes.
                        time: ``string``
        :param      auto_scaling: AutoScaling object
        :type       auto_scaling: ``dict`` {'minNodeCount': 2, 'maxNodeCount': 3}
                        minNodeCount": The minimum number of worker nodes that the managed node group can scale in.
                            Should be set together with 'maxNodeCount'.
                            Value for this attribute must be greater than equal to 1 and less than equal to maxNodeCount.
                        minNodeCount" : ``integer``
                        maxNodeCount: The maximum number of worker nodes that the managed node pool can scale-out.
                                Should be set together with 'minNodeCount'.
                                Value for this attribute must be greater than equal to 1 and minNodeCount.
                        maxNodeCount: ``integer``
        :param      lan_ids: array of additional LANs attached to worker nodes
        :type       lan_ids: ``list of ints``
        :param      labels: map of labels attached to node pool
        :type       labels: ``dict``
        :param      annotations: map of annotations attached to node pool
        :type       annotations: ``dict``
        :param      public_ips: Optional array of reserved public IP addresses to be used by the nodes.
                        IPs must be from same location as the data center used for the node pool.
                        The array must contain one extra IP than maximum number of nodes could be.
                        (nodeCount+1 if fixed node amount or maxNodeCount+1 if auto scaling is used).
                        The extra provided IP Will be used during rebuilding of nodes.
        :type       public_ips: ``list``
        """

        # mandatory fields
        properties = {
            'name': name,
            'datacenter_id': datacenter_id,
            'node_count': node_count,
            'cpu_family': cpu_family,
            'cores_count': cores_count,
            'ram_size': ram_size,
            'availability_zone': availability_zone,
            'storage_type': storage_type,
            'storage_size': storage_size
        }

        # optional fields
        if k8s_version is not None:
            properties['k8s_version'] = k8s_version
        if maintenance_window is not None:
            properties['maintenance_window'] = maintenance_window
        if auto_scaling is not None:
            properties['auto_scaling'] = auto_scaling
        if lan_ids is not None:
            properties['lans'] = [{'id':int(lan_id)} for lan_id in lan_ids]
        if labels is not None:
            properties['labels'] = labels
        if annotations is not None:
            properties['annotations'] = annotations
        if public_ips is not None:
            properties['public_ips'] = public_ips

        kubernetes_node_pool = ionoscloud.models.KubernetesNodePool(
            properties=ionoscloud.models.KubernetesNodePoolProperties(
                **properties
            )
        )

        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_nodepools_post_with_http_info(k8s_cluster_id, kubernetes_node_pool, response_type='object')
