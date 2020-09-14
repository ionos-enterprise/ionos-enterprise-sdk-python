import ionos_cloud_sdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class nic:

    @IonosCoreProxy.process_response
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
        return self.get_api_instance(ionos_cloud_sdk.NicApi).datacenters_servers_nics_find_by_id_with_http_info(datacenter_id, server_id, nic_id,
                                                                                    depth=depth, response_type='object')

    @IonosCoreProxy.process_response
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
        return self.get_api_instance(ionos_cloud_sdk.NicApi).datacenters_servers_nics_get_with_http_info(datacenter_id, server_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
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

        return self.get_api_instance(ionos_cloud_sdk.NicApi).datacenters_servers_nics_delete_with_http_info(datacenter_id, server_id, nic_id)

    @IonosCoreProxy.process_response
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

        nic = ionos_cloud_sdk.models.Nic(
            **self._create_nic_dict(nic)
        )
        return self.get_api_instance(ionos_cloud_sdk.NicApi).datacenters_servers_nics_post_with_http_info(datacenter_id, server_id, nic, response_type='object')

    @IonosCoreProxy.process_response
    def update_nic(self, datacenter_id, server_id, nic_id, **kwargs):
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

        return self.get_api_instance(ionos_cloud_sdk.NicApi).datacenters_servers_nics_patch_with_http_info(datacenter_id, server_id, nic_id, data, response_type='object')
