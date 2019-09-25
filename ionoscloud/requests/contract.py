class contract:
    def list_contracts(self, depth=1):
        """
        Retrieves information about the resource limits
        for a particular contract and the current resource usage.

        """
        response = self._perform_request('/contracts?depth=' + str(depth))

        return response
