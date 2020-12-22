import ionoscloud
from coreadaptor.IonosCoreProxy import IonosCoreProxy
from ..utils import find_item_by_name


class datacenter:

    @IonosCoreProxy.process_response
    def list_datacenters(self, depth=1):
        """
        Retrieves a list of all data centers.
        """
        return self.get_api_instance(ionoscloud.DataCenterApi)\
            .datacenters_get_with_http_info(depth=depth, response_type='object')

    @IonosCoreProxy.process_response
    def get_datacenter(self, datacenter_id, depth=1):
        """
        Retrieves a data center by its ID.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        :param      depth: The depth of the response data.
        :type       depth: ``int``

        """
        return self.get_api_instance(ionoscloud.DataCenterApi)\
            .datacenters_find_by_id_with_http_info(
                datacenter_id, depth=depth, response_type='object'
            )

    @IonosCoreProxy.process_response
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
        if not data_center:
            raise NameError("No data center found with name "
                            "containing '{name}'.".format(name=name))
        if len(data_center) > 1:
            raise NameError("Found {n} data centers with the name '{name}': {names}".format(
                n=len(data_center),
                name=name,
                names=", ".join(d['properties']['name'] for d in data_center)
            ))
        return data_center[0]

    @IonosCoreProxy.process_response
    def delete_datacenter(self, datacenter_id):
        """
        Removes the data center and all its components such as servers, NICs,
        load balancers, volumes.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        """
        return self.get_api_instance(ionoscloud.DataCenterApi)\
            .datacenters_delete_with_http_info(datacenter_id)

    @IonosCoreProxy.process_response
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
        if datacenter.servers:
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
        if datacenter.volumes:
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
        if datacenter.loadbalancers:
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
        if datacenter.lans:
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

        if not entities:
            raw = {
                "properties": properties,
            }
        else:
            raw = {
                "properties": properties,
                "entities": entities
            }

        if 'entities' not in raw:
            datacenter = ionoscloud.models.Datacenter(properties=raw['properties'])
        else:
            datacenter = ionoscloud.models.Datacenter(
                properties=raw['properties'], entities=raw['entities'])

        return self.get_api_instance(ionoscloud.DataCenterApi)\
            .datacenters_post_with_http_info(datacenter, response_type='object')

    @IonosCoreProxy.process_response
    def update_datacenter(self, datacenter_id, **kwargs):
        """
        Updates a data center with the parameters provided.

        :param      datacenter_id: The unique ID of the data center.
        :type       datacenter_id: ``str``

        """
        data = {}

        for attr, value in kwargs.items():
            data[self._underscore_to_camelcase(attr)] = value

        return self.get_api_instance(ionoscloud.DataCenterApi) \
            .datacenters_put_with_http_info(
            datacenter_id,
                ionoscloud.models.Datacenter(
                    properties=data
                )
            )
