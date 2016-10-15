import base64
import json
import re

import requests
import six
from six.moves.urllib.parse import urlencode

from profitbricks import (
    API_HOST, __version__
)

"""ProfitBricks Object Classes
"""


class ProfitBricksService(object):
    """
        ProfitBricksClient Base Class
    """

    def __init__(self, username=None, password=None, host_base=API_HOST,
                 host_cert=None, ssl_verify=True, headers=dict()):
        self.username = username
        self.password = password
        self.host_base = host_base
        self.host_cert = host_cert
        self.verify = ssl_verify
        self.headers = headers

    """Datacenter Functions
    """

    def get_datacenter(self, datacenter_id, depth=1):
        """
        Retrieves a datacenter by its ID.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s?depth=%s' % (datacenter_id, str(depth)))

        return response

    def list_datacenters(self, depth=1):
        """
        Retrieves a list of all datacenters.

        """
        response = self._perform_request('/datacenters?depth=' + str(depth))

        return response

    def delete_datacenter(self, datacenter_id):
        """
        Removes the server from your Datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s' % (datacenter_id),
            type='DELETE')

        return response

    def create_datacenter(self, datacenter):
        """
        Creates a Datacenter -- both simple and complex are supported.

        """
        server_items = []
        volume_items = []
        lan_items = []
        loadbalancer_items = []

        entities = dict()

        properties = {
            "name": datacenter.name,
            "location": datacenter.location,
        }

        ' Optional Properties'
        if datacenter.description:
            properties['description'] = datacenter.description

        ' Servers '
        if len(datacenter.servers) > 0:
            for server in datacenter.servers:
                server_items.append(self._create_server_dict(server))

            servers = {
                "items": server_items
            }

            server_entities = {
                "servers": servers
            }

            entities.update(server_entities)

        ' Volumes '
        if len(datacenter.volumes) > 0:
            for volume in datacenter.volumes:
                volume_items.append(self._create_volume_dict(volume))

            volumes = {
                "items": volume_items
            }

            volume_entities = {
                "volumes": volumes
            }

            entities.update(volume_entities)

        ' Load Balancers '
        if len(datacenter.loadbalancers) > 0:
            for loadbalancer in datacenter.loadbalancers:
                loadbalancer_items.append(
                    self._create_loadbalancer_dict(
                        loadbalancer
                    )
                )

            loadbalancers = {
                "items": loadbalancer_items
            }

            loadbalancer_entities = {
                "loadbalancers": loadbalancers
            }

            entities.update(loadbalancer_entities)

        ' LANs '
        if len(datacenter.lans) > 0:
            for lan in datacenter.lans:
                lan_items.append(
                    self._create_lan_dict(lan)
                )

            lans = {
                "items": lan_items
            }

            lan_entities = {
                "lans": lans
            }

            entities.update(lan_entities)

        if len(entities) == 0:
            raw = {
                "properties": properties,
            }
        else:
            raw = {
                "properties": properties,
                "entities": entities
            }

        data = json.dumps(raw)

        response = self._perform_request(
            url='/datacenters',
            type='POST',
            data=data)

        return response

    def update_datacenter(self, datacenter_id, **kwargs):
        """
        Updates a server with the parameters provided.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s' % (
                datacenter_id),
            type='PATCH',
            data=json.dumps(data))

        return response

    """FirewallRule Functions
    """

    def get_firewall_rule(self, datacenter_id,
                          server_id, nic_id, firewall_rule_id):
        """
        Retrieves a single FirewallRule by ID.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule_id: The unique ID of the FirewallRule.
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
        Retrieves a list of FirewallRules available in the account.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

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
        Removes a Firewall rule from the NIC.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule_id: The unique ID of the FirewallRule.
        :type       firewall_rule_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s/firewallrules/%s' % (
                datacenter_id,
                server_id,
                nic_id,
                firewall_rule_id),
            type='DELETE')

        return response

    def create_firewall_rule(self, datacenter_id, server_id,
                             nic_id, firewall_rule):
        """
        Creates a firewall rule on the specified NIC and Server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the Server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule: A FirewallRule dict.
        :type       firewall_rule: ``dict``

        """
        properties = {
            "name": firewall_rule.name,
            "protocol": firewall_rule.protocol,
        }

        ' Optional Properties'
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
            type='POST',
            data=json.dumps(data))

        return response

    def update_firewall_rule(self, datacenter_id, server_id,
                             nic_id, firewall_rule_id, **kwargs):
        """
        Updates a firewall rule.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      firewall_rule_id: The unique ID of the firewall.
        :type       firewall_rule_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

            if attr == 'source_mac':
                data['sourceMac'] = kwargs[attr]
            elif attr == 'source_ip':
                data['sourceIp'] = kwargs[attr]
            elif attr == 'target_ip':
                data['targetIp'] = kwargs[attr]
            elif attr == 'port_range_start':
                data['portRangeStart'] = kwargs[attr]
            elif attr == 'port_range_end':
                data['portRangeEnd'] = kwargs[attr]
            elif attr == 'icmp_type':
                data['icmpType'] = kwargs[attr]
            elif attr == 'icmp_code':
                data['icmpCode'] = kwargs[attr]
            else:
                data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s/firewallrules/%s' % (
                datacenter_id,
                server_id,
                nic_id,
                firewall_rule_id),
            type='PATCH',
            data=json.dumps(data))

        return response

    """Image Functions
    """

    def get_image(self, image_id):
        """
        Retrieves a single image by ID.

        :param      image_id: The unique ID of the image.
        :type       image_id: ``str``

        """
        response = self._perform_request('/images/%s' % image_id)
        return response

    def list_images(self, depth=1):
        """
        Retrieves a list of images available in the datacenter.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/images?depth=' + str(depth))
        return response

    def delete_image(self, image_id):
        """
        Removes only user created images.

        :param      image_id: The unique ID of the image.
        :type       image_id: ``str``

        """
        response = self._perform_request(url='/images/' + image_id,
                                         type='DELETE')
        return response

    def update_image(self, image_id, **kwargs):
        """
        Replace all properties of an image.

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(url='/images/' + image_id,
                                         type='PATCH',
                                         data=json.dumps(data))
        return response

    """IPBlock Functions
    """

    def get_ipblock(self, ipblock_id):
        """
        Retrieves a single IPBlock by ID.

        :param      ipblock_id: The unique ID of the IPBlock.
        :type       ipblock_id: ``str``

        """
        response = self._perform_request('/ipblocks/%s' % ipblock_id)
        return response

    def list_ipblocks(self, depth=1):
        """
        Retrieves a list of IPBlocks available in the account.

        """
        response = self._perform_request('/ipblocks?depth=%s' % str(depth))
        return response

    def delete_ipblock(self, ipblock_id):
        """
        Removes a IPBlock from your account.

        :param      ipblock_id: The unique ID of the IPBlock.
        :type       ipblock_id: ``str``

        """
        response = self._perform_request(
            url='/ipblocks/' + ipblock_id, type='DELETE')

        return response

    def reserve_ipblock(self, ipblock):
        """
        Reserves an IPBlock within your account.

        """
        properties = {
            "name": ipblock.name,
            "location": ipblock.location,
            "size": str(ipblock.size).lower()
        }

        raw = {
            "properties": properties,
        }

        data = self._underscore_to_camelcase(json.dumps(raw))

        response = self._perform_request(
            url='/ipblocks', type='POST', data=data)

        return response

    """LAN Functions
    """

    def get_lan(self, datacenter_id, lan_id, depth=1):
        """
        Retrieves a single LAN by ID.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/lans/%s?depth=%s' % (
                datacenter_id,
                lan_id,
                str(depth)))

        return response

    def list_lans(self, datacenter_id, depth=1):
        """
        Retrieves a list of LANs available in the account.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/lans?depth=%s' % (
                datacenter_id,
                str(depth)))

        return response

    def delete_lan(self, datacenter_id, lan_id):
        """
        Removes a LAN from the Datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/lans/%s' % (
                datacenter_id, lan_id), type='DELETE')

        return response

    def create_lan(self, datacenter_id, lan):
        """
        Creates a LAN in the Datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      lan: The LAN object to be created.
        :type       lan: ``dict``

        """
        data = self._underscore_to_camelcase(
            json.dumps(
                self._create_lan_dict(lan)
            )
        )

        response = self._perform_request(
            url='/datacenters/%s/lans' % datacenter_id,
            type='POST',
            data=data)

        return response

    def update_lan(self, datacenter_id, lan_id, **kwargs):
        """
        Updates a LAN

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s/lans/%s' % (datacenter_id, lan_id),
            type='PATCH',
            data=json.dumps(data))

        return response

    def get_lan_members(self, datacenter_id, lan_id, depth=1):
        """
        Retrieves the list of NICs that are part of the LAN.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/lans/%s/nics?depth=%s' % (
                datacenter_id,
                lan_id,
                str(depth)))

        return response

    """LoadBalancer Functions
    """

    def get_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Retrieves a single LoadBalancer by ID.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the LoadBalancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s' % (
                datacenter_id, loadbalancer_id))

        return response

    def list_loadbalancers(self, datacenter_id, depth=1):
        """
        Retrieves a list of LoadBalancers in the Datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers?depth=%s' % (
                datacenter_id, str(depth)))

        return response

    def delete_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Removes the LoadBalancer from the Datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the LoadBalancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s' % (
                datacenter_id, loadbalancer_id), type='DELETE')

        return response

    def create_loadbalancer(self, datacenter_id, loadbalancer):
        """
        Creates a LoadBalancer within the specified DataCenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      loadbalancer: The LoadBalancer object to be created.
        :type       loadbalancer: ``dict``

        """
        data = self._underscore_to_camelcase(
            json.dumps(
                self._create_loadbalancer_dict(loadbalancer)
            )
        )

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers' % datacenter_id,
            type='POST',
            data=data)

        return response

    def update_loadbalancer(self, datacenter_id,
                            loadbalancer_id, **kwargs):
        """
        Updates a LoadBalancer

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the LoadBalancer.
        :type       loadbalancer_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s' % (datacenter_id,
                                                      loadbalancer_id),
            type='PATCH',
            data=json.dumps(data))

        return response

    def get_loadbalancer_members(self, datacenter_id, loadbalancer_id,
                                 depth=1):
        """
        Retrieves the list of NICs that are part of the LAN.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the LoadBalancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s/balancednics?depth=%s' % (
                datacenter_id, loadbalancer_id, str(depth)))

        return response

    def add_loadbalanced_nics(self, datacenter_id,
                              loadbalancer_id, nic_id):
        """
        Associates a NIC with the given LoadBalancer.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the LoadBalancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The ID of the NIC.
        :type       nic_id: ``str``

        """
        data = '{ "id": "' + nic_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s/balancednics' % (
                datacenter_id,
                loadbalancer_id),
            type='POST',
            data=data)

        return response

    def get_loadbalanced_nic(self, datacenter_id,
                             loadbalancer_id, nic_id, depth=1):
        """
        Gets the properties of a balanced NIC.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the LoadBalancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s/balancednics/%s?depth=%s' % (
                datacenter_id,
                loadbalancer_id,
                nic_id,
                str(depth)))

        return response

    def remove_loadbalanced_nic(self, datacenter_id,
                                loadbalancer_id, nic_id):
        """
        Removes a NIC from the loadbalancer.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the LoadBalancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s/balancednics/%s' % (
                datacenter_id,
                loadbalancer_id,
                nic_id),
            type='DELETE')

        return response

    """Location Functions
    """

    def get_location(self, location_id):
        """
        Retrieves a single Location by ID.

        :param      location_id: The unique ID of the Location.
        :type       location_id: ``str``

        """
        response = self._perform_request('/locations/' + location_id)
        return response

    def list_locations(self):
        """
        Retrieves a list of Location available in the account.

        """
        response = self._perform_request('/locations')

        return response

    """NIC Functions
    """

    def get_nic(self, datacenter_id, server_id, nic_id, depth=1):
        """
        Retrieves a NIC by its ID.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/nics/%s?depth=%s' % (
                datacenter_id,
                server_id,
                nic_id,
                str(depth)))

        return response

    def list_nics(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of all NICs bound to the specified server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/nics?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

    def delete_nic(self, datacenter_id, server_id, nic_id):
        """
        Removes a NIC from the server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s' % (
                datacenter_id,
                server_id,
                nic_id),
            type='DELETE')

        return response

    def create_nic(self, datacenter_id, server_id, nic):
        """
        Creates a NIC on the specified server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the Server.
        :type       server_id: ``str``

        :param      nic: A NIC dict.
        :type       nic: ``dict``

        """

        data = json.dumps(self._create_nic_dict(nic))

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics' % (
                datacenter_id,
                server_id),
            type='POST',
            data=data)

        return response

    def update_nic(self, datacenter_id, server_id,
                   nic_id, **kwargs):
        """
        Updates a NIC with the parameters provided.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the Server.
        :type       server_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics/%s' % (
                datacenter_id,
                server_id,
                nic_id),
            type='PATCH',
            data=json.dumps(data))

        return response

    """Request Functions
    """

    def get_request(self, request_id, status=False):
        """
        Retrieves a single request by ID.

        :param      request_id: The unique ID of the request.
        :type       request_id: ``str``

        :param      status: Retreive the full status of the request.
        :type       status: ``bool``

        """
        if status:
            response = self._perform_request(
                '/requests/' + request_id + '/status')
        else:
            response = self._perform_request(
                '/requests/%s' % request_id)

        return response

    def list_requests(self, depth=1):
        """
        Retrieves a list of requests available in the account.

        """
        response = self._perform_request(
            '/requests?depth=%s' % str(depth))

        return response

    """Server Functions
    """

    def get_server(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a server by its ID.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

    def list_servers(self, datacenter_id, depth=1):
        """
        Retrieves a list of all servers bound to the specified server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers?depth=%s' % (datacenter_id, str(depth)))

        return response

    def delete_server(self, datacenter_id, server_id):
        """
        Removes the server from your Datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s' % (
                datacenter_id,
                server_id),
            type='DELETE')

        return response

    def create_server(self, datacenter_id, server):
        """
        Creates a server within the Datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server: A dict of the Server to be created.
        :type       server: ``dict``

        """

        data = json.dumps(self._create_server_dict(server))

        response = self._perform_request(
            url='/datacenters/%s/servers' % (datacenter_id),
            type='POST',
            data=data)

        return response

    def update_server(self, datacenter_id, server_id, **kwargs):
        """
        Updates a server with the parameters provided.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            if attr == 'boot_volume':
                boot_volume_properties = {
                    "id": kwargs[attr]
                }
                boot_volume_entities = {
                    "bootVolume": boot_volume_properties
                }
                data.update(boot_volume_entities)
            else:
                data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s/servers/%s' % (
                datacenter_id,
                server_id),
            type='PATCH',
            data=json.dumps(data))

        return response

    def get_attached_volumes(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of volumes attached to the server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/volumes?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

    def get_attached_volume(self, datacenter_id, server_id, volume_id):
        """
        Retrieves volume information.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/volumes/%s' % (
                datacenter_id,
                server_id,
                volume_id))

        return response

    def attach_volume(self, datacenter_id, server_id, volume_id):
        """
        Attaches a volume to a server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        data = '{ "id": "' + volume_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/volumes' % (
                datacenter_id,
                server_id),
            type='POST',
            data=data)

        return response

    def detach_volume(self, datacenter_id, server_id, volume_id):
        """
        Detaches a volume from a server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/volumes/%s' % (
                datacenter_id,
                server_id,
                volume_id),
            type='DELETE')

        return response

    def get_attached_cdroms(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of CDROMs attached to the server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/cdroms?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

    def get_attached_cdrom(self, datacenter_id, server_id, cdrom_id):
        """
        Retrieves an attached CDROM.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      cdrom_id: The unique ID of the CDROM.
        :type       cdrom_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s/cdroms/%s' % (
                datacenter_id,
                server_id,
                cdrom_id))

        return response

    def attach_cdrom(self, datacenter_id, server_id, cdrom_id):
        """
        Attaches a CDROM to a server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      cdrom_id: The unique ID of the volume.
        :type       cdrom_id: ``str``

        """
        data = '{ "id": "' + cdrom_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/cdroms' % (
                datacenter_id,
                server_id),
            type='POST',
            data=data)

        return response

    def detach_cdrom(self, datacenter_id, server_id, cdrom_id):
        """
        Detaches a volume from a server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      cdrom_id: The unique ID of the CDROM.
        :type       cdrom_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/cdroms/%s' % (
                datacenter_id,
                server_id,
                cdrom_id),
            type='DELETE')

        return response

    def start_server(self, datacenter_id, server_id):
        """
        Starts the server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/start' % (
                datacenter_id,
                server_id),
            type='POST-ACTION')

        return response

    def stop_server(self, datacenter_id, server_id):
        """
        Stops the server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/stop' % (
                datacenter_id,
                server_id),
            type='POST-ACTION')

        return response

    def reboot_server(self, datacenter_id, server_id):
        """
        Reboots the server.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/reboot' % (
                datacenter_id,
                server_id),
            type='POST-ACTION')

        return response

    """Snapshot Functions
    """

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
            url='/snapshots/' + snapshot_id, type='DELETE')

        return response

    def update_snapshot(self, snapshot_id, **kwargs):
        """
        Removes a snapshot from your account.

        :param      snapshot_id: The unique ID of the snapshot.
        :type       snapshot_id: ``str``
        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/snapshots/' + snapshot_id, type='PATCH', data=json.dumps(data))

        return response

    def create_snapshot(self, datacenter_id, volume_id,
                        name=None, description=None):
        """
        Creates a snapshot of the specified volume.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """

        data = {'name': name, 'description': description}

        response = self._perform_request(
            '/datacenters/%s/volumes/%s/create-snapshot' % (
                datacenter_id, volume_id),
            type='POST-ACTION-JSON',
            data=urlencode(data))

        return response

    def restore_snapshot(self, datacenter_id, volume_id, snapshot_id):
        """
        Restores a snapshot to the specified volume.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        :param      snapshot_id: The unique ID of the Snapshot.
        :type       snapshot_id: ``str``

        """
        data = {'snapshotId': snapshot_id}

        response = self._perform_request(
            url='/datacenters/%s/volumes/%s/restore-snapshot' % (
                datacenter_id,
                volume_id),
            type='POST-ACTION',
            data=urlencode(data))

        return response

    def remove_snapshot(self, snapshot_id):
        """
        Removes a snapshot.

        :param      snapshot_id: The ID of the Snapshot
                                 you wish to remove.
        :type       snapshot_id: ``str``

        """
        response = self._perform_request(
            url='/snapshots/' + snapshot_id, type='DELETE')

        return response

    """Volume Functions
    """

    def get_volume(self, datacenter_id, volume_id):
        """
        Retrieves a single volume by ID.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/volumes/%s' % (datacenter_id, volume_id))

        return response

    def list_volumes(self, datacenter_id, depth=1):
        """
        Retrieves a list of Volumes in the datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/volumes?depth=%s' % (datacenter_id, str(depth)))

        return response

    def delete_volume(self, datacenter_id, volume_id):
        """
        Removes a Volume from the Datacenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/volumes/%s' % (
                datacenter_id, volume_id), type='DELETE')

        return response

    def create_volume(self, datacenter_id, volume):
        """
        Creates a volume within the specified DataCenter.

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      volume: A Volume dict.
        :type       volume: ``dict``

        """

        data = (json.dumps(self._create_volume_dict(volume)))

        response = self._perform_request(
            url='/datacenters/%s/volumes' % datacenter_id,
            type='POST',
            data=data)

        return response

    def update_volume(self, datacenter_id, volume_id, **kwargs):
        """
        Updates a volume

        :param      datacenter_id: The unique ID of the Datacenter.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s/volumes/%s' % (
                datacenter_id,
                volume_id),
            type='PATCH',
            data=json.dumps(data))

        return response

    """Private Functions
    """

    def _wrapped_request(self, method, url,
                         params=None,
                         data=None,
                         headers=None,
                         cookies=None,
                         files=None,
                         auth=None,
                         timeout=None,
                         allow_redirects=True,
                         proxies=None,
                         hooks=None,
                         stream=None):

        headers.update(self.headers)
        session = requests.Session()
        return session.request(method, url, params, data, headers, cookies,
                               files, auth, timeout, allow_redirects, proxies,
                               hooks, stream, self.verify, self.host_cert)

    def _perform_request(self, url, type='GET', data=None, headers=dict()):
        headers.update({'Authorization': 'Basic %s' % (base64.b64encode(
            self._b('%s:%s' % (self.username,
                               self.password))).decode('utf-8'))})

        url = self._build_url(url)
        headers.update(
            {'User-Agent':
                 'profitbricks-sdk-python/' + __version__})
        if type == 'POST' or type == 'PUT':
            headers.update(
                {'Content-Type':
                     'application/json'})
            response = self._wrapped_request(type, url, data=data,
                                             headers=headers)
        elif type == 'POST-ACTION-JSON' or type == 'POST-ACTION':
            headers.update(
                {'Content-Type':
                     'application/x-www-form-urlencoded; charset=UTF-8'})
            response = self._wrapped_request('POST', url, data=data,
                                             headers=headers)
            if response.status_code == 202 and type == 'POST-ACTION':
                return True
            elif response.status_code == 401:
                raise response.raise_for_status()
        elif type == 'PATCH':
            headers.update(
                {'Content-Type':
                     'application/json'})
            response = self._wrapped_request(type, url, data=data,
                                             headers=headers)
        else:
            headers.update(
                {'Content-Type':
                     'application/json'})
            response = self._wrapped_request(type, url, params=data,
                                             headers=headers)
            if type == 'DELETE':
                if response.status_code == 202:
                    return True

        try:
            if not response.ok:
                err = response.json()
                code = err['httpStatus']
                msg = err['messages'][0]['message']
                raise Exception(code, msg)
        except ValueError as e:
            raise Exception('Failed to parse the response', response.text)

        json_response = response.json()

        if 'location' in response.headers:
            json_response['requestId'] = self._request_id(response.headers)

        return json_response

    def _request_id(self, headers):
        # The request URL has currently the format:
        # {host_base}/requests/{request ID}/status
        # Thus search for a UUID.
        match = re.search('/requests/([-A-Fa-f0-9]+)/', headers['location'])
        if match:
            return match.group(1)
        else:
            raise Exception("Failed to extract request ID from response "
                            "header 'location': '{location}'".format(
                location=headers['location']))

    def _build_url(self, uri):
        url = self.host_base + uri
        return url

    def _b(self, s, encoding='utf-8'):
        """
        Returns the given string as a string of bytes. That means in
        Python2 as a str object, and in Python3 as a bytes object.
        Raises a TypeError, if it cannot be converted.
        """
        if six.PY2:
            # This is Python2
            if isinstance(s, str):
                return s
            elif isinstance(s, unicode):
                return s.encode(encoding)
        else:
            # And this is Python3
            if isinstance(s, bytes):
                return s
            elif isinstance(s, str):
                return s.encode(encoding)

        raise TypeError("Invalid argument %r for _b()" % (s,))

    'Used to convert python snake case back to mixed case.'

    def _underscore_to_camelcase(self, value):
        def camelcase():
            yield str.lower
            while True:
                yield str.capitalize

        c = camelcase()
        return "".join(next(c)(x) if x else '_' for x in value.split("_"))

    def _create_lan_dict(self, lan):
        items = []
        entities = dict()

        properties = {
            "name": lan.name
        }

        ' Optional Properties'
        if lan.public is not None:
            properties['public'] = str(lan.public).lower()

        if len(lan.nics) > 0:
            for nic in lan.nics:
                nics_properties = {
                    "id": nic
                }
                items.append(nics_properties)

            item_entities = {
                "items": items
            }

            nics_entities = {
                "nics": item_entities
            }

            entities.update(nics_entities)

        if len(entities) == 0:
            raw = {
                "properties": properties,
            }
        else:
            raw = {
                "properties": properties,
                "entities": entities
            }

        return raw

    def _create_loadbalancer_dict(self, loadbalancer):
        items = []
        entities = dict()

        properties = {
            "name": loadbalancer.name
        }

        ' Optional Properties'
        if loadbalancer.ip:
            properties['ip'] = loadbalancer.ip
        if loadbalancer.dhcp is not None:
            properties['dhcp'] = str(loadbalancer.dhcp).lower()

        if len(loadbalancer.balancednics) > 0:
            for nic in loadbalancer.balancednics:
                balancednic_properties = {
                    "id": nic
                }
                items.append(balancednic_properties)

            item_entities = {
                "items": items
            }

            balancednics_entities = {
                "balancednics": item_entities
            }

            entities.update(balancednics_entities)

        if len(loadbalancer.balancednics) == 0:
            raw = {
                "properties": properties,
            }
        else:
            raw = {
                "properties": properties,
                "entities": entities
            }

        return raw

    def _create_nic_dict(self, nic):
        items = []

        properties = {
            "name": nic.name,
            "lan": nic.lan,
        }

        ' Optional Properties'
        if nic.nat:
            properties['nat'] = nic.nat

        if nic.ips:
            properties['ips'] = nic.ips

        if nic.dhcp is not None:
            properties['dhcp'] = nic.dhcp

        if nic.firewall_active is not None:
            properties['firewallActive'] = nic.firewall_active

        if len(nic.firewall_rules) > 0:
            for rule in nic.firewall_rules:
                items.append(self._create_firewallrules_dict(rule))

        rules = {
            "items": items
        }

        entities = {
            "firewallrules": rules
        }

        if len(nic.firewall_rules) == 0:
            raw = {
                "properties": properties,
            }
        else:
            raw = {
                "properties": properties,
                "entities": entities
            }

        return raw

    def _create_firewallrules_dict(self, rule):
        properties = {}

        if rule.name:
            properties['name'] = rule.name

        if rule.protocol:
            properties['protocol'] = rule.protocol

        if rule.source_mac:
            properties['sourceMac'] = rule.source_mac

        if rule.source_ip:
            properties['sourceIp'] = rule.source_ip

        if rule.target_ip:
            properties['targetIp'] = rule.target_ip

        if rule.port_range_start:
            properties['portRangeStart'] = rule.port_range_start

        if rule.port_range_end:
            properties['portRangeEnd'] = rule.port_range_end

        if rule.icmp_type:
            properties['icmpType'] = rule.icmp_type

        if rule.icmp_code:
            properties['icmpCode'] = rule.icmp_code

        raw = {
            "properties": properties
        }

        return raw

    def _create_server_dict(self, server):
        volume_items = []
        nic_items = []
        entities = dict()

        properties = {
            "name": server.name,
            "ram": server.ram,
            "cores": server.cores
        }

        ' Optional Properties'
        if server.availability_zone:
            properties['availabilityZone'] = server.availability_zone

        if server.boot_cdrom:
            properties['bootCdrom'] = server.boot_cdrom

        if server.boot_volume_id:
            boot_volume = {
                "id": server.boot_volume_id
            }
            properties['bootVolume'] = boot_volume

        if server.cpu_family:
            properties['cpuFamily'] = server.cpu_family

        if len(server.create_volumes) > 0:
            for volume in server.create_volumes:
                volume_items.append(self._create_volume_dict(volume))

            volumes = {
                "items": volume_items
            }

            volume_entities = {
                "volumes": volumes
            }

            entities.update(volume_entities)

        if len(server.nics) > 0:
            for nic in server.nics:
                nic_items.append(self._create_nic_dict(nic))

            nics = {
                "items": nic_items
            }

            nic_entities = {
                "nics": nics
            }
            entities.update(nic_entities)

        ' Attach Existing Volume(s) '
        if len(server.attach_volumes) > 0:
            for volume in server.attach_volumes:
                volume_properties = {
                    "id": volume
                }
                volume_items.append(volume_properties)

            volumes = {
                "items": volume_items
            }

            volume_entities = {
                "volumes": volumes
            }

            entities.update(volume_entities)

        if len(entities) == 0:
            raw = {
                "properties": properties,
            }
        else:
            raw = {
                "properties": properties,
                "entities": entities
            }

        return raw

    def _create_volume_dict(self, volume):
        properties = {
            "name": volume.name,
            "size": volume.size
        }

        ' Optional Properties'
        if volume.availability_zone:
            properties['availabilityZone'] = volume.availability_zone

        if volume.image:
            properties['image'] = volume.image

        if volume.bus:
            properties['bus'] = volume.bus

        if volume.disk_type:
            properties['type'] = volume.disk_type

        if volume.image is None:
            properties['licenceType'] = volume.licence_type

        # if volume.licence_type:
        #     properties['licenceType'] = volume.licence_type

        if volume.image_password:
            properties['imagePassword'] = volume.image_password

        if volume.ssh_keys:
            properties['sshKeys'] = volume.ssh_keys

        raw = {
            "properties": properties
        }

        return raw


