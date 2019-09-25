class LoadBalancer(object):
    """
    This is the main class for managing load balancer resources.
    """

    def __init__(self, name=None, ip=None,  # pylint: disable=unused-argument
                 dhcp=None, balancednics=None, **kwargs):
        """
        LoadBalancer class initializer.

        :param      name: The name of the load balancer.
        :type       name: ``str``

        :param      ip: The IP for the load balancer.
        :type       ip: ``str``

        :param      dhcp: Indicates if the load balancer
                          uses DHCP or not.
        :type       dhcp: ``bool``

        :param      balancednics: A list of NICs associated
                                  with the load balancer.
        :type       balancednics: ``list``

        """
        if balancednics is None:
            balancednics = []
        self.name = name
        self.ip = ip
        self.dhcp = dhcp
        self.balancednics = balancednics

    def __repr__(self):
        return (('<LoadBalancer: name=%s, ip=%s, dhcp=%s> ...>')
                % (self.name, self.ip, str(self.dhcp)))
