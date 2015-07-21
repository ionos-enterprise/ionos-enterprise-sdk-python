"""List LANs
"""
from profitbricks.client import ProfitBricksService

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = ProfitBricksService(
    username='username', password='password')

lans = client.list_lans(datacenter_id=datacenter_id)

print(lans)

"""Create Complex LAN
"""
from profitbricks.client import ProfitBricksService, LAN

lan_id = '4'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = ProfitBricksService(
    username='username', password='password')

nics = ['<NIC-ID-1>', '<NIC-ID-2>']

i = LAN(
    name='public Lan 4',
    public=True,
    nics=nics)

response = client.create_lan(datacenter_id=datacenter_id, lan=i)

"""Create LAN
"""
from profitbricks.client import ProfitBricksService, LAN

lan_id = '4'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = ProfitBricksService(
    username='username', password='password')

i = LAN(
    name='public Lan 4',
    public=True)

response = client.create_lan(datacenter_id=datacenter_id, lan=i)

"""Get LAN Members
"""
from profitbricks.client import ProfitBricksService

lan_id = '4'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = ProfitBricksService(
    username='username', password='password')

members = client.get_lan_members(datacenter_id=datacenter_id,
                                 lan_id=lan_id)
