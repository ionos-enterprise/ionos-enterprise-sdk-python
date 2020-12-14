import ionossdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class contract:
    @IonosCoreProxy.process_response
    def list_contracts(self, depth=1):
        """
        Retrieves information about the resource limits
        for a particular contract and the current resource usage.

        """
        return self.get_api_instance(ionossdk.ContractApi).contracts_get_with_http_info(depth=depth, response_type='object')
