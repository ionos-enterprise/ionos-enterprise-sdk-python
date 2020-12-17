import ionoscloud
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class resource:
    @IonosCoreProxy.process_response
    def list_resources(self, resource_type=None, depth=1):
        """
        Retrieves a list of all resources.

        :param      resource_type: The resource type: datacenter,
                                   snapshot, image, ipblock, pcc,
                                   backupunit or k8s. Default is None,
                                   i.e., all resources are listed.
        :type       resource_type: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        if resource_type is not None:
            return self.get_api_instance(ionoscloud.UserManagementApi).um_resources_find_by_type_with_http_info(resource_type, depth=depth, response_type='object')
        else:
            return self.get_api_instance(ionoscloud.UserManagementApi).um_resources_get_with_http_info(depth=depth, response_type='object')

        # return response

    @IonosCoreProxy.process_response
    def get_resource(self, resource_type, resource_id, depth=1):
        """
        Retrieves a single resource of a particular type.

        :param      resource_type: The resource type: datacenter,
                                   snapshot, image, ipblock, pcc,
                                   backupunit or k8s.
        :type       resource_type: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionoscloud.UserManagementApi).um_resources_find_by_type_and_id_with_http_info(resource_type, resource_id, depth=depth, response_type='object')

# check
# test-volume
# test-k8s
# test k8s-nodepool
# test shares