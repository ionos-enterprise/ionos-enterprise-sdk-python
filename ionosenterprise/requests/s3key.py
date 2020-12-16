import ionoscloud
from coreadaptor.IonosCoreProxy import IonosCoreProxy
from ionoscloud.models.s3_key_properties import S3KeyProperties
from ionoscloud.models.s3_key import S3Key

class s3key:

    @IonosCoreProxy.process_response
    def list_s3keys(self, user_id, depth=1):
        """
        Retrieve a User's S3 keys

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionoscloud.UserManagementApi).um_users_s3keys_get_with_http_info(user_id, depth=depth,
                                                                                                     response_type='object')

    @IonosCoreProxy.process_response
    def create_s3key(self, user_id):
        """
        Create a S3 key for the given user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        return self.get_api_instance(ionoscloud.UserManagementApi).um_users_s3keys_post_with_http_info(user_id,
                                                                                                      response_type='object')

    @IonosCoreProxy.process_response
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
        return self.get_api_instance(ionoscloud.UserManagementApi).um_users_s3keys_find_by_key_id_with_http_info(user_id,
                                                                                                           key_id,
                                                                                                           depth=depth,
                                                                                                           response_type='object')

    @IonosCoreProxy.process_response
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
            data[attr] = value

        s3keyProperties = S3Key(properties = S3KeyProperties(**data))

        return self.get_api_instance(ionoscloud.UserManagementApi).um_users_s3keys_put_with_http_info(user_id,
                                                                                                           key_id,
                                                                                                       s3keyProperties,
                                                                                                       response_type='object')

    @IonosCoreProxy.process_response
    def delete_s3key(self, user_id, key_id):
        """
        Delete a S3 key

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      key_id: The unique ID of the key.
        :type       key_id: ``str``

        """
        return self.get_api_instance(ionoscloud.UserManagementApi).um_users_s3keys_delete_with_http_info(user_id,
                                                                                                           key_id)

    @IonosCoreProxy.process_response
    def get_s3ssourl(self, user_id):
        """
        Retrieve given S3 key belonging to the given User

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionoscloud.UserManagementApi).um_users_s3ssourl_get_with_http_info(user_id, response_type='object')
