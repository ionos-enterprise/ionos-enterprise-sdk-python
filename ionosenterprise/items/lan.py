class LAN(object):
    """
    This is the main class for managing LAN resources.
    """

    def __init__(self, name=None, public=None, nics=None, pcc_id=None):
        """
        LAN class initializer.

        :param      name: The name of the LAN.
        :type       name: ``str``

        :param      public: Indicates if the LAN is public.
        :type       public: ``bool``

        :param      nics: A list of NICs
        :type       nics: ``list``

        :param      pcc_id: Unique identifier of the private cross connect the given LAN is connected to if any
        :type       pcc_id: ``str``

        """
        if nics is None:
            nics = []
        self.name = name
        self.public = public
        self.nics = nics
        self.pcc = pcc_id

    def __repr__(self):
        return (('<LAN: name=%s, public=%s, nics=%s, pcc_id=%s> ...>')
                % (self.name, str(self.public), str(self.nics), str(self.pcc)))
