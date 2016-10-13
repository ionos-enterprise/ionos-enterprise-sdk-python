The ProfitBricks Client Library for Python provides you with access to the ProfitBricks REST API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python. 

This guide will walk you through getting setup with the library and performing various actions against the API.  

## Table of Contents

* [Concepts](#concepts)
* [Getting Started](#getting-started)
* [Installation](#installation)
* [Authenticating](#authenticating)
* [Using the Module](#using-the-module)
* [Additional Documentation and Support](#additional-documentation-and-support)
* [How to: Create a Datacenter](#how-to-create-a-datacenter)
* [How to: Delete a Datacenter](#how-to-delete-a-datacenter)
* [How to: Update Cores, Memory, and Disk](#how-to-update-cores-memory-and-disk)
* [How to: List Servers, Volumes, and Data Centers](#how-to-list-servers-volumes-and-data-centers)
* [How to: Create Additional Network Interfaces](#how-to-create-additional-network-interfaces)
* [How to: Check Resource Status](#how-to-check-resource-status)
* [Conclusion](#conclusion)

## Concepts

The Python Client Library wraps the latest version of the ProfitBricks REST API. All API operations are performed over SSL and authenticated using your ProfitBricks portal credentials. The API can be accessed within an instance running in ProfitBricks or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response. 

## Getting Started

Before you begin you will need to have [signed-up](https://www.profitbricks.com/signup) for a ProfitBricks account. The credentials you setup during sign-up will be used to authenticate against the API. 
 
## Installation

The Python Client Library is available on [PyPi](https://pypi.python.org/pypi/profitbricks). You can install the latest stable version using pip:

    pip install profitbricks
    
Done!

## Authenticating

Connecting to ProfitBricks is handled by first setting up your authentication.  

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='username', password='password')

You can now use `client` for any future request. 

## Using the Module

Here are a few examples on how to use the module. In this first one we pull a list of our datacenters. 

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='username', password='password')

    datacenters = client.list_datacenters()

And in this one we reserve an IPBlock:

    from profitbricks.client import ProfitBricksService, IPBlock

    client = ProfitBricksService(
        username='username', password='password')

    i = IPBlock(location='de/fra', size=5)

    ipblock = client.reserve_ipblock(i)

Some object creation supports simple and complex requests, such as a server which can be created simply by doing this: 

    from profitbricks.client import ProfitBricksService
    from profitbricks.client import Server, NIC, Volume

    datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

    client = ProfitBricksService(
        username='username', password='password')

    i = Server(
        name='server1',
        ram=4096,
        cores=4
        )
    
    response = client.create_server(
        datacenter_id=datacenter_id,
        server=i)

Or if you want one with some volumes and NICs you would do: 

    from profitbricks.client import ProfitBricksService
    from profitbricks.client import Server, NIC, Volume

    server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
    datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

    client = ProfitBricksService(
        username='username', password='password')

    nic1 = NIC(
        name='nic1',
        ips=['10.2.2.3'],
        dhcp='true',
        lan=1,
        firewall_active=True,
        nat=False
        )

    nic2 = NIC(
        name='nic2',
        ips=['10.2.3.4'],
        dhcp='true',
        lan=1,
        firewall_active=True,
        )

    volume1 = Volume(
        name='volume1',
        size=56,
        image='<IMAGE/SNAPSHOT-ID>',
        bus='VIRTIO'
        ssh_keys=['ssh-rsa AAAAB3NzaC1yc2EAAAADAQ...'],
        image_password='s3cr3tpass0rd',
        availability_zone='ZONE_3'
        )

    volume2 = Volume(
        name='volume2',
        size=56,
        image='<IMAGE/SNAPSHOT-ID>',
        type='SSD',
        bus='VIRTIO',
        license_type='OTHER'
        )

    nics = [nic1, nic2]
    create_volumes = [volume1, volume2]

    i = Server(
        name='server1',
        ram=4096,
        cores=4,
        cpu_family='INTEL_XEON',
        nics=nics,
        create_volumes=create_volumes
        )

    response = client.create_server(
        datacenter_id=datacenter_id, server=i)

**Notes on volumes**:

* You will need to provide either the `image` or the `licence_type` parameter. The `licence_type` is required, but ProfitBricks images will already have a `licence_type` set.
* A list of public SSH keys and/or the image root password can added to the volume. Only official ProfitBricks base images support the `ssh_keys` and `image_password` parameters.

## Additional Documentation and Support

You can find additional examples in the repo `examples` directory. If you find any issues, please let us know via the DevOps Central community or GitHub's issue system and we'll check it out. 


## How to: Create a Datacenter

ProfitBricks introduces the concept of Virtual Datacenters. These are logically separated from one and the other and allow you to have a self-contained environment for all servers, volumes, networking, snapshots, and so forth. The goal is to give you the same experience as you would have if you were running your own physical datacenter.

You will need a datacenter before you can create anything else. Like the server functions, the datacenter functions can be used to create a simple vDC or a complex one. 

To create a simple one you would do this: 

    from profitbricks.client import ProfitBricksService
    from profitbricks.client import Datacenter, Volume, Server

    client = ProfitBricksService(
        username='username', password='password')

    i = Datacenter(
        username='username',
        password='password',
        name='datacenter1',
        description='My New Datacenter',
        location='de/fkb'
        )

    response = client.create_datacenter(datacenter=i)

To create a complex datacenter you would do this. As you can see, you can create quite a few of the objects you will need later all in one request. These all get serialized in a request queue which you can check using the Requests functions: 

    from profitbricks.client import ProfitBricksService
    from profitbricks.client import Datacenter, Volume, Server
    from profitbricks.client import LAN, NIC, LoadBalancer, FirewallRule

    client = ProfitBricksService(
        username='username', password='password')

    fwrule1 = FirewallRule(
        name='Open SSH port',
        protocol='TCP',
        source_mac='01:23:45:67:89:00',
        port_range_start=22
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
        image='<IMAGE/SNAPSHOT-ID>',
        bus='VIRTIO'
        )

    volume2 = Volume(
        name='volume2',
        size=56,
        image='<IMAGE/SNAPSHOT-ID>',
        bus='VIRTIO'
        )

    volumes = [volume2]

    server1 = Server(
        name='server1',
        ram=4096,
        cores=4,
        nics=nics,
        create_volumes=[volume1]
        )

    servers = [server1]

    balancednics = ['<NIC-ID-1>', '<NIC-ID-2>']

    loadbalancer1 = LoadBalancer(
        name='My LB',
        balancednics=balancednics)

    loadbalancers = [loadbalancer1]

    lan1 = LAN(
        name='public Lan 4',
        public=True
        )

    lan2 = LAN(
        name='public Lan 4',
        public=True
        )

    lans = [lan1, lan2]

    d = Datacenter(
        name='datacenter1',
        description='my DC',
        location='de/fkb',
        servers=servers,
        volumes=volumes,
        loadbalancers=loadbalancers,
        lans=lans
        )

    response = client.create_datacenter(datacenter=d)

## How to: Delete a Datacenter

You will want to exercise a bit of caution here. Removing a datacenter will **destroy** all objects contained within that datacenter -- servers, volumes, snapshots, and so on. The objects -- once removed -- will be unrecoverable. 

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='username', password='password')

    datacenter_id = '700e1cab-99b2-4c30-ba8c-
    datacenter = client.delete_datacenter(datacenter_id=datacenter_id)

## How to: Update Cores, Memory, and Disk

ProfitBricks allows users to dynamically update cores, memory, and disk independently of each other. This removes the restriction of needing to upgrade to the next size up to receive an increase in memory. You can now simply increase the instances memory keeping your costs in-line with your resource needs. 

The following code illustrates how you can update cores and memory: 

    from profitbricks.client import ProfitBricksService

    datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
    server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

    client = ProfitBricksService(
        username='username', password='password')

    server = client.update_server(
        datacenter_id=datacenter_id,
        server_id=server_id,
        cores=16,
        ram=2048)

 This is how you would update your volume's size: 
 
    from profitbricks.client import ProfitBricksService, Volume
    
    datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
    volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'
    
    client = ProfitBricksService(
        username='username', password='password')
    
    volume = client.update_volume(
        datacenter_id=datacenter_id,
        volume_id=volume_id,
        size=100,
        name='Resized storage to 100 GB',
        cpu_hot_unplug=True)


## How to: List Servers, Volumes, and Data Centers

Listing resources is fairly straight forward. 

Grabbing the datacenters:

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='username', password='password')

    datacenters = client.list_datacenters() 

Your servers:

    from profitbricks.client import ProfitBricksService

    datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

    client = ProfitBricksService(
        username='username', password='password')

    servers = client.list_servers(datacenter_id=datacenter_id)

Finally, your volumes: 

    from profitbricks.client import ProfitBricksService

    datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

    client = ProfitBricksService(
        username='username', password='password')

    volumes = self.volume.list_volumes(
        datacenter_id=datacenter_id)

## How to: Create Additional Network Interfaces

The ProfitBricks platform supports adding multiple NICs to a server. These NICs can be used to create different, segmented networks on the platform. 

The sample below shows you how to add a second NIC to an existing server: 

    from profitbricks.client import ProfitBricksService, FirewallRule, NIC

    datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
    server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'

    client = ProfitBricksService(
        username='username', password='password')

    i = NIC(
        name='nic1',
        ips=['10.2.2.3','10.2.3.4'],
        dhcp='true',
        lan=1,
        firewall_active=True
        )

    response = client.create_nic(
        datacenter_id=datacenter_id,
        server_id=server_id,
        nic=i)

## How to: Check Resource Status

When a new resource (server, volume, NIC, etc.) is created, the return value will include a `requestId` UUID value. This value can be passed to the `get_request()` method to retrieve the request status and any potential error messages produced by the request.

    client.get_request('3e2d336f-cdf5-482b-923a-f3026dfc934b', status=True)

The request status can be repeatedly polled until the resource create resource operation completes with a `DONE` or `FAILED` status. An example poller method might look something like this:

    def wait_for_completion(conn, response, timeout):
        if not response:
            return
        timeout = time.time() + timeout
        while timeout > time.time():
            time.sleep(5)
            request = conn.get_request(
                request_id=response['requestId'],
                status=True)

            if request['metadata']['status'] == 'DONE':
                return
            elif request['metadata']['status'] == 'FAILED':
                raise Exception('Request {0} failed to complete: {1}'.format(
                    response['requestId'], request['metadata']['message']))

        raise Exception('Timed out waiting for request {0}.'.format(
            response['requestId']))

The above method can then be called after creating a new resource.

    i = Server(
        name='server1',
        ram=4096,
        cores=4)

    response = client.create_server(
        datacenter_id=datacenter_id,
        server=i)

    wait_for_completion(client, response, 300)

## Conclusion

We touched on only a few ways you can interact with the ProfitBricks API using python. Our repo, located [here], has further examples. If you have any other question, ping us in the community. 
