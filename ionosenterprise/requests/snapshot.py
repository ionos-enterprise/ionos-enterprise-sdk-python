import json
from six.moves.urllib.parse import urlencode  # false positive, pylint: disable=import-error


class snapshot:
    def get_snapshot(self, snapshot_id):
        """
        Retrieves a single snapshot by ID.

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``

        """
        response = self._perform_request('/snapshots/%s' % snapshot_id)
        return response

    def list_snapshots(self, depth=1):
        """
        Retrieves a list of snapshots available in the account.

        """
        response = self._perform_request(
            '/snapshots?depth=%s' % str(depth))

        return response

    def delete_snapshot(self, snapshot_id):
        """
        Removes a snapshot from your account.

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``

        """
        response = self._perform_request(
            url='/snapshots/' + snapshot_id, method='DELETE')

        return response

    def update_snapshot(self, snapshot_id, **kwargs):
        """
        Removes a snapshot from your account.

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``
        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        response = self._perform_request(
            url='/snapshots/' + snapshot_id, method='PATCH', data=json.dumps(data))

        return response

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

        data = {'name': name, 'description': description}

        response = self._perform_request(
            '/datacenters/%s/volumes/%s/create-snapshot' % (
                datacenter_id, volume_id),
            method='POST-ACTION-JSON',
            data=urlencode(data))

        return response

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
        data = {'snapshotId': snapshot_id}

        response = self._perform_request(
            url='/datacenters/%s/volumes/%s/restore-snapshot' % (
                datacenter_id,
                volume_id),
            method='POST-ACTION',
            data=urlencode(data))

        return response

    def remove_snapshot(self, snapshot_id):
        """
        Removes a snapshot.

        :param      snapshot_id: The ID of the snapshot
                                 you wish to remove.
        :type       snapshot_id: ``str``

        """
        response = self._perform_request(
            url='/snapshots/' + snapshot_id, method='DELETE')

        return response
