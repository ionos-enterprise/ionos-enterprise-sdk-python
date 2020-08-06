from ..utils import find_item_by_name
import json


class backupunit:

    def list_backupunits(self, depth=1):
        """
        You can retrieve a complete list of backup Units that you have access to.

        """
        response = self._perform_request('/backupunits?depth=' + str(depth))

        return response

    def create_backupunit(self, backupunit):
        """
        Create a Backup Unit. A Backup Unit is considered a resource like a virtual datacenter, IP Block, snapshot, etc.
        It shall be shareable via groups inside our User Management Feature

        :param      backupunit: The backupunit object.
        :type       backupunit: ``dict``

        """
        data = json.dumps(self._create_backupunit_dict(backupunit))

        response = self._perform_request(
            url='/backupunits',
            method='POST',
            data=data)

        return response

    def get_backupunit(self, backupunit_id, depth=1):
        """
        Retrieve the details of an specific backup unit.

        """
        response = self._perform_request(
            '/backupunits/%s?depth=%s' % (backupunit_id, str(depth))
        )

        return response

    def update_backupunit(self, backupunit_id, **kwargs):
        """
        Partially modify a Backup Unit

        """
        data = {}

        for attr, value in kwargs.items():
            data[attr] = value

        request_data = json.dumps(
            {'properties': data}
        )

        response = self._perform_request(
            url='/backupunits/%s' % backupunit_id,
            method='PATCH',
            data=request_data)

        return response

    def update_backupunit_put(self, backupunit_id, **kwargs):
        """
        Modify a Backup Unit.

        """
        data = {}

        for attr, value in kwargs.items():
            data[attr] = value

        request_data = json.dumps(
            {'properties': data}
        )

        response = self._perform_request(
            url='/backupunits/%s' % backupunit_id,
            method='PUT',
            data=request_data)

        return response

    def delete_backupunit(self, backupunit_id):
        """
        Delete a Backup Unit.

        """

        response = self._perform_request(
            url='/backupunits/%s' % backupunit_id,
            method='DELETE')

        return response

    def get_ssourl(self, backupunit_id, depth=1):
        """
        Returns a single signon URL for the specified backup Unit.

        """
        response = self._perform_request(
            '/backupunits/%s/ssourl?depth=%s' % (backupunit_id, str(depth))
        )

        return response