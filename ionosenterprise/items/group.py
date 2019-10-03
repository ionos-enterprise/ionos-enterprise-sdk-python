class Group(object):
    def __init__(self, name=None, create_datacenter=None,
                 create_snapshot=None, reserve_ip=None,
                 access_activity_log=None):
        """
        Group class initializer.

        :param      name: The name of the group.
        :type       name: ``str``

        :param      create_datacenter: Indicates if the group is allowed
                                       to create virtual data centers.
        :type       create_datacenter: ``bool``

        :param      create_snapshot: Indicates if the group is allowed
                                     to create snapshots.
        :type       create_snapshot: ``bool``

        :param      reserve_ip: Indicates if the group is allowed
                                to reserve IP addresses.
        :type       reserve_ip: ``bool``

        :param      access_activity_log: Indicates if the group is allowed
                                         to access activity log.
        :type       access_activity_log: ``bool``

        """
        self.name = name
        self.create_datacenter = create_datacenter
        self.create_snapshot = create_snapshot
        self.reserve_ip = reserve_ip
        self.access_activity_log = access_activity_log

    def __repr__(self):
        return ('<Group: name=%s, create_datacenter=%s, create_snapshot=%s, '
                'reserve_ip=%s, access_activity_log=%s>'
                % (self.name, str(self.create_datacenter),
                   str(self.create_snapshot), str(self.reserve_ip),
                   str(self.access_activity_log)))
