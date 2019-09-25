class location:
    def get_location(self, location_id, depth=0):
        """
        Retrieves a single location by ID.

        :param      location_id: The unique ID of the location.
        :type       location_id: ``str``

        """
        response = self._perform_request('/locations/%s?depth=%s' % (location_id, depth))
        return response

    def list_locations(self, depth=0):
        """
        Retrieves a list of locations available in the account.

        """
        response = self._perform_request('/locations?depth=%s' % (depth))

        return response
