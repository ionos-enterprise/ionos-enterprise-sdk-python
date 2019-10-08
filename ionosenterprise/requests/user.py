import json


class user:
    def list_users(self, depth=1):
        """
        Retrieves a list of all users.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/users?depth=' + str(depth))

        return response

    def get_user(self, user_id, depth=1):
        """
        Retrieves a single user by ID.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/users/%s?depth=%s' % (user_id, str(depth)))

        return response

    def create_user(self, user):
        """
        Creates a new user.

        :param      user: The user object to be created.
        :type       user: ``dict``

        """
        data = self._create_user_dict(user=user)

        response = self._perform_request(
            url='/um/users',
            method='POST',
            data=json.dumps(data))

        return response

    def update_user(self, user_id, **kwargs):
        """
        Updates a user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        properties = {}

        for attr, value in kwargs.items():
            properties[self._underscore_to_camelcase(attr)] = value

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/users/%s' % user_id,
            method='PUT',
            data=json.dumps(data))

        return response

    def delete_user(self, user_id):
        """
        Removes a user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        response = self._perform_request(
            url='/um/users/%s' % user_id,
            method='DELETE')

        return response

    def list_group_users(self, group_id, depth=1):
        """
        Retrieves a list of all users that are members of a particular group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/groups/%s/users?depth=%s' % (group_id, str(depth)))

        return response

    def add_group_user(self, group_id, user_id):
        """
        Adds an existing user to a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        data = {
            "id": user_id
        }

        response = self._perform_request(
            url='/um/groups/%s/users' % group_id,
            method='POST',
            data=json.dumps(data))

        return response

    def remove_group_user(self, group_id, user_id):
        """
        Removes a user from a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        response = self._perform_request(
            url='/um/groups/%s/users/%s' % (group_id, user_id),
            method='DELETE')

        return response
