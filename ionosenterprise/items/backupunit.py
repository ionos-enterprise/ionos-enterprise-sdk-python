class BackupUnit(object):
    def __init__(self, name, password=None, email=None):
        """
        BackupUnit class initializer.

        :param      name: A name of that resource (only alphanumeric characters are acceptable)"
        :type       name: ``str``

        :param      password: The password associated to that resource.
        :type       password: ``str``

        :param      email: The email associated with the backup unit. Bear in mind that this email does not be the same email as of the user.
        :type       email: ``str``

        """
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return ('<BackupUnit: name=%s, password=%s, email=%s>'
                % (self.name, str(self.password), self.email))
