class User(object):
    def __init__(self, firstname=None, lastname=None,
                 email=None, password=None,
                 administrator=None,
                 force_sec_auth=None):
        """
        User class initializer.

        :param      firstname: The user's first name.
        :type       firstname: ``str``

        :param      lastname: The user's last name.
        :type       lastname: ``str``

        :param      email: The user's email.
        :type       email: ``str``

        :param      password: A password for the user.
        :type       password: ``str``

        :param      administrator: Indicates if the user have
                                   administrative rights.
        :type       administrator: ``bool``

        :param      force_sec_auth: Indicates if secure (two-factor)
                                    authentication should be forced
                                    for the user.
        :type       force_sec_auth: ``bool``

        """
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.administrator = administrator
        self.force_sec_auth = force_sec_auth

    def __repr__(self):
        return ('<Group: firstname=%s, lastname=%s, email=%s, '
                'password=%s, administrator=%s, force_sec_auth=%s>'
                % (self.firstname, self.lastname,
                   self.email, self.password,
                   str(self.administrator),
                   str(self.force_sec_auth)))
