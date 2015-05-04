from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='spc@profitbricks.com', password='spc2015', host_base='https://spc.profitbricks.com/rest')

client = ProfitBricksService(
    username='vendors@stackpointcloud.com',
    password='*******',
    host_base='https://api.profitbricks.com/rest')

for res in client.list_servers('b0ac144e-e294-415f-ba39-6737d5a9d419')['items']: print res['properties']['name'],res['properties']['vmState']
datacenter_id = 'b0ac144e-e294-415f-ba39-6737d5a9d419'





image_id = '226ed8c0-a2fe-11e4-b187-5f1f641608c8'

datacenter_id = 'a2259c2b-f8fc-49a8-80e3-4e00980a4ba7'

image = client.update_image(
    image_id,
    name='New name')

images = client.list_images()
print(images['items'][0])


"""Datacenter Live Tests
"""

from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Volume, Server
from profitbricks.client import LAN, NIC, LoadBalancer, FirewallRule

client = ProfitBricksService(
    username='spc@profitbricks.com', password='spc2015', host_base='https://spc.profitbricks.com/rest')

datacenter_id = 'a2259c2b-f8fc-49a8-80e3-4e00980a4ba7'


' Create Simple '

i = Datacenter(
    name='datacenter5',
    description='My New Datacenter',
    location='de/fkb'
    )

response = client.create_datacenter(datacenter=i)


datacenter = client.update_datacenter(
    datacenter_id=datacenter_id,
    name='datacenter5  \ updated')


"""Server
"""

datacenter_id = '96e7f598-83c2-42fd-a096-75c00073491a'
server_id = 'c6675bc1-f59e-4cd5-8b30-4e028fa0bb19'
volume_id='d955fbf6-9fe6-4856-ac5d-5eead6ca8e54'

volume_id_attach='6a599fbc-6d62-4feb-aa5a-8eb2ff44b448'
image_id = '226ed8c0-a2fe-11e4-b187-5f1f641608c8'
cdrom_id = '34dd35a2-a2ff-11e4-b187-5f1f641608c8'
snapshot_id = '40cb5a55-c8dc-4067-a4ef-ad9e26c01e29'
nic_id = '7f93bff9-d397-474f-bf44-c5bac5320ec5'
loadbalancer_id = '7f3f8db4-993e-4ad0-8073-5a37528ee17e'
ipblock_id = 'd0000fac-1c1a-4bd3-898a-6559487b23f0'
loadbalancer_id = '7f3f8db4-993e-4ad0-8073-5a37528ee17e'
create_with_volume_id = '950e6bd2-786c-40e9-9b61-50f09a0362fe'
firewall_rule_id = 'ec5a1746-1902-43e3-ae95-9a9e4e693560'
boot_volume = 'bcbc184e-a101-4ecc-885a-8f621ef7129e'


from profitbricks.client import ProfitBricksService, Volume, Datacenter
from profitbricks.client import LAN, NIC, LoadBalancer, FirewallRule, IPBlock, Server

client = ProfitBricksService(
    username='spc@profitbricks.com', password='spc2015', host_base='https://spc.profitbricks.com/rest')


attach_volumes = [create_with_volume_id]

i = Server(
    name='server22',
    ram=4096,
    cores=4,
    attach_volumes=attach_volumes
    )

response = client.create_server(
    datacenter_id=datacenter_id, server=i)


server = client.update_server(
    datacenter_id=datacenter_id,
    server_id=server_id,
    boot_volume='6a599fbc-6d62-4feb-aa5a-8eb2ff44b448',
    cores=16,
    ram=2048,
    name='new name')




client.create_snapshot(datacenter_id, '950e6bd2-786c-40e9-9b61-50f09a0362fe', 'snapshot1','our first one')

' 950e6bd2-786c-40e9-9b61-50f09a0362fe '

client.get_volume(datacenter_id, volume_id='cc64b417-37dd-47ea-8731-b4904c6c9ae9')
client.get_server(datacenter_id=datacenter_id,server_id=server_id)

client.attach_volume(datacenter_id=datacenter_id,server_id=server_id,volume_id=volume_id_attach)
client.detach_volume(datacenter_id=datacenter_id,server_id=server_id,volume_id=volume_id_attach)

# PATCH / UPDATE

from profitbricks.client import ProfitBricksService, Volume, Datacenter
from profitbricks.client import LAN, NIC, LoadBalancer, FirewallRule, IPBlock, Server

client = ProfitBricksService(
    username='spc@profitbricks.com', password='spc2015', host_base='https://spc.profitbricks.com/rest')

