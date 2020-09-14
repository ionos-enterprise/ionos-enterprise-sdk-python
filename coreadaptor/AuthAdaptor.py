import ionos_cloud_sdk

class AuthAdaptor:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_api_client(self):
        return ionos_cloud_sdk.ApiClient(ionos_cloud_sdk.Configuration(
            username = self.username,
            password = self.password
        ))