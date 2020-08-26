import json


class lan:
    def get_lan(self, datacenter_id, lan_id, depth=1):
        """
        Retrieves a single LAN by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/lans/%s?depth=%s' % (
                datacenter_id,
                lan_id,
                str(depth)))

        return response

    def list_lans(self, datacenter_id, depth=1):
        """
        Retrieves a list of LANs available in the account.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/lans?depth=%s' % (
                datacenter_id,
                str(depth)))

        return response

    def delete_lan(self, datacenter_id, lan_id):
        """
        Removes a LAN from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/lans/%s' % (
                datacenter_id, lan_id), method='DELETE')

        return response

    def create_lan(self, datacenter_id, lan):
        """
        Creates a LAN in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan: The LAN object to be created.
        :type       lan: ``dict``

        """
        data = json.dumps(self._create_lan_dict(lan))

        response = self._perform_request(
            url='/datacenters/%s/lans' % datacenter_id,
            method='POST',
            data=data)

        return response

    def update_lan(self, datacenter_id, lan_id, name=None,
                   public=None, ip_failover=None, pcc=None):
        """
        Updates a LAN

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        :param      name: The new name of the LAN.
        :type       name: ``str``

        :param      public: Indicates if the LAN is public.
        :type       public: ``bool``

        :param      ip_failover: A list of IP fail-over dicts.
        :type       ip_failover: ``list``

        """
        data = {}

        if name:
            data['name'] = name

        if public is not None:
            data['public'] = public

        if ip_failover:
            data['ipFailover'] = ip_failover

        if pcc:
            data['pcc'] = pcc

        response = self._perform_request(
            url='/datacenters/%s/lans/%s' % (datacenter_id, lan_id),
            method='PATCH',
            data=json.dumps(data))

        return response

    def get_lan_members(self, datacenter_id, lan_id, depth=1):
        """
        Retrieves the list of NICs that are part of the LAN.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/lans/%s/nics?depth=%s' % (
                datacenter_id,
                lan_id,
                str(depth)))

        return response
