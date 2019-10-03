import json


class firewall:
    def get_firewall_rule(self, datacenter_id,
                          server_id, nic_id, firewall_rule_id):
        """
        Retrieves a single firewall rule by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule_id: The unique ID of the firewall rule.
        :type       firewall_rule_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/nics/%s/firewallrules/%s' % (
                datacenter_id,
                server_id,
                nic_id,
                firewall_rule_id))

        return response

    def get_firewall_rules(self, datacenter_id, server_id, nic_id, depth=1):
        """
        Retrieves a list of firewall rules available in the account.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/nics/%s/firewallrules?depth=%s' % (
                datacenter_id,
                server_id,
                nic_id,
                str(depth)))

        return response

    def delete_firewall_rule(self, datacenter_id, server_id,
                             nic_id, firewall_rule_id):
        """
        Removes a firewall rule from the NIC.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule_id: The unique ID of the firewall rule.
        :type       firewall_rule_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s/firewallrules/%s' % (
                datacenter_id,
                server_id,
                nic_id,
                firewall_rule_id),
            method='DELETE')

        return response

    def create_firewall_rule(self, datacenter_id, server_id,
                             nic_id, firewall_rule):
        """
        Creates a firewall rule on the specified NIC and server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule: A firewall rule dict.
        :type       firewall_rule: ``dict``

        """
        properties = {
            "name": firewall_rule.name
        }

        if firewall_rule.protocol:
            properties['protocol'] = firewall_rule.protocol

        # Optional Properties
        if firewall_rule.source_mac:
            properties['sourceMac'] = firewall_rule.source_mac

        if firewall_rule.source_ip:
            properties['sourceIp'] = firewall_rule.source_ip

        if firewall_rule.target_ip:
            properties['targetIp'] = firewall_rule.target_ip

        if firewall_rule.port_range_start:
            properties['portRangeStart'] = firewall_rule.port_range_start

        if firewall_rule.port_range_end:
            properties['portRangeEnd'] = firewall_rule.port_range_end

        if firewall_rule.icmp_type:
            properties['icmpType'] = firewall_rule.icmp_type

        if firewall_rule.icmp_code:
            properties['icmpCode'] = firewall_rule.icmp_code

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s/firewallrules' % (
                datacenter_id,
                server_id,
                nic_id),
            method='POST',
            data=json.dumps(data))

        return response

    def update_firewall_rule(self, datacenter_id, server_id,
                             nic_id, firewall_rule_id, **kwargs):
        """
        Updates a firewall rule.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule_id: The unique ID of the firewall rule.
        :type       firewall_rule_id: ``str``

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

            if attr == 'source_mac':
                data['sourceMac'] = value
            elif attr == 'source_ip':
                data['sourceIp'] = value
            elif attr == 'target_ip':
                data['targetIp'] = value
            elif attr == 'port_range_start':
                data['portRangeStart'] = value
            elif attr == 'port_range_end':
                data['portRangeEnd'] = value
            elif attr == 'icmp_type':
                data['icmpType'] = value
            elif attr == 'icmp_code':
                data['icmpCode'] = value
            else:
                data[self._underscore_to_camelcase(attr)] = value

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s/firewallrules/%s' % (
                datacenter_id,
                server_id,
                nic_id,
                firewall_rule_id),
            method='PATCH',
            data=json.dumps(data))

        return response
