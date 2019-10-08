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
