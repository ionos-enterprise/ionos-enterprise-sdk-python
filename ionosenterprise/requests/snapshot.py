import ionossdk
from coreadaptor.IonosCoreProxy import IonosCoreProxy

class snapshot:

    @IonosCoreProxy.process_response
    def get_snapshot(self, snapshot_id):
        """
        Retrieves a single snapshot by ID.

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``

        """

        return self.get_api_instance(ionossdk.SnapshotApi).snapshots_find_by_id_with_http_info(snapshot_id, response_type='object')

    @IonosCoreProxy.process_response
    def list_snapshots(self, depth=1):
        """
        Retrieves a list of snapshots available in the account.

        """

        return self.get_api_instance(ionossdk.SnapshotApi).snapshots_get_with_http_info(depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def delete_snapshot(self, snapshot_id):
        """
        Removes a snapshot from your account.

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``

        """

        return self.get_api_instance(ionossdk.SnapshotApi).snapshots_delete_with_http_info(snapshot_id)

    @IonosCoreProxy.process_response
    def update_snapshot(self, snapshot_id, **kwargs):
        """
        Removes a snapshot from your account.

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``
        """

        snapshot = ionossdk.models.SnapshotProperties(**kwargs)
        return self.get_api_instance(ionossdk.SnapshotApi).snapshots_patch_with_http_info(snapshot_id, snapshot, response_type='object')

    @IonosCoreProxy.process_response
    def create_snapshot(self, datacenter_id, volume_id,
                        name=None, description=None):
        """
        Creates a snapshot of the specified volume.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        :param      name: The name given to the volume.
        :type       name: ``str``

        :param      description: The description given to the volume.
        :type       description: ``str``

        """

        return self.get_api_instance(ionossdk.VolumeApi)\
            .datacenters_volumes_create_snapshot_post_with_http_info(
            datacenter_id, volume_id, name=name, description=description, response_type='object')

    @IonosCoreProxy.process_response
    def restore_snapshot(self, datacenter_id, volume_id, snapshot_id):
        """
        Restores a snapshot to the specified volume.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``

        """

        return self.get_api_instance(ionossdk.VolumeApi).datacenters_volumes_restore_snapshot_post_with_http_info(
            datacenter_id, volume_id, snapshot_id = snapshot_id)

    @IonosCoreProxy.process_response
    def remove_snapshot(self, snapshot_id):
        """
        Removes a snapshot.

        :param      snapshot_id: The ID of the snapshot
                                 you wish to remove.
        :type       snapshot_id: ``str``

        """

        return self.get_api_instance(ionossdk.SnapshotApi).snapshots_delete_with_http_info(snapshot_id)
