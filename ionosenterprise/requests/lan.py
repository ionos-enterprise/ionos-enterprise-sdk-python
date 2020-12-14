import ionossdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy


class lan:

    @IonosCoreProxy.process_response
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

        return self.get_api_instance(ionossdk.LanApi).datacenters_lans_find_by_id_with_http_info(datacenter_id, lan_id,
                                                                                                depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def list_lans(self, datacenter_id, depth=1):
        """
        Retrieves a list of LANs available in the account.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionossdk.LanApi).datacenters_lans_get_with_http_info(datacenter_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def delete_lan(self, datacenter_id, lan_id):
        """
        Removes a LAN from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """

        return self.get_api_instance(ionossdk.LanApi).datacenters_lans_delete_with_http_info(datacenter_id, lan_id)

    @IonosCoreProxy.process_response
    def create_lan(self, datacenter_id, lan):
        """
        Creates a LAN in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan: The LAN object to be created.
        :type       lan: ``dict``

        """

        lan_properties = lan.__dict__
        del lan_properties['nics']
        lan = ionossdk.models.Lan(
            properties=lan_properties
        )
        return self.get_api_instance(ionossdk.LanApi).datacenters_lans_post_with_http_info(datacenter_id, lan, response_type='object')

    @IonosCoreProxy.process_response
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

        :param      pcc: Unique identifier of the private cross connect the given LAN is connected to if any
        :type       pcc: ``str``

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

        lan = ionossdk.models.LanProperties(
            **data
        )
        return self.get_api_instance(ionossdk.LanApi).datacenters_lans_patch_with_http_info(datacenter_id, lan_id, lan, response_type='object')

    @IonosCoreProxy.process_response
    def get_lan_members(self, datacenter_id, lan_id, depth=1):
        """
        Retrieves the list of NICs that are part of the LAN.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """

        return self.get_api_instance(ionossdk.LanApi).datacenters_lans_nics_get_with_http_info(datacenter_id, lan_id,
                                                                                                  depth=depth, response_type='object')
