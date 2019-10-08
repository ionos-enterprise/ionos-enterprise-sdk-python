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
