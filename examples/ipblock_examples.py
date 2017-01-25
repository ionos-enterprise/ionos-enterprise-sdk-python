import os
"""List IPBlocks
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username=os.getenv('PROFITBRICKS_USERNAME'), password=os.getenv('PROFITBRICKS_PASSWORD'))

ipblocks = client.list_ipblocks()

print(ipblocks)

"""Reserve IPBlock
"""
from profitbricks.client import ProfitBricksService, IPBlock  # noqa

i = IPBlock(name='py-test', location='de/fra', size=1)

ipblock = client.reserve_ipblock(i)

"""Release IPBlock
"""
from profitbricks.client import ProfitBricksService  # noqa

ipblock_id = ipblock['id']


ipblock = client.delete_ipblock(ipblock_id)
