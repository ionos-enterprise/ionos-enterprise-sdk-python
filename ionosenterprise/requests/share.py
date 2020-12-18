import ionoscloud
from coreadaptor.IonosCoreProxy import IonosCoreProxy


class share:
    @IonosCoreProxy.process_response
    def list_shares(self, group_id, depth=1):
        """
        Retrieves a list of all shares though a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionoscloud.UserManagementApi)\
            .um_groups_shares_get_with_http_info(group_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def get_share(self, group_id, resource_id, depth=1):
        """
        Retrieves a specific resource share available to a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionoscloud.UserManagementApi)\
            .um_groups_shares_find_by_resource_id_with_http_info(
            group_id, resource_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def add_share(self, group_id, resource_id, **kwargs):
        """
        Shares a resource through a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        properties = {}

        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        resource = ionoscloud.models.GroupShare(
            properties=properties
        )

        return self.get_api_instance(ionoscloud.UserManagementApi)\
            .um_groups_shares_post_with_http_info(group_id, resource_id, resource,
                                                  response_type='object')

    @IonosCoreProxy.process_response
    def update_share(self, group_id, resource_id, **kwargs):
        """
        Updates the permissions of a group for a resource share.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        properties = {}

        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        group_share = ionoscloud.models.GroupShare(
            properties=properties
        )
        return self.get_api_instance(ionoscloud.UserManagementApi)\
            .um_groups_shares_put_with_http_info(
            group_id, resource_id, group_share, response_type='object')

    @IonosCoreProxy.process_response
    def delete_share(self, group_id, resource_id):
        """
        Removes a resource share from a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """

        return self.get_api_instance(ionoscloud.UserManagementApi)\
            .um_groups_shares_delete_with_http_info(group_id, resource_id)