class Datacenter(ProfitBricksService):
    def __init__(self, name=None, location=None, description=None,
                 volumes=[], servers=[], lans=[], loadbalancers=[],
                 **kwargs):
        """
        Datacenter class initializer.

        :param      name: The Datacenter name..
        :type       name: ``str``

        :param      location: The Datacenter geographical location.
        :type       location: ``str``

        :param      description: Optional description.
        :type       description: ``str``

        :param      volumes: List of volume dicts.
        :type       volumes: ``list``

        :param      servers: List of server dicts.
        :type       servers: ``list``

        :param      lans: List of LAN dicts.
        :type       lans: ``list``

        :param      loadbalancers: List of loadbalancer dicts.
        :type       loadbalancers: ``list``

        """
        self.name = name
        self.description = description
        self.location = location
        self.servers = servers
        self.volumes = volumes
        self.lans = lans
        self.loadbalancers = loadbalancers

    def __repr__(self):
        return ((
                    '<Datacenter: name=%s, location=%s, description=%s> ...>')
                % (self.name, self.location, self.description))


class FirewallRule(ProfitBricksService):
    def __init__(self, name=None, protocol=None,
                 source_mac=None, source_ip=None,
                 target_ip=None, port_range_start=None,
                 port_range_end=None, icmp_type=None,
                 icmp_code=None, **kwargs):
        """
        FirewallRule class initializer.

        :param      name: The name of the FirewallRule.
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
        return ((
                    '<FirewallRule: name=%s, protocol=%s, source_mac=%s, '
                    'source_ip=%s, target_ip=%s, port_range_start=%s, '
                    'port_range_end=%s, icmp_type=%s, icmp_code=%s> ...>')
                % (self.name, self.protocol, self.source_mac,
                   self.source_ip, self.target_ip, self.port_range_start,
                   self.port_range_end, self.icmp_type, self.icmp_code))


class IPBlock(ProfitBricksService):
    def __init__(self, name=None, location=None, size=None):
        """
        IPBlock class initializer.

        :param      name: The name of the IP Block.
        :type       name: ``str``

        :param      location: The location for the IP Block.
        :type       location: ``str``

        :param      size: The number of IPs in the block.
        :type       size: ``str``

        """
        self.name = name
        self.location = location
        self.size = size

    def __repr__(self):
        return ((
                    '<IPBlock: location=%s, size=%s>')
                % (self.location, self.size))


class LAN(ProfitBricksService):
    '''
    This is the main class for managing LAN resources.
    '''

    def __init__(self, name=None, public=None, nics=[]):
        """
        LAN class initializer.

        :param      name: The name of the LAN.
        :type       name: ``str``

        :param      public: Indicates if the LAN is public.
        :type       public: ``bool``

        :param      nics: A list of NICs
        :type       nics: ``list``

        """
        self.name = name
        self.public = public
        self.nics = nics

    def __repr__(self):
        return ((
                    '<LAN: name=%s, public=%s> ...>')
                % (self.name, str(self.public)))


class LoadBalancer(ProfitBricksService):
    '''
    This is the main class for managing LoadBalancer resources.
    '''

    def __init__(self, name=None, ip=None,
                 dhcp=None, balancednics=[], **kwargs):
        """
        LoadBalancer class initializer.

        :param      name: The name of the LoadBalancer.
        :type       name: ``str``

        :param      ip: The IP for the loadbalancer.
        :type       ip: ``str``

        :param      dhcp: Indicates if the LoadBalancer
                          uses DHCP or not.
        :type       dhcp: ``bool``

        :param      balancednics: A list of NICs associated
                                  with the LoadBalancer.
        :type       balancednics: ``list``

        """
        self.name = name
        self.ip = ip
        self.dhcp = dhcp
        self.balancednics = balancednics

    def __repr__(self):
        return ((
                    '<LoadBalancer: name=%s, ip=%s, dhcp=%s> ...>')
                % (self.name, self.ip, str(self.dhcp)))


class NIC(ProfitBricksService):
    def __init__(self, name=None, ips=None,
                 dhcp=None, lan=None, firewall_active=None,
                 firewall_rules=[], nat=None, **kwargs):
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

        :param      firewall_active: Turns the firewall on or not;
                                     default is disabled until a
                                     rule is added.
        :type       firewall_active: ``bool``

        :param      firewall_rules: List of Firewall rule dicts.
        :type       firewall_rules: ``list``

        """
        self.name = name
        self.nat = nat
        self.ips = ips
        self.dhcp = dhcp
        self.lan = lan
        self.firewall_active = firewall_active
        self.firewall_rules = firewall_rules

    def __repr__(self):
        return ((
                    '<NIC: name=%s, ips=%s, dhcp=%s,lan=%s, '
                    'firewall_active=%s> ...>')
                % (self.name, self.ips, str(self.dhcp),
                   self.lan, str(self.firewall_active)))


