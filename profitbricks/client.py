# Copyright 2015-2017 ProfitBricks GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json
import logging
import re
import time
import requests
import six

from six.moves.urllib.parse import urlencode

from profitbricks import (
    API_HOST, __version__
)

from profitbricks.errors import (
    PBNotAuthorizedError,
    PBNotFoundError,
    PBValidationError,
    PBRateLimitExceededError,
    PBError,
    PBFailedRequest,
    PBTimeoutError,
)

from .utils import find_item_by_name


# ProfitBricks Object Classes
class ProfitBricksService(object):
    """
        ProfitBricksClient Base Class
    """

    def __init__(self, username=None, password=None, host_base=API_HOST,
                 host_cert=None, ssl_verify=True, headers=None, client_user_agent=None):
        if headers is None:
            headers = dict()
        self.username = username
        self.password = password
        self.host_base = host_base
        self.host_cert = host_cert
        self.verify = ssl_verify
        self.headers = headers
        self.user_agent = 'profitbricks-sdk-python/' + __version__
        if client_user_agent:
            self.user_agent = client_user_agent + ' ' + self.user_agent

    # Contract Resources Functions

    def list_contracts(self, depth=1):
        """
        Retrieves information about the resource limits
        for a particular contract and the current resource usage.

        """
        response = self._perform_request('/contracts?depth=' + str(depth))

        return response

    # Data Center Functions

    def get_datacenter(self, datacenter_id, depth=1):
        """
        Retrieves a data center by its ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s?depth=%s' % (datacenter_id, str(depth)))

        return response

    def get_datacenter_by_name(self, name, depth=1):
        """
        Retrieves a data center by its name.

        Either returns the data center response or raises an Exception
        if no or more than one data center was found with the name.
        The search for the name is done in this relaxing way:

        - exact name match
        - case-insentive name match
        - data center starts with the name
        - data center starts with the name  (case insensitive)
        - name appears in the data center name
        - name appears in the data center name (case insensitive)

        :param      name: The name of the data center.
        :type       name: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``
        """
        all_data_centers = self.list_datacenters(depth=depth)['items']
        data_center = find_item_by_name(all_data_centers, lambda i: i['properties']['name'], name)
        if len(data_center) == 0:
            raise NameError("No data center found with name "
                            "containing '{name}'.".format(name=name))
        if len(data_center) > 1:
            raise NameError("Found {n} data centers with the name '{name}': {names}".format(
                n=len(data_center),
                name=name,
                names=", ".join(d['properties']['name'] for d in data_center)
            ))
        return data_center[0]

    def list_datacenters(self, depth=1):
        """
        Retrieves a list of all data centers.

        """
        response = self._perform_request('/datacenters?depth=' + str(depth))

        return response

    def delete_datacenter(self, datacenter_id):
        """
        Removes the data center and all its components such as servers, NICs,
        load balancers, volumes.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s' % (datacenter_id),
            method='DELETE')

        return response

    def create_datacenter(self, datacenter):
        """
        Creates a data center -- both simple and complex are supported.

        """
        server_items = []
        volume_items = []
        lan_items = []
        loadbalancer_items = []

        entities = dict()

        properties = {
            "name": datacenter.name
        }

        # Omit 'location', if not provided, to receive
        # a meaningful error message.
        if datacenter.location:
            properties['location'] = datacenter.location

        # Optional Properties
        if datacenter.description:
            properties['description'] = datacenter.description

        # Servers
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

        # Volumes
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

        # Load Balancers
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

        # LANs
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
            method='POST',
            data=data)

        return response

    def update_datacenter(self, datacenter_id, **kwargs):
        """
        Updates a data center with the parameters provided.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s' % (
                datacenter_id),
            method='PATCH',
            data=json.dumps(data))

        return response

    # Firewall Rule Functions

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
            method='PATCH',
            data=json.dumps(data))

        return response

    # Image Functions

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
        Retrieves a list of images available in the data center.

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
                                         method='DELETE')
        return response

    def update_image(self, image_id, **kwargs):
        """
        Replace all properties of an image.

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(url='/images/' + image_id,
                                         method='PATCH',
                                         data=json.dumps(data))
        return response

    # IP block Functions

    def get_ipblock(self, ipblock_id):
        """
        Retrieves a single IP block by ID.

        :param      ipblock_id: The unique ID of the IP block.
        :type       ipblock_id: ``str``

        """
        response = self._perform_request('/ipblocks/%s' % ipblock_id)
        return response

    def list_ipblocks(self, depth=1):
        """
        Retrieves a list of IP blocks available in the account.

        """
        response = self._perform_request('/ipblocks?depth=%s' % str(depth))
        return response

    def delete_ipblock(self, ipblock_id):
        """
        Removes a single IP block from your account.

        :param      ipblock_id: The unique ID of the IP block.
        :type       ipblock_id: ``str``

        """
        response = self._perform_request(
            url='/ipblocks/' + ipblock_id, method='DELETE')

        return response

    def reserve_ipblock(self, ipblock):
        """
        Reserves an IP block within your account.

        """
        properties = {
            "name": ipblock.name
        }

        if ipblock.location:
            properties['location'] = ipblock.location

        if ipblock.size:
            properties['size'] = str(ipblock.size)

        raw = {
            "properties": properties,
        }

        data = self._underscore_to_camelcase(json.dumps(raw))

        response = self._perform_request(
            url='/ipblocks', method='POST', data=data)

        return response

    # LAN Functions

    def get_lan(self, datacenter_id, lan_id, depth=1):
        """
        Retrieves a single LAN by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

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

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/lans?depth=%s' % (
                datacenter_id,
                str(depth)))

        return response

    def delete_lan(self, datacenter_id, lan_id):
        """
        Removes a LAN from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/lans/%s' % (
                datacenter_id, lan_id), method='DELETE')

        return response

    def create_lan(self, datacenter_id, lan):
        """
        Creates a LAN in the data center.

        :param      datacenter_id: The unique ID of the data center.
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
            method='POST',
            data=data)

        return response

    def update_lan(self, datacenter_id, lan_id, name=None,
                   public=None, ip_failover=None):
        """
        Updates a LAN

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      lan_id: The unique ID of the LAN.
        :type       lan_id: ``str``

        :param      name: The new name of the LAN.
        :type       name: ``str``

        :param      public: Indicates if the LAN is public.
        :type       public: ``bool``

        :param      ip_failover: A list of IP fail-over dicts.
        :type       ip_failover: ``list``

        """
        data = {}

        if name:
            data['name'] = name

        if public is not None:
            data['public'] = public

        if ip_failover:
            data['ipFailover'] = ip_failover

        response = self._perform_request(
            url='/datacenters/%s/lans/%s' % (datacenter_id, lan_id),
            method='PATCH',
            data=json.dumps(data))

        return response

    def get_lan_members(self, datacenter_id, lan_id, depth=1):
        """
        Retrieves the list of NICs that are part of the LAN.

        :param      datacenter_id: The unique ID of the data center.
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

    # Load balancer Functions

    def get_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Retrieves a single load balancer by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s' % (
                datacenter_id, loadbalancer_id))

        return response

    def list_loadbalancers(self, datacenter_id, depth=1):
        """
        Retrieves a list of load balancers in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers?depth=%s' % (
                datacenter_id, str(depth)))

        return response

    def delete_loadbalancer(self, datacenter_id, loadbalancer_id):
        """
        Removes the load balancer from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s' % (
                datacenter_id, loadbalancer_id), method='DELETE')

        return response

    def create_loadbalancer(self, datacenter_id, loadbalancer):
        """
        Creates a load balancer within the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer: The load balancer object to be created.
        :type       loadbalancer: ``dict``

        """
        data = self._underscore_to_camelcase(
            json.dumps(
                self._create_loadbalancer_dict(loadbalancer)
            )
        )

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers' % datacenter_id,
            method='POST',
            data=data)

        return response

    def update_loadbalancer(self, datacenter_id,
                            loadbalancer_id, **kwargs):
        """
        Updates a load balancer

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        """
        data = {}

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s' % (datacenter_id,
                                                      loadbalancer_id),
            method='PATCH',
            data=json.dumps(data))

        return response

    def get_loadbalancer_members(self, datacenter_id, loadbalancer_id,
                                 depth=1):
        """
        Retrieves the list of NICs that are associated with a load balancer.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/loadbalancers/%s/balancednics?depth=%s' % (
                datacenter_id, loadbalancer_id, str(depth)))

        return response

    def add_loadbalanced_nics(self, datacenter_id,
                              loadbalancer_id, nic_id):
        """
        Associates a NIC with the given load balancer.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The ID of the NIC.
        :type       nic_id: ``str``

        """
        data = '{ "id": "' + nic_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s/balancednics' % (
                datacenter_id,
                loadbalancer_id),
            method='POST',
            data=data)

        return response

    def get_loadbalanced_nic(self, datacenter_id,
                             loadbalancer_id, nic_id, depth=1):
        """
        Gets the properties of a load balanced NIC.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

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
        Removes a NIC from the load balancer.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      loadbalancer_id: The unique ID of the load balancer.
        :type       loadbalancer_id: ``str``

        :param      nic_id: The unique ID of the NIC.
        :type       nic_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/loadbalancers/%s/balancednics/%s' % (
                datacenter_id,
                loadbalancer_id,
                nic_id),
            method='DELETE')

        return response

    # Location Functions

    def get_location(self, location_id):
        """
        Retrieves a single location by ID.

        :param      location_id: The unique ID of the location.
        :type       location_id: ``str``

        """
        response = self._perform_request('/locations/' + location_id)
        return response

    def list_locations(self):
        """
        Retrieves a list of locations available in the account.

        """
        response = self._perform_request('/locations')

        return response

    # NIC Functions

    def get_nic(self, datacenter_id, server_id, nic_id, depth=1):
        """
        Retrieves a NIC by its ID.

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
            '/datacenters/%s/servers/%s/nics/%s?depth=%s' % (
                datacenter_id,
                server_id,
                nic_id,
                str(depth)))

        return response

    def list_nics(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of all NICs bound to the specified server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

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

        :param      datacenter_id: The unique ID of the data center.
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
            method='DELETE')

        return response

    def create_nic(self, datacenter_id, server_id, nic):
        """
        Creates a NIC on the specified server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      nic: A NIC dict.
        :type       nic: ``dict``

        """

        data = json.dumps(self._create_nic_dict(nic))

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/nics' % (
                datacenter_id,
                server_id),
            method='POST',
            data=data)

        return response

    def update_nic(self, datacenter_id, server_id,
                   nic_id, **kwargs):
        """
        Updates a NIC with the parameters provided.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
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
            method='PATCH',
            data=json.dumps(data))

        return response

    # Request Functions

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

    # Server Functions

    def get_server(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a server by its ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/servers/%s?depth=%s' % (
                datacenter_id,
                server_id,
                str(depth)))

        return response

    def list_servers(self, datacenter_id, depth=1):
        """
        Retrieves a list of all servers bound to the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/servers?depth=%s' % (datacenter_id, str(depth)))

        return response

    def delete_server(self, datacenter_id, server_id):
        """
        Removes the server from your data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s' % (
                datacenter_id,
                server_id),
            method='DELETE')

        return response

    def create_server(self, datacenter_id, server):
        """
        Creates a server within the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server: A dict of the server to be created.
        :type       server: ``dict``

        """

        data = json.dumps(self._create_server_dict(server))

        response = self._perform_request(
            url='/datacenters/%s/servers' % (datacenter_id),
            method='POST',
            data=data)

        return response

    def update_server(self, datacenter_id, server_id, **kwargs):
        """
        Updates a server with the parameters provided.

        :param      datacenter_id: The unique ID of the data center.
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
            method='PATCH',
            data=json.dumps(data))

        return response

    def get_attached_volumes(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of volumes attached to the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

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

        :param      datacenter_id: The unique ID of the data center.
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

        :param      datacenter_id: The unique ID of the data center.
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
            method='POST',
            data=data)

        return response

    def detach_volume(self, datacenter_id, server_id, volume_id):
        """
        Detaches a volume from a server.

        :param      datacenter_id: The unique ID of the data center.
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
            method='DELETE')

        return response

    def get_attached_cdroms(self, datacenter_id, server_id, depth=1):
        """
        Retrieves a list of CDROMs attached to the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

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

        :param      datacenter_id: The unique ID of the data center.
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

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        :param      cdrom_id: The unique ID of the CDROM.
        :type       cdrom_id: ``str``

        """
        data = '{ "id": "' + cdrom_id + '" }'

        response = self._perform_request(
            url='/datacenters/%s/servers/%s/cdroms' % (
                datacenter_id,
                server_id),
            method='POST',
            data=data)

        return response

    def detach_cdrom(self, datacenter_id, server_id, cdrom_id):
        """
        Detaches a volume from a server.

        :param      datacenter_id: The unique ID of the data center.
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
            method='DELETE')

        return response

    def start_server(self, datacenter_id, server_id):
        """
        Starts the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/start' % (
                datacenter_id,
                server_id),
            method='POST-ACTION')

        return response

    def stop_server(self, datacenter_id, server_id):
        """
        Stops the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/stop' % (
                datacenter_id,
                server_id),
            method='POST-ACTION')

        return response

    def reboot_server(self, datacenter_id, server_id):
        """
        Reboots the server.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      server_id: The unique ID of the server.
        :type       server_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/servers/%s/reboot' % (
                datacenter_id,
                server_id),
            method='POST-ACTION')

        return response

    # Snapshot Functions

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

        for attr in kwargs.keys():
            data[self._underscore_to_camelcase(attr)] = kwargs[attr]

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

    # User Management Functions

    def list_groups(self, depth=1):
        """
        Retrieves a list of all groups.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/groups?depth=' + str(depth))

        return response

    def get_group(self, group_id, depth=1):
        """
        Retrieves a single group by ID.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/groups/%s?depth=%s' % (group_id, str(depth)))

        return response

    def create_group(self, group):
        """
        Creates a new group and set group privileges.

        :param      group: The group object to be created.
        :type       group: ``dict``

        """
        data = json.dumps(self._create_group_dict(group))

        response = self._perform_request(
            url='/um/groups',
            method='POST',
            data=data)

        return response

    def update_group(self, group_id, **kwargs):
        """
        Updates a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        """
        properties = {}

        # make the key camel-case transformable
        if 'create_datacenter' in kwargs:
            kwargs['create_data_center'] = kwargs.pop('create_datacenter')

        for attr in kwargs.keys():
            properties[self._underscore_to_camelcase(attr)] = kwargs[attr]

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/groups/%s' % group_id,
            method='PUT',
            data=json.dumps(data))

        return response

    def delete_group(self, group_id):
        """
        Removes a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        """
        response = self._perform_request(
            url='/um/groups/%s' % group_id,
            method='DELETE')

        return response

    def list_shares(self, group_id, depth=1):
        """
        Retrieves a list of all shares though a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/groups/%s/shares?depth=%s' % (group_id, str(depth)))

        return response

    def get_share(self, group_id, resource_id, depth=1):
        """
        Retrieves a specific resource share available to a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/groups/%s/shares/%s?depth=%s'
            % (group_id, resource_id, str(depth)))

        return response

    def add_share(self, group_id, resource_id, **kwargs):
        """
        Shares a resource through a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        properties = {}

        for attr in kwargs.keys():
            properties[self._underscore_to_camelcase(attr)] = kwargs[attr]

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/groups/%s/shares/%s' % (group_id, resource_id),
            method='POST',
            data=json.dumps(data))

        return response

    def update_share(self, group_id, resource_id, **kwargs):
        """
        Updates the permissions of a group for a resource share.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        properties = {}

        for attr in kwargs.keys():
            properties[self._underscore_to_camelcase(attr)] = kwargs[attr]

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/groups/%s/shares/%s' % (group_id, resource_id),
            method='PUT',
            data=json.dumps(data))

        return response

    def delete_share(self, group_id, resource_id):
        """
        Removes a resource share from a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        """
        response = self._perform_request(
            url='/um/groups/%s/shares/%s' % (group_id, resource_id),
            method='DELETE')

        return response

    def list_users(self, depth=1):
        """
        Retrieves a list of all users.

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request('/um/users?depth=' + str(depth))

        return response

    def get_user(self, user_id, depth=1):
        """
        Retrieves a single user by ID.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/users/%s?depth=%s' % (user_id, str(depth)))

        return response

    def create_user(self, user):
        """
        Creates a new user.

        :param      user: The user object to be created.
        :type       user: ``dict``

        """
        data = self._create_user_dict(user=user)

        response = self._perform_request(
            url='/um/users',
            method='POST',
            data=json.dumps(data))

        return response

    def update_user(self, user_id, **kwargs):
        """
        Updates a user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        properties = {}

        for attr in kwargs.keys():
            properties[self._underscore_to_camelcase(attr)] = kwargs[attr]

        data = {
            "properties": properties
        }

        response = self._perform_request(
            url='/um/users/%s' % user_id,
            method='PUT',
            data=json.dumps(data))

        return response

    def delete_user(self, user_id):
        """
        Removes a user.

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        response = self._perform_request(
            url='/um/users/%s' % user_id,
            method='DELETE')

        return response

    def list_group_users(self, group_id, depth=1):
        """
        Retrieves a list of all users that are members of a particular group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/groups/%s/users?depth=%s' % (group_id, str(depth)))

        return response

    def add_group_user(self, group_id, user_id):
        """
        Adds an existing user to a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        data = {
            "properties": {
                "user": user_id
            }
        }

        response = self._perform_request(
            url='/um/groups/%s/users' % group_id,
            method='POST',
            data=json.dumps(data))

        return response

    def remove_group_user(self, group_id, user_id):
        """
        Removes a user from a group.

        :param      group_id: The unique ID of the group.
        :type       group_id: ``str``

        :param      user_id: The unique ID of the user.
        :type       user_id: ``str``

        """
        response = self._perform_request(
            url='/um/groups/%s/users/%s' % (group_id, user_id),
            method='DELETE')

        return response

    def list_resources(self, resource_type=None, depth=1):
        """
        Retrieves a list of all resources.

        :param      resource_type: The resource type: datacenter, image,
                                   snapshot or ipblock. Default is None,
                                   i.e., all resources are listed.
        :type       resource_type: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        if resource_type is not None:
            response = self._perform_request(
                '/um/resources/%s?depth=%s' % (resource_type, str(depth)))
        else:
            response = self._perform_request(
                '/um/resources?depth=' + str(depth))

        return response

    def get_resource(self, resource_type, resource_id, depth=1):
        """
        Retrieves a single resource of a particular type.

        :param      resource_type: The resource type: datacenter, image,
                                   snapshot or ipblock.
        :type       resource_type: ``str``

        :param      resource_id: The unique ID of the resource.
        :type       resource_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/um/resources/%s/%s?depth=%s' % (
                resource_type, resource_id, str(depth)))

        return response

    # Volume Functions

    def get_volume(self, datacenter_id, volume_id):
        """
        Retrieves a single volume by ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            '/datacenters/%s/volumes/%s' % (datacenter_id, volume_id))

        return response

    def list_volumes(self, datacenter_id, depth=1):
        """
        Retrieves a list of volumes in the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        response = self._perform_request(
            '/datacenters/%s/volumes?depth=%s' % (datacenter_id, str(depth)))

        return response

    def delete_volume(self, datacenter_id, volume_id):
        """
        Removes a volume from the data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume_id: The unique ID of the volume.
        :type       volume_id: ``str``

        """
        response = self._perform_request(
            url='/datacenters/%s/volumes/%s' % (
                datacenter_id, volume_id), method='DELETE')

        return response

    def create_volume(self, datacenter_id, volume):
        """
        Creates a volume within the specified data center.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      volume: A volume dict.
        :type       volume: ``dict``

        """

        data = (json.dumps(self._create_volume_dict(volume)))

        response = self._perform_request(
            url='/datacenters/%s/volumes' % datacenter_id,
            method='POST',
            data=data)

        return response

    def update_volume(self, datacenter_id, volume_id, **kwargs):
        """
        Updates a volume

        :param      datacenter_id: The unique ID of the data center.
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
            method='PATCH',
            data=json.dumps(data))

        return response

    def wait_for_completion(self, response, timeout=3600, initial_wait=5, scaleup=10):
        """
        Poll resource request status until resource is provisioned.

        :param      response: A response dict, which needs to have a 'requestId' item.
        :type       response: ``dict``

        :param      timeout: Maximum waiting time in seconds. None means infinite waiting time.
        :type       timeout: ``int``

        :param      initial_wait: Initial polling interval in seconds.
        :type       initial_wait: ``int``

        :param      scaleup: Double polling interval every scaleup steps, which will be doubled.
        :type       scaleup: ``int``

        """
        if not response:
            return
        logger = logging.getLogger(__name__)
        wait_period = initial_wait
        next_increase = time.time() + wait_period * scaleup
        if timeout:
            timeout = time.time() + timeout
        while True:
            request = self.get_request(request_id=response['requestId'], status=True)

            if request['metadata']['status'] == 'DONE':
                break
            elif request['metadata']['status'] == 'FAILED':
                raise PBFailedRequest(
                    'Request {0} failed to complete: {1}'.format(
                        response['requestId'], request['metadata']['message']),
                    response['requestId']
                )

            current_time = time.time()
            if timeout and current_time > timeout:
                raise PBTimeoutError('Timed out waiting for request {0}.'.format(
                    response['requestId']), response['requestId'])

            if current_time > next_increase:
                wait_period *= 2
                next_increase = time.time() + wait_period * scaleup
                scaleup *= 2

            logger.info("Request %s is in state '%s'. Sleeping for %i seconds...",
                        response['requestId'], request['metadata']['status'], wait_period)
            time.sleep(wait_period)

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

    def _perform_request(self, url, method='GET', data=None, headers=None):
        if headers is None:
            headers = dict()
        headers.update({'Authorization': 'Basic %s' % (base64.b64encode(
            self._b('%s:%s' % (self.username,
                               self.password))).decode('utf-8'))})

        url = self._build_url(url)
        headers.update({'User-Agent': self.user_agent})
        if method == 'POST' or method == 'PUT':
            response = self._wrapped_request(method, url, data=data,
                                             headers=headers)
            headers.update({'Content-Type': 'application/json'})
        elif method == 'POST-ACTION-JSON' or method == 'POST-ACTION':
            headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
            response = self._wrapped_request('POST', url, data=data,
                                             headers=headers)
            if response.status_code == 202 and method == 'POST-ACTION':
                return True
            elif response.status_code == 401:
                raise response.raise_for_status()
        elif method == 'PATCH':
            headers.update({'Content-Type': 'application/json'})
            response = self._wrapped_request(method, url, data=data,
                                             headers=headers)
        else:
            headers.update({'Content-Type': 'application/json'})
            response = self._wrapped_request(method, url, params=data,
                                             headers=headers)
            if method == 'DELETE':
                if response.status_code == 202:
                    return True

        try:
            if not response.ok:
                err = response.json()
                code = err['httpStatus']
                msg = err['messages']
                if response.status_code == 401:
                    raise PBNotAuthorizedError(code, msg, url)
                if response.status_code == 404:
                    raise PBNotFoundError(code, msg, url)
                if response.status_code == 422:
                    raise PBValidationError(code, msg, url)
                if response.status_code == 429:
                    raise PBRateLimitExceededError(code, msg, url)
                else:
                    raise PBError(code, msg, url)

        except ValueError:
            raise Exception('Failed to parse the response', response.text)

        json_response = response.json()

        if 'location' in response.headers:
            json_response['requestId'] = self._request_id(response.headers)

        return json_response

    @staticmethod
    def _request_id(headers):
        # The request URL has currently the format:
        # {host_base}/requests/{request ID}/status
        # Thus search for a UUID.
        match = re.search('/requests/([-A-Fa-f0-9]+)/', headers['location'])
        if match:
            return match.group(1)
        else:
            raise Exception("Failed to extract request ID from response "
                            "header 'location': '{location}'".format(location=headers['location']))

    def _build_url(self, uri):
        url = self.host_base + uri
        return url

    @staticmethod
    def _b(s, encoding='utf-8'):
        """
        Returns the given string as a string of bytes. That means in
        Python2 as a str object, and in Python3 as a bytes object.
        Raises a TypeError, if it cannot be converted.
        """
        if six.PY2:
            # This is Python2
            if isinstance(s, str):
                return s
            elif isinstance(s, unicode):  # noqa, pylint: disable=undefined-variable
                return s.encode(encoding)
        else:
            # And this is Python3
            if isinstance(s, bytes):
                return s
            elif isinstance(s, str):
                return s.encode(encoding)

        raise TypeError("Invalid argument %r for _b()" % (s,))

    @staticmethod
    def _underscore_to_camelcase(value):
        """
        Convert Python snake case back to mixed case.
        """
        def camelcase():
            yield str.lower
            while True:
                yield str.capitalize

        c = camelcase()
        return "".join(next(c)(x) if x else '_' for x in value.split("_"))

    @staticmethod
    def _create_lan_dict(lan):
        items = []
        entities = dict()

        properties = {
            "name": lan.name
        }

        # Optional Properties
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

    @staticmethod
    def _create_loadbalancer_dict(loadbalancer):
        items = []
        entities = dict()

        properties = {}

        if loadbalancer.name:
            properties['name'] = loadbalancer.name

        # Optional Properties
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
            "name": nic.name
        }

        if nic.lan:
            properties['lan'] = nic.lan

        # Optional Properties
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

    @staticmethod
    def _create_firewallrules_dict(rule):
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
            "name": server.name
        }

        # Omit required attributes, if not provided,
        # to receive a proper error message.
        if server.ram:
            properties['ram'] = server.ram

        if server.cores:
            properties['cores'] = server.cores

        # Optional Properties
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

        # Attach Existing Volume(s)
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

    @staticmethod
    def _create_volume_dict(volume):
        properties = {
            "name": volume.name
        }

        # Omit 'size' attributes, if not provided,
        # to receive a proper error message.
        if volume.size:
            properties['size'] = int(volume.size)

        # Optional Properties
        if volume.availability_zone:
            properties['availabilityZone'] = volume.availability_zone

        if volume.image:
            properties['image'] = volume.image

        if volume.image_alias:
            properties['imageAlias'] = volume.image_alias

        if volume.bus:
            properties['bus'] = volume.bus

        if volume.disk_type:
            properties['type'] = volume.disk_type

        if volume.image is None and volume.image_alias is None:
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

    @staticmethod
    def _create_group_dict(group):
        properties = {}

        if group.name:
            properties['name'] = group.name

        # Optional Properties
        if group.reserve_ip:
            properties['reserveIp'] = group.reserve_ip

        if group.create_snapshot:
            properties['createSnapshot'] = group.create_snapshot

        if group.create_datacenter:
            properties['createDataCenter'] = \
                group.create_datacenter

        if group.access_activity_log:
            properties['accessActivityLog'] = \
                group.access_activity_log

        raw = {
            "properties": properties
        }

        return raw

    @staticmethod
    def _create_user_dict(user):
        properties = {}

        if user.firstname:
            properties['firstname'] = user.firstname

        if user.lastname:
            properties['lastname'] = user.lastname

        if user.email:
            properties['email'] = user.email

        if user.password:
            properties['password'] = user.password

        # Optional Properties
        if user.administrator:
            properties['administrator'] = user.administrator

        if user.force_sec_auth:
            properties['forceSecAuth'] = user.force_sec_auth

        raw = {
            "properties": properties
        }

        return raw


class Datacenter(object):
    def __init__(self, name=None, location=None, description=None,
                 volumes=None, servers=None, lans=None, loadbalancers=None):
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


class FirewallRule(object):
    def __init__(self, name=None, protocol=None,
                 source_mac=None, source_ip=None,
                 target_ip=None, port_range_start=None,
                 port_range_end=None, icmp_type=None,
                 icmp_code=None):
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


class IPBlock(object):
    def __init__(self, name=None, location=None, size=None):
        """
        IPBlock class initializer.

        :param      name: The name of the IP block.
        :type       name: ``str``

        :param      location: The location for the IP block.
        :type       location: ``str``

        :param      size: The number of IPs in the block.
        :type       size: ``str``

        """
        self.name = name
        self.location = location
        self.size = size

    def __repr__(self):
        return (('<IPBlock: location=%s, size=%s>')
                % (self.location, self.size))


class LAN(object):
    """
    This is the main class for managing LAN resources.
    """

    def __init__(self, name=None, public=None, nics=None):
        """
        LAN class initializer.

        :param      name: The name of the LAN.
        :type       name: ``str``

        :param      public: Indicates if the LAN is public.
        :type       public: ``bool``

        :param      nics: A list of NICs
        :type       nics: ``list``

        """
        if nics is None:
            nics = []
        self.name = name
        self.public = public
        self.nics = nics

    def __repr__(self):
        return (('<LAN: name=%s, public=%s> ...>')
                % (self.name, str(self.public)))


class LoadBalancer(object):
    """
    This is the main class for managing load balancer resources.
    """

    def __init__(self, name=None, ip=None,
                 dhcp=None, balancednics=None):
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


class NIC(object):
    def __init__(self, name=None, ips=None,
                 dhcp=None, lan=None, firewall_active=None,
                 firewall_rules=None, nat=None):
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


class Server(object):
    """
    This is the main class for managing server resources.
    """

    def __init__(self, name=None, cores=None, ram=None, availability_zone=None,
                 boot_volume_id=None, boot_cdrom=None, cpu_family=None,
                 create_volumes=None, attach_volumes=None, nics=None):
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

        :param      create_volumes: List of volume dicts to create.
        :type       create_volumes: ``list``

        :param      attach_volumes: List of volume IDs to attach.
        :type       attach_volumes: ``list``

        :param      nics: List of NIC dicts to create.
        :type       nics: ``list``

        """
        if create_volumes is None:
            create_volumes = []
        if attach_volumes is None:
            attach_volumes = []
        if nics is None:
            nics = []
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
        return (('<Server: name=%s, cores=%s, ram=%s, '
                 'availability_zone=%s, boot_volume_id=%s, '
                 'boot_cdrom=%s, ...>')
                % (self.name, self.cores, self.ram,
                   self.availability_zone, self.boot_volume_id, self.boot_cdrom))


