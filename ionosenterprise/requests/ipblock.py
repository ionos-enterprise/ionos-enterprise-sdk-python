import ionoscloud
from coreadaptor.IonosCoreProxy import IonosCoreProxy


class ipblock:
    @IonosCoreProxy.process_response
    def get_ipblock(self, ipblock_id):
        """
        Retrieves a single IP block by ID.

        :param      ipblock_id: The unique ID of the IP block.
        :type       ipblock_id: ``str``

        """
        return self.get_api_instance(ionoscloud.IPBlocksApi)\
            .ipblocks_find_by_id_with_http_info(ipblock_id, response_type='object')

    @IonosCoreProxy.process_response
    def list_ipblocks(self, depth=1):
        """
        Retrieves a list of IP blocks available in the account.

        """
        return self.get_api_instance(ionoscloud.IPBlocksApi)\
            .ipblocks_get_with_http_info(depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def delete_ipblock(self, ipblock_id):
        """
        Removes a single IP block from your account.

        :param      ipblock_id: The unique ID of the IP block.
        :type       ipblock_id: ``str``

        """
        return self.get_api_instance(ionoscloud.IPBlocksApi)\
            .ipblocks_delete_with_http_info(ipblock_id)

    @IonosCoreProxy.process_response
    def reserve_ipblock(self, ipblock):
        """
        Reserves an IP block within your account.

        """
        properties = {
            "name": ipblock.name
        }

        if ipblock.location:
            properties['location'] = ipblock.location

        if ipblock.size:
            properties['size'] = str(ipblock.size)

        ipblock = ionoscloud.models.IpBlock(
            properties=properties
        )

        return self.get_api_instance(ionoscloud.IPBlocksApi)\
            .ipblocks_post_with_http_info(ipblock, response_type='object')
