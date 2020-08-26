import json

class s3key:
    def list_s3keys(self, user_id, depth=1):
        """
        Retrieve a User's S3 keys

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/users/%s/s3keys?depth=%s' % (user_id, str(depth)))

        return response

    def create_s3key(self, user_id):
        """
        Create a S3 key for the given user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        response = self._perform_request(
            url='/um/users/%s/s3keys' % user_id,
            method='POST')

        return response


    def get_s3key(self, user_id, key_id, depth=1):
        """
        Retrieve given S3 key belonging to the given User

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      key_id: The unique ID of the key.
        :type       key_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/users/%s/s3keys/%s?depth=%s' % (user_id, key_id, str(depth)))

        return response

    def update_s3key(self, user_id, key_id, **kwargs):
        """
        Modify a S3 key having the given key id

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      key_id: The unique ID of the key.
        :type       key_id: ``str``

        :param      kwargs: arguments active.
        :type       kwargs: ``dict``

        """

        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        response = self._perform_request(
            url = '/um/users/%s/s3keys/%s' % (user_id, key_id),
            method='PUT',
            data=json.dumps({'properties':data})
        )

        return response

    def delete_s3key(self, user_id, key_id):
        """
        Delete a S3 key

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      key_id: The unique ID of the key.
        :type       key_id: ``str``

        """

        response = self._perform_request(
            url='/um/users/%s/s3keys/%s' % (user_id, key_id),
            method='DELETE')

        return response

    def get_s3ssourl(self, user_id, depth=1):
        """
        Retrieve given S3 key belonging to the given User

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/users/%s/s3ssourl?depth=%s' % (user_id, str(depth)))
        return response