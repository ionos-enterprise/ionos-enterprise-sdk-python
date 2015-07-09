"""List IPBlocks
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

ipblocks = client.list_ipblocks()

print(ipblocks)

"""Reserve IPBlock
"""
from profitbricks.client import ProfitBricksService, IPBlock

client = ProfitBricksService(
    username='username', password='password')

i = IPBlock(location='de/fra', size=5)

ipblock = client.reserve_ipblock(i)

"""Release IPBlock
"""
from profitbricks.client import ProfitBricksService

ipblock_id = '854467eb-a0d3-4651-ac83-754e2faedba4'

client = ProfitBricksService(
    username='username', password='password')

ipblock = client.delete_ipblock(ipblock_id)
