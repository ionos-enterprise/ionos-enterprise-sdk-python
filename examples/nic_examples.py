"""List NICs
"""
from profitbricks.client import ProfitBricksService

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = ProfitBricksService(
    username='username', password='password')

nics = client.list_nics(
    datacenter_id=datacenter_id,
    server_id=server_id)

for n in nics['items']:
    print(n['properties']['name'])

"""Create NIC
"""
from profitbricks.client import ProfitBricksService, NIC

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

client = ProfitBricksService(
    username='username', password='password')

i = NIC(
    name='nic1',
    ips=['10.2.2.3', '10.2.3.4'],
    dhcp='true',
    lan=1,
    firewall_active=True
    )

response = client.create_nic(
    datacenter_id=datacenter_id,
    server_id=server_id,
    nic=i)

"""Create NIC with FirewallRules
"""
from profitbricks.client import ProfitBricksService, FirewallRule, NIC

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
nic_id = '<NIC-ID>'

client = ProfitBricksService(
    username='username', password='password')

fwrule1 = FirewallRule(
    name='Open SSH port',
    protocol='TCP',
    source_mac='01:23:45:67:89:00',
    port_range_start=22,
    port_range_end=22
    )

fwrule2 = FirewallRule(
    name='Allow PING',
    protocol='ICMP',
    icmp_type=8,
    icmp_code=0
    )

fw_rules = [fwrule1, fwrule2]

i = NIC(
    name='nic1',
    ips=['10.2.2.3', '10.2.3.4'],
    dhcp='true',
    lan=1,
    firewall_active=True,
    firewall_rules=fw_rules
    )

response = client.create_nic(
    datacenter_id=datacenter_id,
    server_id=server_id, nic=i)