class Server(ProfitBricksService):
    '''
    This is the main class for managing server resources.
    '''

    def __init__(self, name=None, cores=None, ram=None, availability_zone=None,
                 boot_volume_id=None, boot_cdrom=None, cpu_family=None,
                 create_volumes=[], attach_volumes=[], nics=[]):
        """
        Server class initializer.

        :param      name: The name of your server..
        :type       name: ``str``

        :param      cores: The number of cores for the server.
        :type       cores: ``str``

        :param      ram: The amount of memory for the server.
        :type       ram: ``str``

        :param      availability_zone: The availability zone for the server.
        :type       availability_zone: ``str``

        :param      boot_volume_id: The ID of the boot volume.
        :type       boot_volume_id: ``str``

        :param      boot_cdrom: Attach a CDROM.
        :type       boot_cdrom: ``str``

        :param      cpu_family: Set the desired CPU type.
        :type       cpu_family: ``str``

        :param      create_volumes: List of Volume dicts to create.
        :type       create_volumes: ``list``

        :param      attach_volumes: List of Volume IDs to attach.
        :type       attach_volumes: ``list``

        :param      nics: List of NIC dicts to create.
        :type       nics: ``list``

        """
        self.name = name
        self.cores = cores
        self.ram = ram
        self.availability_zone = availability_zone
        self.boot_volume_id = boot_volume_id
        self.boot_cdrom = boot_cdrom
        self.cpu_family = cpu_family
        self.create_volumes = create_volumes
        self.attach_volumes = attach_volumes
        self.nics = nics

    def __repr__(self):
        return ((
                    '<Server: name=%s, cores=%s, ram=%s, '
                    'availability_zone=%s, boot_volume_id=%s, '
                    'boot_cdrom=%s, ...>')
                % (self.name, self.cores, self.ram,
                   self.availability_zone, self.boot_volume_id, self.boot_cdrom))


