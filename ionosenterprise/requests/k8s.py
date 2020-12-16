import ionoscloud
from coreadaptor.IonosCoreProxy import IonosCoreProxy


class k8s:
    @IonosCoreProxy.process_response
    def get_k8s_cluster(self, k8s_cluster_id):
        """
        Retrieves a kubernetes cluster by its ID.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """

        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_find_by_clusterid_with_http_info(k8s_cluster_id, response_type='object')

    @IonosCoreProxy.process_response
    def list_k8s_clusters(self, depth=1):
        """
        Retrieves the list of kubernetes clusters.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_get_with_http_info(depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def create_k8s_cluster(self, name):
        """
        Creates a Kubernets cluster.

        :param      name: A Kubernetes Cluster Name. Valid Kubernetes
                          Cluster name must be 63 characters or less
                          and must be empty or begin and end with an
                          alphanumeric character ([a-z0-9A-Z]) with
                          dashes (-), underscores (_), dots (.), and
                          alphanumerics between.
        :type       name: ``str``

        """

        kubernetesCluster = ionoscloud.models.KubernetesCluster(
            properties={
                'name': name
            }
        )
        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_post_with_http_info(kubernetesCluster, response_type='object')

    @IonosCoreProxy.process_response
    def delete_k8s_cluster(self, k8s_cluster_id):
        """
        Removes a kubernetes cluster.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """

        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_delete_with_http_info(k8s_cluster_id)

    @IonosCoreProxy.process_response
    def update_k8s_cluster(self, k8s_cluster_id, **kwargs):
        """
        Replace all properties of a kubernetes cluster.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """

        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        kubernetesCluster = ionoscloud.models.KubernetesCluster(
            properties=data
        )
        return self.get_api_instance(ionoscloud.KubernetesApi).k8s_put_with_http_info(k8s_cluster_id, kubernetesCluster, response_type='object')