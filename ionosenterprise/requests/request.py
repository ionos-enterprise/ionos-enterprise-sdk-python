import ionossdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class request:
    @IonosCoreProxy.process_response
    def get_request(self, request_id, status=False):
        """
        Retrieves a single request by ID.

        :param      request_id: The unique ID of the request.
        :type       request_id: ``str``

        :param      status: Retreive the full status of the request.
        :type       status: ``bool``

        """

        if status:
            return self.get_api_instance(ionossdk.RequestApi).requests_status_get_with_http_info(request_id, response_type='object')
        else:
            return self.get_api_instance(ionossdk.RequestApi).requests_find_by_id_with_http_info(request_id, response_type='object')

    @IonosCoreProxy.process_response
    def list_requests(self, depth=1):
        """
        Retrieves a list of requests available in the account.

        """

        return self.get_api_instance(ionossdk.RequestApi).requests_get_with_http_info(depth=depth, response_type='object')
