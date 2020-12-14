import ionossdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class location:

    @IonosCoreProxy.process_response
    def get_location(self, location_id, depth=0):
        """
        Retrieves a single location by ID.

        :param      location_id: The unique ID of the location.
        :type       location_id: ``str``

        """
        return self.get_api_instance(ionossdk.LocationApi).locations_find_by_region_id_with_http_info(location_id, depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def list_locations(self, depth=0):
        """
        Retrieves a list of locations available in the account.

        """
        return self.get_api_instance(ionossdk.LocationApi).locations_get_with_http_info(depth=depth, response_type='object')

