import ionoscloud

class AuthAdaptor:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_api_client(self):
        return ionoscloud.ApiClient(ionoscloud.Configuration(
            username = self.username,
            password = self.password
        ))