class Volume(ProfitBricksService):
    def __init__(self, name=None, size=None, bus='VIRTIO', image=None,
                 disk_type='HDD', licence_type='UNKNOWN', image_password=None,
                 ssh_keys=[], availability_zone='AUTO', **kwargs):
        """
        Volume class initializer.

        :param      name: The name of the volume.
        :type       name: ``str``

        :param      size: The size of the volume.
        :type       size: ``str``

        :param      bus: The BUS type. Def. VIRTIO.
        :type       bus: ``str``

        :param      image: The Image ID to use.
        :type       image: ``str``

        :param      disk_type: The type of storage. Def. HDD
        :type       disk_type: ``str``

        :param      licence_type: The license type.
        :type       licence_type: ``str``

        :param      ssh_keys: A list of public SSH keys.
        :type       ssh_keys: ``list``

        :param      availability_zone: The availability zone for the server.
        :type       availability_zone: ``str``

        """
        self.name = name
        self.availability_zone = availability_zone
        self.size = int(size)
        self.image = image
        self.bus = bus
        self.disk_type = disk_type
        self.licence_type = licence_type
        self.image_password = image_password
        self.ssh_keys = ssh_keys

    def __repr__(self):
        return ((
                    '<Volume: name=%s, size=%s, image=%s, bus=%s, disk_type=%s, ...>')
                % (self.name, str(self.size), self.image,
                   self.bus, self.disk_type))
