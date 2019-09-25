class cdrom:
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
        response = self._perform_request(
            '/datacenters/%s/servers/%s/cdroms?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

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
        response = self._perform_request(
            '/datacenters/%s/servers/%s/cdroms/%s' % (
                datacenter_id,
                server_id,
                cdrom_id))

        return response

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
        data = '{ "id": "' + cdrom_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/cdroms' % (
                datacenter_id,
                server_id),
            method='POST',
            data=data)

        return response

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
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/cdroms/%s' % (
                datacenter_id,
                server_id,
                cdrom_id),
            method='DELETE')

        return response
