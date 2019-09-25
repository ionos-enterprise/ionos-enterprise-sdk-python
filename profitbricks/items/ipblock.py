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
