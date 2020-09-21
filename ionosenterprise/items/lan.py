class LAN(object):
    """
    This is the main class for managing LAN resources.
    """

    def __init__(self, name=None, public=None, nics=None, pcc=None):
        """
        LAN class initializer.

        :param      name: The name of the LAN.
        :type       name: ``str``

        :param      public: Indicates if the LAN is public.
        :type       public: ``bool``

        :param      nics: A list of NICs
        :type       nics: ``list``

        :param      pcc: Unique identifier of the private cross connect the given LAN is connected to if any
        :type       pcc: ``str``

        """
        if nics is None:
            nics = []
        self.name = name
        self.public = public
        self.nics = nics
        self.pcc = pcc

    def __repr__(self):
        return (('<LAN: name=%s, public=%s, nics=%s, pcc=%s> ...>')
                % (self.name, str(self.public), str(self.nics), str(self.pcc)))