class Volume(object):
    def __init__(self, name=None, size=None, bus='VIRTIO', image=None,
                 image_alias=None, disk_type='HDD', licence_type='UNKNOWN',
                 image_password=None, ssh_keys=None, availability_zone='AUTO'):
        """
        Volume class initializer.

        :param      name: The name of the volume.
        :type       name: ``str``

        :param      size: The size of the volume.
        :type       size: ``str``

        :param      bus: The bus type. Def. VIRTIO.
        :type       bus: ``str``

        :param      image: The image ID to use.
        :type       image: ``str``

        :param      image_alias: An alias of the image to use.
        :type       image_alias: ``str``

        :param      disk_type: The type of storage. Def. HDD
        :type       disk_type: ``str``

        :param      licence_type: The licence type.
        :type       licence_type: ``str``

        :param      ssh_keys: A list of public SSH keys.
        :type       ssh_keys: ``list``

        :param      availability_zone: The availability zone for the server.
        :type       availability_zone: ``str``

        """
        if ssh_keys is None:
            ssh_keys = []
        self.name = name
        self.availability_zone = availability_zone
        self.size = size
        self.image = image
        self.image_alias = image_alias
        self.bus = bus
        self.disk_type = disk_type
        self.licence_type = licence_type
        self.image_password = image_password
        self.ssh_keys = ssh_keys

    def __repr__(self):
        return (('<Volume: name=%s, size=%s, image=%s, image_alias=%s,'
                 'bus=%s, disk_type=%s, ...>')
                % (self.name, str(self.size), self.image,
                   self.image_alias, self.bus, self.disk_type))


