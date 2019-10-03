class k8s_config:
    def get_k8s_config(self, k8s_cluster_id):
        """
        Retrieves a kubernetes cluster config by its ID.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """
        response = self._perform_request('/k8s/%s/kubeconfig' % k8s_cluster_id)
        return response
