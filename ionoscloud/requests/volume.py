import json


class volume:
    def get_volume(self, datacenter_id, volume_id):
        """
        Retrieves a single volume by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/volumes/%s' % (datacenter_id, volume_id))

        return response

    def list_volumes(self, datacenter_id, depth=1):
        """
        Retrieves a list of volumes in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/volumes?depth=%s' % (datacenter_id, str(depth)))

        return response

    def delete_volume(self, datacenter_id, volume_id):
        """
        Removes a volume from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/volumes/%s' % (
                datacenter_id, volume_id), method='DELETE')

        return response

    def create_volume(self, datacenter_id, volume):
        """
        Creates a volume within the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume: A volume dict.
        :type       volume: ``dict``

        """

        data = (json.dumps(self._create_volume_dict(volume)))

        response = self._perform_request(
            url='/datacenters/%s/volumes' % datacenter_id,
            method='POST',
            data=data)

        return response

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

        response = self._perform_request(
            url='/datacenters/%s/volumes/%s' % (
                datacenter_id,
                volume_id),
            method='PATCH',
            data=json.dumps(data))

        return response

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
        response = self._perform_request(
            '/datacenters/%s/servers/%s/volumes?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

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
        response = self._perform_request(
            '/datacenters/%s/servers/%s/volumes/%s' % (
                datacenter_id,
                server_id,
                volume_id))

        return response

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
        data = '{ "id": "' + volume_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/volumes' % (
                datacenter_id,
                server_id),
            method='POST',
            data=data)

        return response

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
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/volumes/%s' % (
                datacenter_id,
                server_id,
                volume_id),
            method='DELETE')

        return response
