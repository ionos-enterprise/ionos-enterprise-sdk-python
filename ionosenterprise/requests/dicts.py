class dicts:
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

        if lan.pcc is not None:
            properties['pcc'] = lan.pcc

        if lan.nics:
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

        if not entities:
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

        if loadbalancer.balancednics:
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

        if not loadbalancer.balancednics:
            raw = {
                "properties": properties,
            }
        else:
            raw = {
                "properties": properties,
                "entities": entities
            }

        return raw

    def _create_k8s_dict(self, cluster_name):
        properties = {
            "name": cluster_name
        }

        raw = {
            "properties": properties,
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

        if nic.firewall_rules:
            for rule in nic.firewall_rules:
                items.append(self._create_firewallrules_dict(rule))

        rules = {
            "items": items
        }

        entities = {
            "firewallrules": rules
        }

        if not nic.firewall_rules:
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

        if server.create_volumes:
            for volume in server.create_volumes:
                volume_items.append(self._create_volume_dict(volume))

            volumes = {
                "items": volume_items
            }

            volume_entities = {
                "volumes": volumes
            }

            entities.update(volume_entities)

        if server.nics:
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
        if server.attach_volumes:
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

        if not entities:
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

    @staticmethod
    def _create_privatecrossconnect_dict(privatecrossconnect):
        properties = {}

        if privatecrossconnect.name:
            properties['name'] = privatecrossconnect.name

        if privatecrossconnect.description:
            properties['description'] = privatecrossconnect.description

        raw = {
            "properties": properties
        }

        return raw

    @staticmethod
    def _create_backupunit_dict(backupunit):
        properties = {}

        if backupunit.name:
            properties['name'] = backupunit.name

        if backupunit.password:
            properties['password'] = backupunit.password

        if backupunit.email:
            properties['email'] = backupunit.email

        raw = {
            "properties": properties
        }

        return raw