import ionos_cloud_sdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class volume:

    @IonosCoreProxy.process_response
    def get_volume(self, datacenter_id, volume_id):
        """
        Retrieves a single volume by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.VolumeApi).datacenters_volumes_find_by_id_with_http_info(datacenter_id, volume_id, response_type='object')

    @IonosCoreProxy.process_response
    def list_volumes(self, datacenter_id, depth=1):
        """
        Retrieves a list of volumes in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionos_cloud_sdk.VolumeApi).datacenters_volumes_get_with_http_info(datacenter_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def delete_volume(self, datacenter_id, volume_id):
        """
        Removes a volume from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.VolumeApi).datacenters_volumes_delete_with_http_info(datacenter_id, volume_id)


    @IonosCoreProxy.process_response
    def create_volume(self, datacenter_id, volume):
        """
        Creates a volume within the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume: A volume dict.
        :type       volume: ``dict``

        """

        ionos_cloud_sdk.models.VolumeProperties
        volume = ionos_cloud_sdk.models.Volume(
            **self._create_volume_dict(volume)
        )
        return self.get_api_instance(ionos_cloud_sdk.VolumeApi).datacenters_volumes_post_with_http_info(datacenter_id, volume)

    @IonosCoreProxy.process_response
    def update_volume(self, datacenter_id, volume_id, **kwargs):
        """
        Updates a volume

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        volume = ionos_cloud_sdk.models.VolumeProperties(**data)
        return self.get_api_instance(ionos_cloud_sdk.VolumeApi).datacenters_volumes_patch_with_http_info(datacenter_id, volume_id, volume)

    @IonosCoreProxy.process_response
    def get_attached_volumes(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of volumes attached to the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_volumes_get_with_http_info(datacenter_id, server_id, depth=depth)

    @IonosCoreProxy.process_response
    def get_attached_volume(self, datacenter_id, server_id, volume_id):
        """
        Retrieves volume information.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_volumes_find_by_id_with_http_info(datacenter_id, server_id, volume_id)

    @IonosCoreProxy.process_response
    def attach_volume(self, datacenter_id, server_id, volume_id):
        """
        Attaches a volume to a server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        volume = ionos_cloud_sdk.models.Volume(
            id=volume_id
        )
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_volumes_post_with_http_info(datacenter_id, server_id,
                                                                                         volume)

    @IonosCoreProxy.process_response
    def detach_volume(self, datacenter_id, server_id, volume_id):
        """
        Detaches a volume from a server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.ServerApi).datacenters_servers_volumes_delete_with_http_info(datacenter_id, server_id, volume_id)
