import ionos_cloud_sdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy
from ionos_cloud_sdk.models.private_cross_connect import PrivateCrossConnect
from ionos_cloud_sdk.models.private_cross_connect_properties import PrivateCrossConnectProperties

class pccs:
    @IonosCoreProxy.process_response
    def list_pccs(self, depth=1):
        """
        List Private Cross-Connects.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionos_cloud_sdk.PrivateCrossConnectApi).pccs_get_with_http_info(depth=depth,
                                                                                                   response_type='object')

    @IonosCoreProxy.process_response
    def create_pcc(self, pcc):
        """
        Create a Private Cross-Connect.

        :param      pcc: PrivateCrossConnect object: name, description.
        :type       pcc: ``PrivateCrossConnect instance``
        """
        pcc_dict = self._create_privatecrossconnect_dict(pcc)

        pcc = PrivateCrossConnect(**pcc_dict)

        return self.get_api_instance(ionos_cloud_sdk.PrivateCrossConnectApi).pccs_post_with_http_info(pcc,
                                                                                                response_type='object')

    @IonosCoreProxy.process_response
    def get_pcc(self, pcc_id, depth=1):
        """
        Retrieves a pcc by its ID.

        :param      pcc_id: The unique ID of the pcc.
        :type       pcc_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionos_cloud_sdk.PrivateCrossConnectApi).pccs_find_by_id_with_http_info(pcc_id,
                                                                                                          depth=depth,
                                                                                                          response_type='object')

    @IonosCoreProxy.process_response
    def delete_pcc(self, pcc_id):
        """
        Removes the pcc.

        :param      pcc_id: The unique ID of the pcc.
        :type       pcc_id: ``str``

        """
        return self.get_api_instance(ionos_cloud_sdk.PrivateCrossConnectApi).pccs_delete_with_http_info(pcc_id)

    @IonosCoreProxy.process_response
    def update_pcc(self, pcc_id, **kwargs):
        """
        Update private cross connect.

        :param      pcc_id: The unique ID of the pcc.
        :type       pcc_id: ``str``

        :param      kwargs: Fields to edit pcc.
        :type       kwargs: ``dict``

        """

        data = {}

        for attr, value in kwargs.items():
            data[attr] = value

        pccProperties = PrivateCrossConnectProperties(**data)

        return self.get_api_instance(ionos_cloud_sdk.PrivateCrossConnectApi).pccs_patch_with_http_info(pcc_id,
                                                                                                     pccProperties,
                                                                                                     response_type='object')
