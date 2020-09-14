import ionos_cloud_sdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class server:
    @IonosCoreProxy.process_response
    def list_servers(self, datacenter_id, depth=1):
        """
        Retrieves a list of all servers bound to the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_get_with_http_info(datacenter_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def get_server(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a server by its ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi)\
            .datacenters_servers_find_by_id_with_http_info(datacenter_id, server_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def delete_server(self, datacenter_id, server_id):
        """
        Removes the server from your data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """

        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_delete_with_http_info(datacenter_id, server_id)

    @IonosCoreProxy.process_response
    def create_server(self, datacenter_id, server):
        """
        Creates a server within the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server: A dict of the server to be created.
        :type       server: ``dict``

        """
        server = ionos_cloud_sdk.models.Server(
            **self._create_server_dict(server)
        )
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_post_with_http_info(datacenter_id, server, response_type='object')

    @IonosCoreProxy.process_response
    def update_server(self, datacenter_id, server_id, **kwargs):
        """
        Updates a server with the parameters provided.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        data = {}

        for attr, value in kwargs.items():
            if attr == 'boot_volume':
                boot_volume_properties = {
                    "id": value
                }
                boot_volume_entities = {
                    "bootVolume": boot_volume_properties
                }
                data.update(boot_volume_entities)
            else:
                data[self._underscore_to_camelcase(attr)] = value

        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_patch_with_http_info(datacenter_id, server_id, data, response_type='object')


    @IonosCoreProxy.process_response
    def start_server(self, datacenter_id, server_id):
        """
        Starts the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_start_post_with_http_info(datacenter_id, server_id)

    @IonosCoreProxy.process_response
    def stop_server(self, datacenter_id, server_id):
        """
        Stops the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_stop_post_with_http_info(datacenter_id, server_id)

    @IonosCoreProxy.process_response
    def reboot_server(self, datacenter_id, server_id):
        """
        Reboots the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_reboot_post_with_http_info(datacenter_id, server_id)
