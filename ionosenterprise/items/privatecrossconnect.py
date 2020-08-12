class PrivateCrossConnect(object):
    def __init__(self, name=None, description=None):
        """
        The PrivateCrossConnect class initializer.

        :param      name: Private Cross-Connect name..
        :type       name: ``str``

        :param      description: The data center geographical location.
        :type       description: ``str``

        """

        self.name = name
        self.description = description

    def __repr__(self):
        return (('<PrivateCrossConnect: name=%s, description=%s> ...>')
                % (self.name, self.description))
