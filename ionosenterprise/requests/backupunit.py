import ionoscloud

from ionoscloud.models.backup_unit import BackupUnit
from ionoscloud.models.backup_unit_properties import BackupUnitProperties

from coreadaptor.IonosCoreProxy import IonosCoreProxy


class backupunit:

    @IonosCoreProxy.process_response
    def list_backupunits(self, depth=1):
        """
        You can retrieve a complete list of backup Units that you have access to.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionoscloud.BackupUnitApi).backupunits_get_with_http_info(depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def create_backupunit(self, backupunit):
        """
        Create a Backup Unit. A Backup Unit is considered a resource like a virtual datacenter, IP Block, snapshot, etc.
        It shall be shareable via groups inside our User Management Feature

        :param      backupunit: The backupunit object.
        :type       backupunit: ``dict``

        """
        data = self._create_backupunit_dict(backupunit)

        backupUnit = BackupUnit(**data)

        return self.get_api_instance(ionoscloud.BackupUnitApi).backupunits_post_with_http_info(backupUnit, response_type='object')

    @IonosCoreProxy.process_response
    def get_backupunit(self, backupunit_id, depth=1):
        """
        Retrieve the details of an specific backup unit.

        :param      backupunit_id: Id of the backup unit.
        :type       backupunit_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionoscloud.BackupUnitApi).backupunits_find_by_id_with_http_info(backupunit_id,
                                                                                                          depth=depth,
                                                                                                    response_type='object')

    @IonosCoreProxy.process_response
    def update_backupunit(self, backupunit_id, **kwargs):
        """
        Partially modify a Backup Unit

        :param      backupunit_id: The unique ID of the backupunit.
        :type       backupunit_id: ``str``

        :param      kwargs: Fields to edit backupunit.
        :type       kwargs: ``dict``

        """
        data = {}

        for attr, value in kwargs.items():
            data[attr] = value

        backupUnitProperties = BackupUnitProperties(**data)

        return self.get_api_instance(ionoscloud.BackupUnitApi).backupunits_patch_with_http_info(backupunit_id, backupUnitProperties, response_type='object')

    @IonosCoreProxy.process_response
    def update_backupunit_put(self, backupunit_id, **kwargs):
        """
        Modify a Backup Unit.

        :param      backupunit_id: The unique ID of the backupunit.
        :type       backupunit_id: ``str``

        :param      kwargs: Fields to edit backupunit.
        :type       kwargs: ``dict``

        """
        data = {}

        for attr, value in kwargs.items():
            data[attr] = value

        backupUnitProperties = BackupUnit(properties = BackupUnitProperties(**data))

        return self.get_api_instance(ionoscloud.BackupUnitApi).backupunits_put_with_http_info(backupunit_id,
                                                                                                     backupUnitProperties,
                                                                                                     response_type='object')


    @IonosCoreProxy.process_response
    def delete_backupunit(self, backupunit_id):
        """
        Delete a Backup Unit.

        :param      backupunit_id: The unique ID of the backupunit.
        :type       backupunit_id: ``str``

        """

        return self.get_api_instance(ionoscloud.BackupUnitApi).backupunits_delete_with_http_info(backupunit_id)


    @IonosCoreProxy.process_response
    def get_ssourl(self, backupunit_id):
        """
        Returns a single signon URL for the specified backup Unit.

        :param      backupunit_id: The unique ID of the backupunit.
        :type       backupunit_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """

        return self.get_api_instance(ionoscloud.BackupUnitApi).backupunits_ssourl_get_with_http_info(backupunit_id, response_type='object')
