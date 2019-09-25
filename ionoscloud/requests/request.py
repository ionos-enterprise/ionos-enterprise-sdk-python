class request:
    def get_request(self, request_id, status=False):
        """
        Retrieves a single request by ID.

        :param      request_id: The unique ID of the request.
        :type       request_id: ``str``

        :param      status: Retreive the full status of the request.
        :type       status: ``bool``

        """
        if status:
            response = self._perform_request(
                '/requests/' + request_id + '/status')
        else:
            response = self._perform_request(
                '/requests/%s' % request_id)

        return response

    def list_requests(self, depth=1):
        """
        Retrieves a list of requests available in the account.

        """
        response = self._perform_request(
            '/requests?depth=%s' % str(depth))

        return response
