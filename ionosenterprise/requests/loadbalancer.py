import json


class loadbalancer:
    def get_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Retrieves a single load balancer by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s' % (
                datacenter_id, loadbalancer_id))

        return response

    def list_loadbalancers(self, datacenter_id, depth=1):
        """
        Retrieves a list of load balancers in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers?depth=%s' % (
                datacenter_id, str(depth)))

        return response

    def delete_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Removes the load balancer from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s' % (
                datacenter_id, loadbalancer_id), method='DELETE')

        return response

    def create_loadbalancer(self, datacenter_id, loadbalancer):
        """
        Creates a load balancer within the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer: The load balancer object to be created.
        :type       loadbalancer: ``dict``

        """
        data = json.dumps(self._create_loadbalancer_dict(loadbalancer))

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers' % datacenter_id,
            method='POST',
            data=data)

        return response

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

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s' % (datacenter_id,
                                                      loadbalancer_id),
            method='PATCH',
            data=json.dumps(data))

        return response

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
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s/balancednics?depth=%s' % (
                datacenter_id, loadbalancer_id, str(depth)))

        return response

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
        data = '{ "id": "' + nic_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s/balancednics' % (
                datacenter_id,
                loadbalancer_id),
            method='POST',
            data=data)

        return response

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
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s/balancednics/%s?depth=%s' % (
                datacenter_id,
                loadbalancer_id,
                nic_id,
                str(depth)))

        return response

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
        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s/balancednics/%s' % (
                datacenter_id,
                loadbalancer_id,
                nic_id),
            method='DELETE')

        return response
