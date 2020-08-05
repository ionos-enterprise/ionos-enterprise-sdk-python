class PrivateCrossConnect(object):
    def __init__(self, name=None, description=None, peers=None, connectableDatacenters=None):
        """
        The PrivateCrossConnect class initializer.

        :param      name: Private Cross-Connect name..
        :type       name: ``str``

        :param      description: The data center geographical location.
        :type       description: ``str``

        :param      peers:
                        "example": "{ "peers": [ { "id": "<lan-id>", "name": "<lan-name>", "datacenterId": "<dc-uuid>",  "datacenterName": "<dc-name>", "location": "<de/fra>"} ] }",
    "                   description": "Read-Only attribute. Lists LAN's joined to this private cross connect"
        :type       peers: ``array``

        :param      connectableDatacenters:
                        "example": "{ "connectableDatacenters": [ { "id": "<dc-id>", "name": "<dc-name>", "location": "<de/fra>"} ] }",
                        "description": "Read-Only attribute. Lists datacenters that can be joined to this private cross connect",
        :type       connectableDatacenters: ``list``

        """

        self.name = name
        self.description = description
        self.peers = peers
        self.connectableDatacenters = connectableDatacenters

    def __repr__(self):
        return (('<PrivateCrossConnect: name=%s, description=%s, peers=%s, peers=%s> ...>')
                % (self.name, self.description, self.peers, self.connectableDatacenters))
