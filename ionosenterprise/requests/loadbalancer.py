import ionoscloud
from coreadaptor.IonosCoreProxy import IonosCoreProxy


class loadbalancer:
    @IonosCoreProxy.process_response
    def get_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Retrieves a single load balancer by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        return self.get_api_instance(ionoscloud.LoadBalancerApi).datacenters_loadbalancers_find_by_id_with_http_info(
            datacenter_id, loadbalancer_id, response_type='object')

    @IonosCoreProxy.process_response
    def list_loadbalancers(self, datacenter_id, depth=1):
        """
        Retrieves a list of load balancers in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionoscloud.LoadBalancerApi).datacenters_loadbalancers_get_with_http_info(
            datacenter_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def delete_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Removes the load balancer from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """

        return self.get_api_instance(ionoscloud.LoadBalancerApi).datacenters_loadbalancers_delete_with_http_info(
            datacenter_id, loadbalancer_id)

    @IonosCoreProxy.process_response
    def create_loadbalancer(self, datacenter_id, loadbalancer):
        """
        Creates a load balancer within the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer: The load balancer object to be created.
        :type       loadbalancer: ``dict``

        """

        loadbalancer = ionoscloud.models.Loadbalancer(
            **self._create_loadbalancer_dict(loadbalancer)
        )
        return self.get_api_instance(ionoscloud.LoadBalancerApi).datacenters_loadbalancers_post_with_http_info(datacenter_id, loadbalancer)

    @IonosCoreProxy.process_response
    def update_loadbalancer(self, datacenter_id,
                            loadbalancer_id, **kwargs):
        """
        Updates a load balancer

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        loadbalancer = ionoscloud.models.LoadbalancerProperties(
            **kwargs
        )
        return self.get_api_instance(ionoscloud.LoadBalancerApi).datacenters_loadbalancers_patch_with_http_info(
            datacenter_id, loadbalancer_id, loadbalancer)

    @IonosCoreProxy.process_response
    def get_loadbalancer_members(self, datacenter_id, loadbalancer_id,
                                 depth=1):
        """
        Retrieves the list of NICs that are associated with a load balancer.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionoscloud.LoadBalancerApi).datacenters_loadbalancers_balancednics_get_with_http_info(
            datacenter_id, loadbalancer_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def add_loadbalanced_nics(self, datacenter_id,
                              loadbalancer_id, nic_id):
        """
        Associates a NIC with the given load balancer.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The ID of the NIC.
        :type       nic_id: ``str``

        """

        nic = ionoscloud.models.Nic(
            id = nic_id
        )
        return self.get_api_instance(ionoscloud.LoadBalancerApi).datacenters_loadbalancers_balancednics_post_with_http_info(
            datacenter_id, loadbalancer_id, nic)

    @IonosCoreProxy.process_response
    def get_loadbalanced_nic(self, datacenter_id,
                             loadbalancer_id, nic_id, depth=1):
        """
        Gets the properties of a load balanced NIC.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionoscloud.LoadBalancerApi).datacenters_loadbalancers_balancednics_find_by_nic_id_with_http_info(
            datacenter_id, loadbalancer_id, nic_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def remove_loadbalanced_nic(self, datacenter_id,
                                loadbalancer_id, nic_id):
        """
        Removes a NIC from the load balancer.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """

        return self.get_api_instance(
            ionoscloud.LoadBalancerApi).datacenters_loadbalancers_balancednics_delete_with_http_info(
            datacenter_id, loadbalancer_id, nic_id)