class Snapshot(object):
    def __init__(self, name=None, description=None, licence_type='UNKNOWN', size=None,
                 location=None):
        """
        Snapshot class initializer.

        :param      name: The name of the snapshot.
        :type       name: ``str``

        :param      name: The description of the snapshot.
        :type       name: ``str``

        :param      size: The size of the snapshot.
        :type       size: ``str``

        :param      licence_type: The licence type.
        :type       licence_type: ``str``


        """
        self.name = name
        self.description = description
        self.size = int(size)
        self.licence_type = licence_type
        self.location = location

    def __repr__(self):
        return ('<Snapshot: name={}, description={}, size={},location={}, ...>'.format(
            self.name, self.description, str(self.size), self.location))


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


class User(object):
    def __init__(self, firstname=None, lastname=None,
                 email=None, password=None,
                 administrator=None,
                 force_sec_auth=None):
        """
        User class initializer.

        :param      firstname: The user's first name.
        :type       firstname: ``str``

        :param      lastname: The user's last name.
        :type       lastname: ``str``

        :param      email: The user's email.
        :type       email: ``str``

        :param      password: A password for the user.
        :type       password: ``str``

        :param      administrator: Indicates if the user have
                                   administrative rights.
        :type       administrator: ``bool``

        :param      force_sec_auth: Indicates if secure (two-factor)
                                    authentication should be forced
                                    for the user.
        :type       force_sec_auth: ``bool``

        """
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.administrator = administrator
        self.force_sec_auth = force_sec_auth

    def __repr__(self):
        return ('<Group: firstname=%s, lastname=%s, email=%s, '
                'password=%s, administrator=%s, force_sec_auth=%s>'
                % (self.firstname, self.lastname,
                   self.email, self.password,
                   str(self.administrator),
                   str(self.force_sec_auth)))
