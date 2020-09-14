import ionos_cloud_sdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class group:

    @IonosCoreProxy.process_response
    def list_groups(self, depth=1):
        """
        Retrieves a list of all groups.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionos_cloud_sdk.UserManagementApi).um_groups_get_with_http_info(depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def get_group(self, group_id, depth=1):
        """
        Retrieves a single group by ID.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionos_cloud_sdk.UserManagementApi).um_groups_find_by_id_with_http_info(group_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def create_group(self, group):
        """
        Creates a new group and set group privileges.

        :param      group: The group object to be created.
        :type       group: ``dict``

        """

        group = ionos_cloud_sdk.models.Group(
            properties=self._create_group_dict(group)['properties']
        )
        return self.get_api_instance(ionos_cloud_sdk.UserManagementApi).um_groups_post_with_http_info(group, response_type='object')

    @IonosCoreProxy.process_response
    def update_group(self, group_id, **kwargs):
        """
        Updates a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        """
        properties = {}

        # make the key camel-case transformable
        if 'create_datacenter' in kwargs:
            kwargs['create_data_center'] = kwargs.pop('create_datacenter')

        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        group = ionos_cloud_sdk.models.Group(
            properties=properties
        )
        return self.get_api_instance(ionos_cloud_sdk.UserManagementApi).um_groups_put_with_http_info(group_id, group, response_type='object')

    @IonosCoreProxy.process_response
    def delete_group(self, group_id):
        """
        Removes a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.UserManagementApi).um_groups_delete_with_http_info(group_id)
