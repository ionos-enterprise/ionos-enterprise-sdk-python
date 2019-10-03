class resource:
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
            response = self._perform_request(
                '/um/resources/%s?depth=%s' % (resource_type, str(depth)))
        else:
            response = self._perform_request(
                '/um/resources?depth=' + str(depth))

        return response

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
        response = self._perform_request(
            '/um/resources/%s/%s?depth=%s' % (
                resource_type, resource_id, str(depth)))

        return response
