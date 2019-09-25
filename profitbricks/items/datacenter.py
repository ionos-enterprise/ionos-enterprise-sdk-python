class Datacenter(object):
    def __init__(self, name=None, location=None,  # pylint: disable=unused-argument
                 description=None, volumes=None, servers=None, lans=None, loadbalancers=None,
                 **kwargs):
        """
        The Datacenter class initializer.

        :param      name: The data center name..
        :type       name: ``str``

        :param      location: The data center geographical location.
        :type       location: ``str``

        :param      description: Optional description.
        :type       description: ``str``

        :param      volumes: List of volume dicts.
        :type       volumes: ``list``

        :param      servers: List of server dicts.
        :type       servers: ``list``

        :param      lans: List of LAN dicts.
        :type       lans: ``list``

        :param      loadbalancers: List of load balancer dicts.
        :type       loadbalancers: ``list``

        """
        if volumes is None:
            volumes = []
        if servers is None:
            servers = []
        if lans is None:
            lans = []
        if loadbalancers is None:
            loadbalancers = []
        self.name = name
        self.description = description
        self.location = location
        self.servers = servers
        self.volumes = volumes
        self.lans = lans
        self.loadbalancers = loadbalancers

    def __repr__(self):
        return (('<Datacenter: name=%s, location=%s, description=%s> ...>')
                % (self.name, self.location, self.description))
