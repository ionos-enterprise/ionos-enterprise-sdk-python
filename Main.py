from ionosenterprise.client import IonosEnterpriseService
from ionosenterprise.items import Datacenter
from ionosenterprise.items import NIC
from ionosenterprise.items import Server
from ionosenterprise.items import FirewallRule
from ionosenterprise.items import Group
from ionosenterprise.items import IPBlock
from ionosenterprise.items import LAN
from ionosenterprise.items import LoadBalancer
from ionosenterprise.items import User
import ionos_cloud_sdk
from ionos_cloud_sdk.rest import ApiException
import json
from ionosenterprise.items import Volume
from ionosenterprise.errors import (
    ICNotAuthorizedError,
    ICNotFoundError,
    ICValidationError,
    ICRateLimitExceededError,
    ICError
)

with open('credentials.json', 'r') as outfile:
    credentials = json.load(outfile)

""" CREATE CLIENT """
client = IonosEnterpriseService(username=credentials['username'], password=credentials['password'])

print(client.list_contracts())
exit()