datacenter_id = 'a2259c2b-f8fc-49a8-80e3-4e00980a4ba7'
server_id = '207781b9-b1b5-4acb-82b4-1670d23b9d4f'

server = client.update_server(
    datacenter_id=datacenter_id,
    server_id=server_id,
    cores=16,
    ram=2048)

# GET CDROMS

client.get_attached_cdroms(datacenter_id=datacenter_id, server_id=server_id)
client.get_attached_cdrom(datacenter_id=datacenter_id, server_id=server_id,cdrom_id=cdrom_id)

# Server Actions

client.stop_server(datacenter_id=datacenter_id,server_id=server_id)

"""Volume
"""
from profitbricks.client import ProfitBricksService, Volume
from profitbricks.client import LAN, NIC, LoadBalancer, FirewallRule, IPBlock

i = Volume(
    name='volume002',
    size=56,
    image=image_id,
    bus='VIRTIO')

response = client.create_volume(
    datacenter_id=datacenter_id, volume=i)

volume = client.update_volume(
    datacenter_id=datacenter_id,
    volume_id=volume_id,
    size=100,
    name='Resized storage to 100 GB')

client.update_snapshot(snapshot_id,name='new name')
client.delete_volume(datacenter_id,volume_id)

"""LoadBalancer
"""

loadbalancer_id = '5e713ea8-ac52-426b-8137-413b9f0a31be'

client.get_loadbalancer(datacenter_id,loadbalancer_id)

nic_id = '38bd56cc-9cac-429b-a8e2-ce1d82b15d4b'
nic_id_2 = '1286e5bd-d838-4de5-9e6a-f9326ea10e27'

balancednics = [nic_id]

i = LoadBalancer(
    name='My LB 6000',
    balancednics=balancednics)

i = LoadBalancer(
    name='My LB2')


response = client.create_loadbalancer(
    datacenter_id=datacenter_id, loadbalancer=i)

nic_id = '88d2fb81-366a-4040-8330-58208d984058'

client.get_nic(datacenter_id,server_id,nic_id)
client.update_nic(datacenter_id,server_id,nic_id,name='new nic name')
client.delete_nic(datacenter_id,server_id,nic_id)

i = IPBlock(location='de/fra', size=5)
ipblock = client.reserve_ipblock(i)

client.delete_ipblock(ipblock_id)

' Curl '
curl --include --request DELETE --header "Authorization: Basic $ENCODED" https://spc.profitbricks.com/rest/datacenters/a2259c2b-f8fc-49a8-80e3-4e00980a4ba7/servers/207781b9-b1b5-4acb-82b4-1670d23b9d4f
curl --include --request PATCH --header "Authorization: Basic $ENCODED" --header "Content-Type: application/vnd.profitbricks.partial-properties+json" --data-binary "{ \"cores\": 16}" https://spc.profitbricks.com/rest/datacenters/a2259c2b-f8fc-49a8-80e3-4e00980a4ba7/servers/207781b9-b1b5-4acb-82b4-1670d23b9d4f
curl --include --request POST --header "Authorization: Basic $ENCODED" --header "Content-Type: application/vnd.profitbricks.resource+json" --data-binary "{\"properties\": {\"description\": \"my new datacenter\", \"name\": \"datacenter1\", \"location\": \"de/fkb\"}}" https://spc.profitbricks.com/rest/datacenters
curl --include --request POST --header "Authorization: Basic $ENCODED" --header "Content-Type: application/x-www-form-urlencoded" https://spc.profitbricks.com/rest/datacenters/a2259c2b-f8fc-49a8-80e3-4e00980a4ba7/servers/207781b9-b1b5-4acb-82b4-1670d23b9d4f/stop

i = FirewallRule(
    name='Open SSH port',
    protocol='TCP',
    source_mac='01:23:45:67:89:00',
    source_ip='12.2.11.22',
    port_range_start=22,
    port_range_end=1000
    )


response = client.create_firewall_rule(
    datacenter_id=datacenter_id,
    server_id=server_id,
    nic_id=nic_id,
    firewall_rule=i)



volume1 = Volume(
    name='volume1',
    size=7,
    image=image_id,
    bus='VIRTIO'
    )

volume2 = Volume(
    name='volume2',
    size=7,
    image=image_id,
    bus='VIRTIO'
    )

create_volumes = [volume1, volume2]

i = Server(
    name='server2',
    ram=4096,
    cores=4,
    create_volumes=create_volumes
    )

response = client.create_server(
    datacenter_id=datacenter_id, server=i)
