import json


class group:
    def list_groups(self, depth=1):
        """
        Retrieves a list of all groups.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/groups?depth=' + str(depth))

        return response

    def get_group(self, group_id, depth=1):
        """
        Retrieves a single group by ID.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/groups/%s?depth=%s' % (group_id, str(depth)))

        return response

    def create_group(self, group):
        """
        Creates a new group and set group privileges.

        :param      group: The group object to be created.
        :type       group: ``dict``

        """
        data = json.dumps(self._create_group_dict(group))

        response = self._perform_request(
            url='/um/groups',
            method='POST',
            data=data)

        return response

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

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/groups/%s' % group_id,
            method='PUT',
            data=json.dumps(data))

        return response

    def delete_group(self, group_id):
        """
        Removes a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        """
        response = self._perform_request(
            url='/um/groups/%s' % group_id,
            method='DELETE')

        return response
