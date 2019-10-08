class NIC(object):
    def __init__(self, name=None, ips=None,  # pylint: disable=unused-argument
                 dhcp=None, lan=None, firewall_active=None,
                 firewall_rules=None, nat=None, **kwargs):
        """
        NIC class initializer.

        :param      name: The name of the NIC.
        :type       name: ``str``

        :param      ips: A list of IPs.
        :type       ips: ``list``

        :param      dhcp: Enable or disable DHCP. Default is enabled.
        :type       dhcp: ``bool``

        :param      lan: ID of the LAN in which the NIC should reside.
        :type       lan: ``str``

        :param      nat: Enable or disable NAT. Default is disabled.
        :type       nat: ``bool``

        :param      firewall_active: Turns the firewall on or off;
                                     default is disabled.
        :type       firewall_active: ``bool``

        :param      firewall_rules: List of firewall rule dicts.
        :type       firewall_rules: ``list``

        """
        if firewall_rules is None:
            firewall_rules = []
        self.name = name
        self.nat = nat
        self.ips = ips
        self.dhcp = dhcp
        self.lan = lan
        self.firewall_active = firewall_active
        self.firewall_rules = firewall_rules

    def __repr__(self):
        return (('<NIC: name=%s, ips=%s, dhcp=%s,lan=%s, '
                 'firewall_active=%s> ...>')
                % (self.name, self.ips, str(self.dhcp),
                   self.lan, str(self.firewall_active)))
