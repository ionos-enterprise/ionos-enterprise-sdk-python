class Snapshot(object):
    def __init__(self, name=None, description=None,  # pylint: disable=unused-argument
                 licence_type='UNKNOWN', size=None, location=None, **kwargs):
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
