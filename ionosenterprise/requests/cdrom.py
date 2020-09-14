import ionos_cloud_sdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class cdrom:
    @IonosCoreProxy.process_response
    def get_attached_cdroms(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of CDROMs attached to the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_cdroms_get_with_http_info(datacenter_id, server_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def get_attached_cdrom(self, datacenter_id, server_id, cdrom_id):
        """
        Retrieves an attached CDROM.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      cdrom_id: The unique ID of the CDROM.
        :type       cdrom_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_cdroms_find_by_id_with_http_info(datacenter_id, server_id, cdrom_id, response_type='object')


    @IonosCoreProxy.process_response
    def attach_cdrom(self, datacenter_id, server_id, cdrom_id):
        """
        Attaches a CDROM to a server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      cdrom_id: The unique ID of the CDROM.
        :type       cdrom_id: ``str``

        """
        image = ionos_cloud_sdk.Image(id=cdrom_id)
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_cdroms_post_with_http_info(datacenter_id, server_id, image, response_type='object')

    @IonosCoreProxy.process_response
    def detach_cdrom(self, datacenter_id, server_id, cdrom_id):
        """
        Detaches a volume from a server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      cdrom_id: The unique ID of the CDROM.
        :type       cdrom_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_cdroms_delete_with_http_info(datacenter_id, server_id,
                                                                                               cdrom_id,
                                                                                               response_type='object')
