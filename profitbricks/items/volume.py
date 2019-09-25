class Volume(object):
    def __init__(self, name=None, size=None, bus='VIRTIO',  # pylint: disable=unused-argument
                 image=None, image_alias=None, disk_type='HDD', licence_type='UNKNOWN',
                 image_password=None, ssh_keys=None, availability_zone='AUTO',
                 **kwargs):
        """
        Volume class initializer.

        :param      name: The name of the volume.
        :type       name: ``str``

        :param      size: The size of the volume.
        :type       size: ``str``

        :param      bus: The bus type. Def. VIRTIO.
        :type       bus: ``str``

        :param      image: The image ID to use.
        :type       image: ``str``

        :param      image_alias: An alias of the image to use.
        :type       image_alias: ``str``

        :param      disk_type: The type of storage. Def. HDD
        :type       disk_type: ``str``

        :param      licence_type: The licence type.
        :type       licence_type: ``str``

        :param      ssh_keys: A list of public SSH keys.
        :type       ssh_keys: ``list``

        :param      availability_zone: The availability zone for the server.
        :type       availability_zone: ``str``

        """
        if ssh_keys is None:
            ssh_keys = []
        self.name = name
        self.availability_zone = availability_zone
        self.size = size
        self.image = image
        self.image_alias = image_alias
        self.bus = bus
        self.disk_type = disk_type
        self.licence_type = licence_type
        self.image_password = image_password
        self.ssh_keys = ssh_keys

    def __repr__(self):
        return (('<Volume: name=%s, size=%s, image=%s, image_alias=%s,'
                 'bus=%s, disk_type=%s, ...>')
                % (self.name, str(self.size), self.image,
                   self.image_alias, self.bus, self.disk_type))
