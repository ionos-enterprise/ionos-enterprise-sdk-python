import ionossdk

class AuthAdaptor:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_api_client(self):
        return ionossdk.ApiClient(ionossdk.Configuration(
            username = self.username,
            password = self.password
        ))