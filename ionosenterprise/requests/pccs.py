from ..utils import find_item_by_name
import json


class pccs:
    def list_pccs(self, depth=1):
        """
        List Private Cross-Connects.

        """
        response = self._perform_request('/pccs?depth=' + str(depth))

        return response

    def create_pcc(self, pcc):
        """
        Create a Private Cross-Connect.
        """
        pcc_dict = self._create_privatecrossconnect_dict(pcc)
        response = self._perform_request(
            url='/pccs',
            method='POST',
            data=json.dumps(pcc_dict))

        return response

    def get_pcc(self, pcc_id, depth=1):
        """
        Retrieves a pcc by its ID.

        :param      pcc_id: The unique ID of the pcc.
        :type       pcc_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/pccs/%s?depth=%s' % (pcc_id, str(depth)))

        return response

    def delete_pcc(self, pcc_id):
        """
        Removes the pcc.

        :param      pcc_id: The unique ID of the pcc.
        :type       pcc_id: ``str``

        """
        response = self._perform_request(
            url='/pccs/%s' % (pcc_id),
            method='DELETE')

        return response

    def update_pcc(self, pcc_id, pcc):
        """
        Removes the pcc.

        :param      pcc_id: The unique ID of the pcc.
        :type       pcc_id: ``str``

        """

        data = self._create_privatecrossconnect_dict(pcc)

        response = self._perform_request(
            url='/pccs/%s' % (pcc_id),
            method='DELETE',
            data=json.dumps(data))

        return response

