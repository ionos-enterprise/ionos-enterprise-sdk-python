import ionossdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy


class user:

    @IonosCoreProxy.process_response
    def list_users(self, depth=1):
        """
        Retrieves a list of all users.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionossdk.UserManagementApi).um_users_get_with_http_info(depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def get_user(self, user_id, depth=1):
        """
        Retrieves a single user by ID.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionossdk.UserManagementApi).um_users_find_by_id_with_http_info(user_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def create_user(self, user):
        """
        Creates a new user.

        :param      user: The user object to be created.
        :type       user: ``dict``

        """
        data = self._create_user_dict(user=user)

        user = ionossdk.models.User(
            **data
        )
        return self.get_api_instance(ionossdk.UserManagementApi).um_users_post_with_http_info(user, response_type='object')

    @IonosCoreProxy.process_response
    def update_user(self, user_id, **kwargs):
        """
        Updates a user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        properties = {}

        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        user = ionossdk.models.User(properties=properties)
        return self.get_api_instance(ionossdk.UserManagementApi).um_users_put_with_http_info(user_id, user, response_type='object')

    @IonosCoreProxy.process_response
    def delete_user(self, user_id):
        """
        Removes a user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """

        return self.get_api_instance(ionossdk.UserManagementApi).um_users_delete_with_http_info(user_id)

    @IonosCoreProxy.process_response
    def list_group_users(self, group_id, depth=1):
        """
        Retrieves a list of all users that are members of a particular group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionossdk.UserManagementApi).um_groups_users_get_with_http_info(group_id, depth=depth, response_type='object')


    @IonosCoreProxy.process_response
    def add_group_user(self, group_id, user_id):
        """
        Adds an existing user to a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """

        user = ionossdk.models.User(id = user_id)
        return self.get_api_instance(ionossdk.UserManagementApi).um_groups_users_post_with_http_info(group_id, user, response_type='object')

    @IonosCoreProxy.process_response
    def remove_group_user(self, group_id, user_id):
        """
        Removes a user from a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """

        return self.get_api_instance(ionossdk.UserManagementApi).um_groups_users_delete_with_http_info(group_id, user_id)
