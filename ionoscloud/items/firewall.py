class FirewallRule(object):
    def __init__(self, name=None, protocol=None,  # pylint: disable=unused-argument
                 source_mac=None, source_ip=None,
                 target_ip=None, port_range_start=None,
                 port_range_end=None, icmp_type=None,
                 icmp_code=None, **kwargs):
        """
        FirewallRule class initializer.

        :param      name: The name of the firewall rule.
        :type       name: ``str``

        :param      protocol: Either TCP or UDP
        :type       protocol: ``str``

        :param      source_mac: Source MAC you want to restrict.
        :type       source_mac: ``str``

        :param      source_ip: Source IP you want to restrict.
        :type       source_ip: ``str``

        :param      target_ip: Target IP you want to restrict.
        :type       target_ip: ``str``

        :param      port_range_start: Optional port range.
        :type       port_range_start: ``str``

        :param      port_range_end: Optional port range.
        :type       port_range_end: ``str``

        :param      icmp_type: Defines the allowed type.
        :type       icmp_type: ``str``

        :param      icmp_code: Defines the allowed code.
        :type       icmp_code: ``str``

        """
        self.name = name
        self.protocol = protocol
        self.source_mac = source_mac
        self.source_ip = source_ip
        self.target_ip = target_ip
        self.port_range_start = port_range_start
        self.port_range_end = port_range_end

        if icmp_type is not None:
            icmp_type = str(icmp_type)
        self.icmp_type = icmp_type

        if icmp_code is not None:
            icmp_code = str(icmp_code)
        self.icmp_code = icmp_code

    def __repr__(self):
        return (('<FirewallRule: name=%s, protocol=%s, source_mac=%s, '
                 'source_ip=%s, target_ip=%s, port_range_start=%s, '
                 'port_range_end=%s, icmp_type=%s, icmp_code=%s> ...>')
                % (self.name, self.protocol, self.source_mac,
                   self.source_ip, self.target_ip, self.port_range_start,
                   self.port_range_end, self.icmp_type, self.icmp_code))
