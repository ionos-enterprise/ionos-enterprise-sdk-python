import json


class server:
    def list_servers(self, datacenter_id, depth=1):
        """
        Retrieves a list of all servers bound to the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/servers?depth=%s' % (datacenter_id, str(depth)))

        return response

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
        response = self._perform_request(
            '/datacenters/%s/servers/%s?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

    def delete_server(self, datacenter_id, server_id):
        """
        Removes the server from your data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s' % (
                datacenter_id,
                server_id),
            method='DELETE')

        return response

    def create_server(self, datacenter_id, server):
        """
        Creates a server within the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server: A dict of the server to be created.
        :type       server: ``dict``

        """

        data = json.dumps(self._create_server_dict(server))

        response = self._perform_request(
            url='/datacenters/%s/servers' % (datacenter_id),
            method='POST',
            data=data)

        return response

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

        response = self._perform_request(
            url='/datacenters/%s/servers/%s' % (
                datacenter_id,
                server_id),
            method='PATCH',
            data=json.dumps(data))

        return response

    def start_server(self, datacenter_id, server_id):
        """
        Starts the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/start' % (
                datacenter_id,
                server_id),
            method='POST-ACTION')

        return response

    def stop_server(self, datacenter_id, server_id):
        """
        Stops the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/stop' % (
                datacenter_id,
                server_id),
            method='POST-ACTION')

        return response

    def reboot_server(self, datacenter_id, server_id):
        """
        Reboots the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/reboot' % (
                datacenter_id,
                server_id),
            method='POST-ACTION')

        return response
