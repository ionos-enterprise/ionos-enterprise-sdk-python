import json


class nic:
    def get_nic(self, datacenter_id, server_id, nic_id, depth=1):
        """
        Retrieves a NIC by its ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/nics/%s?depth=%s' % (
                datacenter_id,
                server_id,
                nic_id,
                str(depth)))

        return response

    def list_nics(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of all NICs bound to the specified server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/nics?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

    def delete_nic(self, datacenter_id, server_id, nic_id):
        """
        Removes a NIC from the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s' % (
                datacenter_id,
                server_id,
                nic_id),
            method='DELETE')

        return response

    def create_nic(self, datacenter_id, server_id, nic):
        """
        Creates a NIC on the specified server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic: A NIC dict.
        :type       nic: ``dict``

        """

        data = json.dumps(self._create_nic_dict(nic))

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics' % (
                datacenter_id,
                server_id),
            method='POST',
            data=data)

        return response

    def update_nic(self, datacenter_id, server_id,
                   nic_id, **kwargs):
        """
        Updates a NIC with the parameters provided.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s' % (
                datacenter_id,
                server_id,
                nic_id),
            method='PATCH',
            data=json.dumps(data))

        return response
