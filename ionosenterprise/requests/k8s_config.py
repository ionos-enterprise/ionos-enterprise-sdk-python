import ionos_cloud_sdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class k8s_config:
    @IonosCoreProxy.process_response
    def get_k8s_config(self, k8s_cluster_id):
        """
        Retrieves a kubernetes cluster config by its ID.

        :param      k8s_cluster_id: The unique ID of the cluster.
        :type       k8s_cluster_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.KubernetesApi).k8s_kubeconfig_get_with_http_info(k8s_cluster_id, response_type='object')
