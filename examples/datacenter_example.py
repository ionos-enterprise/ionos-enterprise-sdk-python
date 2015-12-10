"""List Datacenters
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

datacenters = client.list_datacenters()

for d in datacenters['items']:
    vdc = client.get_datacenter(d['id'])
    name = vdc['properties']['name']
    if name is


for d in datacenters['items']:
    vdc = client.get_datacenter(d['id'])
    vdc['properties']['name']
    if dc_name == vdc['properties']['name']:


"""Get Datacenter
"""
from profitbricks.client import ProfitBricksService

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = ProfitBricksService(
    username='username', password='password')

datacenter = client.get_datacenter(
    datacenter_id=datacenter_id)

"""Create Simple Datacenter
"""
from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Volume, Server

client = ProfitBricksService(
    username='username', password='password')

i = Datacenter(
    name='dc1',
    description='My New Datacenter',
    location='de/fkb'
    )

response = client.create_datacenter(datacenter=i)

"""Create Complex Datacenter
"""

from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Volume, Server
from profitbricks.client import LAN, NIC, LoadBalancer, FirewallRule, IPBlock, Server


image_id = '226ed8c0-a2fe-11e4-b187-5f1f641608c8'

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

nic1 = NIC(
    name='nic1',
    ips=['10.2.2.3'],
    dhcp='true',
    lan=1,
    firewall_active=True,
    firewall_rules=fw_rules
    )

nic2 = NIC(
    name='nic2',
    ips=['10.2.3.4'],
    dhcp='true',
    lan=1,
    firewall_active=True,
    firewall_rules=fw_rules
    )

nics = [nic1, nic2]

volume1 = Volume(
    name='volume1',
    size=56,
    image=image_id,
    bus='VIRTIO'
    )

volume2 = Volume(
    name='volume2',
    size=56,
    image=image_id,
    bus='VIRTIO'
    )

volumes = [volume2]

server1 = Server(
    name='My New Server1',
    ram=4096,
    cores=4,
    nics=nics,
    create_volumes=[volume1]
    )

servers = [server1]

lan1 = LAN(
    name='public Lan 4',
    public=True
    )

lan2 = LAN(
    name='public Lan 5',
    public=True
    )

lans = [lan1, lan2]

loadbalancer1 = LoadBalancer(
    name='LB01',
    ip='10.2.2.5',
    dhcp=False)

loadbalancers = [loadbalancer1]

d = Datacenter(
    name='My New Datacenter',
    description='Production environment',
    location='de/fkb',
    servers=servers,
    volumes=volumes,
    lans=lans,
    loadbalancers=loadbalancers
    )

response = client.create_datacenter(datacenter=d)
