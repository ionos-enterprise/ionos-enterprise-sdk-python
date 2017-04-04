# Python SDK

Version: profitbricks-sdk-python **3.1.2**

## Table of Contents

* [Description](#description)
* [Getting Started](#getting-started)
  * [Installation](#installation)
  * [Authenticating](#authenticating)
  * [Error Handling](#error-handling)
* [Reference](#reference)
  * [Data Centers](#data-centers)
    * [List Data Centers](#list-data-centers)
    * [Retrieve a Data Center](#retrieve-a-data-center)
    * [Create a Data Centers](#create-a-data-center)
    * [Update a Data Centers](#update-a-data-center)
    * [Delete a Data Centers](#delete-a-data-center)
  * [Locations](#locations)
    * [List Locations](#list-locations)
    * [Get a Location](#get-a-location)
  * [Servers](#servers)
    * [List Servers](#list-servers)
    * [Retrieve a Server](#retrieve-a-server)
    * [Create a Server](#create-a-server)
    * [Update a Server](#update-a-server)
    * [Delete a Server](#delete-a-server)
    * [List Attached Volumes](#list-attached-volumes)
    * [Attach a Volume](#attach-a-volume)
    * [Retrieve an Attached Volume](#retrieve-an-attached-volume)
    * [Detach a Volume](#detach-a-volume)
    * [List Attached CD-ROMs](#list-attached-cd-roms)
    * [Attach a CD-ROM](#attach-a-cd-rom)
    * [Retrieve an Attached CD-ROM](#retrieve-an-attached-cd-rom)
    * [Detach a CD-ROM](#detach-a-cd-rom)
    * [Reboot a Server](#reboot-a-server)
    * [Start a Server](#start-a-server)
    * [Stop a Server](#stop-a-server)
  * [Volumes](#volumes)
    * [List Volumes](#list-volumes)
    * [Get a Volume](#get-a-volume)
    * [Create a Volume](#create-a-volume)
    * [Update a Volume](#update-a-volume)
    * [Delete a Volume](#delete-a-volume)
    * [Create a Volume Snapshot](#create-a-volume-snapshot)
    * [Restore a Volume Snapshot](#restore-a-volume-snapshot)
  * [Snapshots](#snapshots)
    * [List Snapshots](#list-snapshots)
    * [Get a Snapshot](#get-a-snapshot)
    * [Update a Snapshot](#update-a-snapshot)
    * [Delete a Snapshot](#delete-a-snapshot)
  * [Load Balancers](#load-balancers)
    * [List Load Balancers](#list-load-balancers)
    * [Get a Load Balancer](#get-a-load-balancer)
    * [Create a Load Balancer](#create-a-load-balancer)
    * [Update a Load Balancer](#update-a-load-balancer)
    * [List Load Balanced NICs](#list-load-balanced-nics)
    * [Get a Load Balanced NIC](#get-a-load-balanced-nic)
    * [Associate NIC to a Load Balancer](#associate-nic-to-a-load-balancer)
    * [Remove a NIC Association](#remove-a-nic-association)
  * [Firewall Rules](#firewall-rules)
    * [List Firewall Rules](#list-firewall-rules)
    * [Get a Firewall Rule](#get-a-firewall-rule)
    * [Create a Firewall Rule](#create-a-firewall-rule)
    * [Update a Firewall Rule](#update-a-firewall-rule)
    * [Delete a Firewall Rule](#delete-a-firewall-rule)
  * [Images](#images)
    * [List Images](#list-images)
    * [Get an Image](#get-an-image)
    * [Update an Image](#update-an-image)
    * [Delete an Image](#delete-an-image)
  * [Network Interfaces (NICs)](#network-interfaces-nics)
    * [List NICs](#list-nics)
    * [Get a NIC](#get-a-nic)
    * [Create a NIC](#create-a-nic)
    * [Update a NIC](#update-a-nic)
    * [Delete a NIC](#delete-a-nic)
  * [IP Blocks](#ip-blocks)
    * [List IP Blocks](#list-ip-blocks)
    * [Get an IP Block](#get-an-ip-block)
    * [Create an IP Block](#create-an-ip-block)
    * [Delete an IP Block](#delete-an-ip-block)
  * [Requests](#requests)
    * [List Requests](#list-requests)
    * [Get a Request](#get-a-request)
    * [Get a Request Status](#get-a-request-status)
  * [LANs](#lans)
    * [List LANs](#list-lans)
    * [Create a LAN](#create-a-lan)
    * [Get a LAN](#get-a-lan)
    * [Update a LAN](#update-a-lan)
    * [Delete a LAN](#delete-a-lan)
* [Examples](#examples)
* [Support](#support)
* [Testing](#testing)
* [Contributing](#contributing)

## Description

The ProfitBricks Client Library for Python provides you with access to the ProfitBricks Cloud API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python.

This guide will walk you through getting setup with the library and performing various actions against the API.

The Python Client Library wraps the ProfitBricks Cloud API. All API operations are performed over SSL and authenticated using your ProfitBricks portal credentials. The API can be accessed within an instance running in ProfitBricks or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response.

## Getting Started

Before you begin you will need to have [signed-up](https://www.profitbricks.com/signup) for a ProfitBricks account. The credentials you setup during sign-up will be used to authenticate against the Cloud API.

### Installation

The Python Client Library is available on [PyPi](https://pypi.python.org/pypi/profitbricks). You can install the latest stable version using `pip`:

    pip install profitbricks

Done!

### Authenticating

Connecting to ProfitBricks is handled by first setting up your authentication credentials.

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='YOUR_USERNAME', password='YOUR_PASSWORD')

Replace the values for *YOUR_USERNAME* and *YOUR_PASSWORD* with the ProfitBricks credentials you established during sign-up..

You can now use `client` for any future request.

### Error Handling

The Python Client Library will raise custom exceptions when the Cloud API returns an error. There are five exception types:

| Exception | HTTP Code | Description |
|---|:-:|---|
| PBNotAuthorizedError | 401 | The supplied user credentials are invalid. |
| PBNotFoundError | 404 | The requested resource cannot be found. |
| PBValidationError | 422 | The request body includes invalid JSON. |
| PBRateLimitExceededError | 429 | The Cloud API rate limit has been exceeded. |
| PBError | Other | A generic exception for all other status codes. |


## Reference

This section provides details on all the available operations and the parameters they accept. Brief code snippets demonstrating usage are also included.

`client` is the `ProfitBricksService` class imported `from profitbricks.client import ProfitBricksService`

### Data Centers

Virtual data centers (VDCs) are the foundation of the ProfitBricks platform. VDCs act as logical containers for all other objects you will be creating, e.g., servers. You can provision as many VDCs as you want. VDCs have their own private network and are logically segmented from each other to create isolation.

#### List Data Centers

This operation will list all currently provisioned VDCs that your account credentials provide access to.

There are no request arguments that need to be supplied.

```
datacenters = client.list_datacenters()
```

---

#### Retrieve a Data Center

Use this to retrieve details about a specific VDC.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the virtual data center. |

```
   datacenter = client.get_datacenter(
            datacenter_id='datacenter_id')
```

---

#### Create a Data Center

Use this operation to create a new VDC. You can create a "simple" VDC by supplying just the required *name* and *location* parameters. This operation also has the capability of provisioning a "complex" VDC by supplying additional parameters for servers, volumes, LANs, and/or load balancers.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| name | **yes** | string | The name of the data center. |
| location | **yes** | string | The physical ProfitBricks location where the VDC will be created. |
| description | no | string | A description for the data center, e.g. staging, production. |
| server_items | no | collection | Details about creating one or more servers. See [create a server](#create-a-server). |
| volume_items | no | collection | Details about creating one or more volumes. See [create a volume](#create-a-volume). |
| lan_items | no | collection | Details about creating one or more LANs. See [create-a-lan](#create-a-lan). |
| loadbalancer_items | no | collection | Details about creating one or more load balancers. See [create-a-loadbalancer](#create-a-loadbalancer). |

The following table outlines the locations currently supported:

| Value| Country | City |
|---|---|---|
| us/las | United States | Las Vegas |
| de/fra | Germany | Frankfurt |
| de/fkb | Germany | Karlsruhe |

**NOTES**:
- The value for `name` cannot contain the following characters: (@, /, , |, ‘’, ‘).
- You cannot change the virtual data center `location` once it has been provisioned.

```
i = Datacenter(
    name='name',
    description='My New Datacenter',
    location='de/fkb'
    )

response = client.create_datacenter(datacenter=i)
```

---

#### Update a Data Center

After retrieving a data center, either by getting it by id, or as a create response object, you can change its properties by calling the `update_datacenter` method. Some parameters may not be changed using `update_datacenter`.

The following table describes the available request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | no | string | The new name of the VDC. |
| description | no | string | The new description of the VDC. |

```
datacenter = client.update_datacenter(
	datacenter_id='existing_datacenter_id',
	name='new name'
	description='new description')
```

---

#### Delete a Data Center

This will remove all objects within the data center and remove the data center object itself.

**NOTE**: This is a highly destructive operation which should be used with extreme caution!

The following table describes the available request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC that you want to delete. |

```
response = client.delete_datacenter(datacenter_id='existing_datacenter_id')
```

---

### Locations

Locations are the physical ProfitBricks data centers where you can provision your VDCs.

#### List Locations

The `list_locations` operation will return the list of currently available locations.

There are no request parameters to supply.

```
locations = client.list_locations()
```

---

#### Get a Location

Retrieves the attributes of a specific location.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| location_id | **yes** | string | The ID consisting of country/city. |

```
self.client.get_location('us/las')
```

---

### Servers

#### List Servers

You can retrieve a list of all the servers provisioned inside a specific VDC.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes**  | string | The ID of the VDC. |

```
servers = client.list_servers(datacenter_id='existing_datacenter_id')
```

---

#### Retrieve a Server

Returns information about a specific server such as its configuration, provisioning status, etc.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

```
server = client.get_server(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id'
        )
```

---

#### Create a Server

Creates a server within an existing VDC. You can configure additional properties such as specifying a boot volume and connecting the server to a LAN.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | **yes** | string | The name of the server. |
| cores | **yes** | int | The total number of cores for the server. |
| ram | **yes** | int | The amount of memory for the server in MB, e.g. 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set `ram_hot_plug` to *True* then you must use a minimum of 1024 MB. |
| availability_zone | no | string | The availability zone in which the server should exist. |
| cpu_family | no | string | Sets the CPU type. "AMD_OPTERON" or "INTEL_XEON". Defaults to "AMD_OPTERON". |
| boot_volume_id | no | string | Reference to a volume used for booting. If not *null* then `boot_cdrom` has to be *null*. |
| boot_cdrom | no | string | Reference to a CD-ROM used for booting. If not *null* then `boot_volume_id` has to be *null*. |
| attach_volumes | no | collection | A collection of volume IDs that you want to connect to the server. |
| create_volumes | no | collection | A collection of volume objects that you want to create and attach to the server.|
| nics | no | collection | A collection of NICs you wish to create at the time the server is provisioned. |

The following table outlines the server availability zones currently supported:

| Availability Zone | Comment |
|---|---|
| AUTO | Automatically Selected Zone |
| ZONE_1 | Fire Zone 1 |
| ZONE_2 | Fire Zone 2 |

```
i = Server(
    name='name',
    cores=1,
    ram=2048,
    description='My new server',
    location='de/fkb'
    )
server = client.create_server(
            datacenter_id='datacenter_id',
            server=i)
```

---

#### Update a Server

Perform updates to the attributes of a server.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| name | no | string | The name of the server. |
| cores | no | int | The number of cores for the server. |
| ram | no | int | The amount of memory in the server. |
| availability_zone | no | string | The new availability zone for the server. |
| cpu_family | no | string | Sets the CPU type. "AMD_OPTERON" or "INTEL_XEON". Defaults to "AMD_OPTERON". |
| boot_volume_id | no | string | Reference to a volume used for booting. If not *null* then `boot_cdrom` has to be *null* |
| boot_cdrom | no | string | Reference to a CD-ROM used for booting. If not *null* then `boot_volume_id` has to be *null*. |

After retrieving a server, either by getting it by id, or as a create response object, you can change its properties and call the `update_server` method:

```
server = client.update_server(
            datacenter_id='existing_datacenter_id',
            server_id'existing_server_id',
            name='new name')
```

---

#### Delete a Server

This will remove a server from a data center. **NOTE**: This will not automatically remove the storage volume(s) attached to a server. A separate operation is required to delete a storage volume.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `delete_server` method directly on the object:

```
response = client.delete_server(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id'
        )
```

---

#### List Attached Volumes

Retrieves a list of volumes attached to the server.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `get_attached_volumes` method directly on the object:

```
servers = client.get_attached_volumes(
          datacenter_id='existing_datacenter_id',
          server_id='existing_server_id')
```

---

#### Attach a Volume

This will attach a pre-existing storage volume to the server.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| volume_id | **yes** | string | The ID of a storage volume. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `attach_volume` method directly on the object:

```
 volume = client.attach_volume(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            volume_id='existing_volume_id')
```

---

#### Retrieve an Attached Volume

This will retrieve the properties of an attached volume.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| volume_id | **yes** | string | The ID of the attached volume. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `get_attached_volume` method directly on the object:

```
server = client.get_attached_volume(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            volume_id='existing_volume_id')
```

---

#### Detach a Volume

This will detach the volume from the server. Depending on the volume `hot_unplug` settings, this may result in the server being rebooted.

This will NOT delete the volume from your virtual data center. You will need to make a separate request to delete a volume.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| volume_id | **yes** | string | The ID of the attached volume. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `detach_volume` method directly on the object:

```
volume = client.detach_volume(
           datacenter_id='existing_datacenter_id',
           server_id='existing_server_id',
           volume_id='existing_volume_id')
```

---

#### List Attached CD-ROMs

Retrieves a list of CD-ROMs attached to a server.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `get_attached_cdroms` method directly on the object:

```
cdroms = client.get_attached_cdroms(
            datacenter_id='datacenter_id',
            server_id='server_id')
```

---

#### Attach a CD-ROM

You can attach a CD-ROM to an existing server.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| cdrom_id | **yes** | string | The ID of a CD-ROM. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `attach_cdrom` method directly on the object:

```
attached_cdrom = client.attach_cdrom(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            cdrom_id='existing_cdrom_id')
```

---

#### Retrieve an Attached CD-ROM

You can retrieve a specific CD-ROM attached to the server.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| cdrom_id | **yes** | string | The ID of the attached CD-ROM. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `get_attached_cdrom` method directly on the object:

```
attached_cdrom = client.get_attached_cdrom(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            cdrom_id='attached_cdrom_id')
```

---

#### Detach a CD-ROM

This will detach a CD-ROM from the server.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| cdrom_id | **yes** | string | The ID of the attached CD-ROM. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `detach_cdrom` method directly on the object:

```
detached_cd = client.detach_cdrom(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            cdrom_id='attached_cdrom_id')
```

---

#### Reboot a Server

This will force a hard reboot of the server. Do not use this method if you want to gracefully reboot the machine. This is the equivalent of powering off the machine and turning it back on.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `reboot_server` method directly on the object:

```
server = client.reboot_server(
            datacenter_id='existing_datacenter_id',
            server_id='rebooting_server_id')
```

---

#### Start a Server

This will start a server. If the server's public IP was deallocated then a new IP will be assigned.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `start_server` method directly on the object:

```
server = client.start_server(
           datacenter_id='existing_datacenter_id',
           server_id='starting_server_id')
```

---

#### Stop a Server

This will stop a server. The machine will be forcefully powered off, billing will cease, and the public IP, if one is allocated, will be deallocated.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `stop_server` method directly on the object:

```
server = client.stop_server(
           datacenter_id='existing_datacenter_id',
           server_id='stopping_server_id')
```

---

### Volumes

#### List Volumes

Retrieve a list of volumes within the virtual data center. If you want to retrieve a list of volumes attached to a server please see the [List Attached Volumes](#list-attached-volumes) entry in the Server section for details.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |

```
volumes = client.list_volumes(
            datacenter_id='existing_datacenter_id')
```

---

#### Get a Volume

Retrieves the attributes of a given volume.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |

```
volume = client.get_volume(
            datacenter_id='existing_datacenter_id',
            volume_id='existing_volume_id')
```

---

#### Create a Volume

Creates a volume within the virtual data center. This will NOT attach the volume to a server. Please see the [Attach a Volume](#attach-a-volume) entry in the Server section for details on how to attach storage volumes.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | no | string | The name of the volume. |
| size | **yes** | int | The size of the volume in GB. |
| bus | no | string | The bus type of the volume (VIRTIO or IDE). Default: VIRTIO. |
| image | **yes** | string | The image or snapshot ID. |
| type | **yes** | string | The volume type, HDD or SSD. |
| licence_type | **yes** | string | The licence type of the volume. Options: LINUX, WINDOWS, WINDOWS2016, UNKNOWN, OTHER |
| image_password | **yes** | string | One-time password is set on the Image for the appropriate root or administrative account. This field may only be set in creation requests. When reading, it always returns *null*. The password has to contain 8-50 characters. Only these characters are allowed: [abcdefghjkmnpqrstuvxABCDEFGHJKLMNPQRSTUVX23456789] |
| ssh_keys | **yes** | string | SSH keys to allow access to the volume via SSH. |
| availability_zone | no | string | The storage availability zone assigned to the volume. Valid values: AUTO, ZONE_1, ZONE_2, or ZONE_3. This only applies to HDD volumes. Leave blank or set to AUTO when provisioning SSD volumes. |

The following table outlines the various licence types you can define:

| Licence Type | Comment |
|---|---|
| WINDOWS2016 | Use this for the Microsoft Windows Server 2016 operating system. |
| WINDOWS | Use this for the Microsoft Windows Server 2008 and 2012 operating systems. |
| LINUX |Use this for Linux distributions such as CentOS, Ubuntu, Debian, etc. |
| OTHER | Use this for any volumes that do not match one of the other licence types. |
| UNKNOWN | This value may be inherited when you've uploaded an image and haven't set the license type. Use one of the options above instead. |

The following table outlines the storage availability zones currently supported:

| Availability Zone | Comment |
|---|---|
| AUTO | Automatically Selected Zone |
| ZONE_1 | Fire Zone 1 |
| ZONE_2 | Fire Zone 2 |
| ZONE_3 | Fire Zone 3 |

* You will need to provide either the `image` or the `licence_type` parameters. `licence_type` is required, but if `image` is supplied, it is already set and cannot be changed. Similarly either the `image_password` or `ssh_keys` parameters need to be supplied when creating a volume. We recommend setting a valid value for `image_password` even when using `ssh_keys` so that it is possible to authenticate using the remote console feature of the DCD.

```
i = Volume(
    name='name',
    size=20,
    bus='VIRTIO',
    type='HDD',
    licence_type='LINUX',
    availability_zone='ZONE_3')

volume = client.create_volume(
            datacenter_id='existing_datacenter_id',
            volume=i)
```

---

#### Update a Volume

You can update -- in full or partially -- various attributes on the volume; however, some restrictions are in place:

You can increase the size of an existing storage volume. You cannot reduce the size of an existing storage volume. The volume size will be increased without requiring a reboot if the relevant hot plug settings have been set to *true*. The additional capacity is not added automatically added to any partition, therefore you will need to handle that inside the OS afterwards. Once you have increased the volume size you cannot decrease the volume size.

Since an existing volume is being modified, none of the request parameters are specifically required as long as the changes being made satisfy the requirements for creating a volume.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |
| name | no | string | The name of the volume. |
| size | no | int | The size of the volume in GB. Only increase when updating. |
| bus | no | string | The bus type of the volume (VIRTIO or IDE). Default: VIRTIO. |
| image | no | string | The image or snapshot ID. |
| type | no | string | The volume type, HDD or SSD. |
| licence_type | no | string | The licence type of the volume. Options: LINUX, WINDOWS, WINDOWS2016, UNKNOWN, OTHER |
| availability_zone | no | string | The storage availability zone assigned to the volume. Valid values: AUTO, ZONE_1, ZONE_2, or ZONE_3. This only applies to HDD volumes. Leave blank or set to AUTO when provisioning SSD volumes. |

After retrieving a volume, either by getting it by id, or as a create response object, you can change its properties and call the `update_volume` method:

```
volume = client.update_volume(
            datacenter_id='existing_datacenter_id',
            volume_id='existing_volume_id',
            size=6,
            name='new_name')
```

---

#### Delete a Volume

Deletes the specified volume. This will result in the volume being removed from your data center. Use this with caution.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |

After retrieving a volume, either by getting it by id, or as a create response object, you can call the `delete_volume` method directly on the object:

```
volume = client.delete_volume(
            datacenter_id='existing_datacenter_id',
            volume_id='deleting_volume_id')
```

---

#### Create a Volume Snapshot

Creates a snapshot of a volume within the virtual data center. You can use a snapshot to create a new storage volume or to restore a storage volume.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |
| name | no | string | The name of the snapshot. |
| description | no | string | The description of the snapshot. |

After retrieving a volume, either by getting it by id, or as a create response object, you can call the `create_snapshot` method directly on the object:

```
snapshot = client.create_snapshot(
            datacenter_id='existing_datacenter_id',
            volume_id='existing_volume_id',
            name='new_snapshot_name',
            description='new_snapshot_description')
```

---

#### Restore a Volume Snapshot

This will restore a snapshot onto a volume. A snapshot is created as just another image that can be used to create new volumes or to restore an existing volume.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |
| snapshot_id | **yes** | string |  The ID of the snapshot. |

After retrieving a volume, either by getting it by id, or as a create response object, you can call the `restore_snapshot` method directly on the object:

```
response = client.restore_snapshot(
            datacenter_id='existing_datacenter_id',
            volume_id='existing_volume_id',
            snapshot_id='existing_snapshot_id')
```

---

### Snapshots

#### List Snapshots

You can retrieve a list of all available snapshots.

There are no request parameters to supply.

```
snapshots = client.list_snapshots()
```

---

#### Get a Snapshot

Retrieves the attributes of a specific snapshot.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| snapshot_id | **yes** | string | The ID of the snapshot. |

```
snapshot = client.get_snapshot(
			snapshot_id='existing_snapshot_id')
```

---

#### Update a Snapshot

Perform updates to attributes of a snapshot.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| snapshot_id | **yes** | string | The ID of the snapshot. |
| name | no | string | The name of the snapshot. |
| description | no | string | The description of the snapshot. |
| licence_type | no | string | The snapshot's licence type: LINUX, WINDOWS, WINDOWS2016, or OTHER. |
| cpu_hot_plug | no | bool | This volume is capable of CPU hot plug (no reboot required) |
| cpu_hot_unplug | no | bool | This volume is capable of CPU hot unplug (no reboot required) |
| ram_hot_plug | no | bool |  This volume is capable of memory hot plug (no reboot required) |
| ram_hot_unplug | no | bool | This volume is capable of memory hot unplug (no reboot required) |
| nic_hot_plug | no | bool | This volume is capable of NIC hot plug (no reboot required) |
| nic_hot_unplug | no | bool | This volume is capable of NIC hot unplug (no reboot required) |
| disc_virtio_hot_plug | no | bool | This volume is capable of VirtIO drive hot plug (no reboot required) |
| disc_virtio_hot_unplug | no | bool | This volume is capable of VirtIO drive hot unplug (no reboot required) |
| disc_scsi_hot_plug | no | bool | This volume is capable of SCSI drive hot plug (no reboot required) |
| disc_scsi_hot_unplug | no | bool | This volume is capable of SCSI drive hot unplug (no reboot required) |

After retrieving a snapshot, either by getting it by id, or as a create response object, you can change its properties and call the `update_snapshot` method:

```
snapshot = client.update_snapshot(
            snapshot_id='existing_snapshot_id',
            name='new_name',
            description='new_description')
```

---

#### Delete a Snapshot

Deletes the specified snapshot.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| snapshot_id | **yes** | string | The ID of the snapshot. |

After retrieving a snapshot, either by getting it by id, or as a create response object, you can call the `delete_snapshot` method directly on the object:

```
snapshot = client.delete_snapshot(snapshot_id='deleting_snapshot_id')
```

---

### Load Balancers

#### List Load Balancers

Retrieve a list of load balancers within the data center.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |

```
loadbalancers = client.list_loadbalancers(
            	 datacenter_id='existing_datacenter_id')
```

---

#### Get a Load Balancer

Retrieves the attributes of a given load balancer.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |

```
loadbalancer = client.get_loadbalancer(
            datacenter_id='existing_datacenter_id',
            loadbalancer_id='existing_loadbalancer_id')
```

---

#### Create a Load Balancer

Creates a load balancer within the virtual data center. Load balancers can be used for public or private IP traffic.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | **yes** | string | The name of the load balancer. |
| ip | no | string | IPv4 address of the load balancer. All attached NICs will inherit this IP. |
| dhcp | no | bool | Indicates if the load balancer will reserve an IP using DHCP. |
| balancednics | no | string collection | List of NICs taking part in load-balancing. All balanced NICs inherit the IP of the load balancer. |

```
i = LoadBalancer(
    name='name',
    dhcp=True)

self.loadbalancer = client.create_loadbalancer(
            datacenter_id='existing_datacenter_id',
            loadbalancer=i
        )
```

---

#### Update a Load Balancer

Perform updates to attributes of a load balancer.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | no | string | The name of the load balancer. |
| ip | no | string | The IP of the load balancer. |
| dhcp | no | bool | Indicates if the load balancer will reserve an IP using DHCP. |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can change it's properties and call the `update_loadbalancer` method:

```
loadbalancer = client.update_loadbalancer(
            datacenter_id='datacenter_id',
            loadbalancer_id='loadbalancer_id',
            name="updated_name")
```

---

#### Delete a Load Balancer

Deletes the specified load balancer.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| load_balancer_id | **yes** | string | The ID of the load balancer. |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `delete_loadbalancer` method directly on the object:

```
loadbalancer = client.delete_loadbalancer(
            datacenter_id='existing_datacenter_id',
            loadbalancer_id='deleting_loadbalancer_id')
```

---

#### List Load Balanced NICs

This will retrieve a list of NICs associated with the load balancer.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `get_loadbalancer_members` method directly on the object:

```
balanced_nics = client.get_loadbalancer_members(
            datacenter_id='existing_datacenter_id',
            loadbalancer_id='existing_loadbalancer_id')
```

---

#### Get a Load Balanced NIC

Retrieves the attributes of a given load balanced NIC.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |
| nic_id | **yes** | string | The ID of the NIC. |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `get_loadbalanced_nic` method directly on the object:

```
balanced_nic = client.get_loadbalanced_nic(
            datacenter_id='existing_datacenter_id',
            loadbalancer_id='existing_loadbalancer_id',
            nic_id='existing_nic_id')
```

---

#### Associate NIC to a Load Balancer

This will associate a NIC to a load balancer, enabling the NIC to participate in load-balancing.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |
| nic_id | **yes** | string | The ID of the NIC. |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `add_loadbalanced_nics` method directly on the object:

```
associated_nic = client.add_loadbalanced_nics(
             datacenter_id='existing_datacenter_id',
             loadbalancer_id='existing_loadbalancer_id',
             nic_id='existing_nic_id')
```

---

#### Remove a NIC Association

Removes the association of a NIC with a load balancer.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |
| nic_id | **yes** | string | The ID of the load balancer. |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `remove_loadbalanced_nic` method directly on the object:

```
remove_nic = client.remove_loadbalanced_nic(
             datacenter_id='existig_datacenter_id',
             loadbalancer_id='existing_loadbalancer_id',
             nic_id='removal_nic_id')
```

---

### Firewall Rules

#### List Firewall Rules

Retrieves a list of firewall rules associated with a particular NIC.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |

```
fwrules = client.get_firewall_rules(
             datacenter_id='existing_datacenter_id',
             server_id='existing_server_id',
             nic_id='nic_id')
```

---

#### Get a Firewall Rule

Retrieves the attributes of a given firewall rule.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| firewall_rule_id | **yes** | string | The ID of the firewall rule. |

```
fwrule = client.get_firewall_rule(
             datacenter_id='existing_datacenter_id',
             loadbalancer_id='existing_loadbalancer_id',
             nic_id='existing_nic_id',
             firewall_rule_id='existing_firewall_rule_id')
```

---

#### Create a Firewall Rule

This will add a firewall rule to the NIC.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| name | no | string | The name of the firewall rule. |
| protocol | **yes** | string | The protocol for the rule: TCP, UDP, ICMP, ANY. |
| source_mac | no | string | Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. A *null* value allows all source MAC address. |
| source_ip | no | string | Only traffic originating from the respective IPv4 address is allowed. A *null* value allows all source IPs. |
| target_ip | no | string | In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed. A *null* value allows all target IPs. |
| port_range_start | no | string | Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave `port_range_start` and `port_range_end` value as *null* to allow all ports. |
| port_range_end | no | string | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave `port_range_start` and `port_range_end` value as *null* to allow all ports. |
| icmp_type | no | string | Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. A *null* value allows all types. |
| icmp_code | no | string | Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. A *null* value allows all codes. |

```
i = FirewallRule(
    name='SSH',
    protocol='TCP',
    source_mac='01:23:45:67:89:00',
    port_range_start=22,
    port_range_end=22,
    icmp_type=None,
    icmp_code=None
    )

self.fwrule = client.create_firewall_rule(
            datacenter_id='datacenter_id',
            loadbalancer_id='loadbalancer_id',
            nic_id='nic_id',
            firewall_rule=i)
```

---

#### Update a Firewall Rule

Perform updates to attributes of a firewall rule.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| firewall_rule_id | **yes** | string | The ID of the firewall rule. |
| name | no | string | The name of the firewall rule. |
| source_mac | no | string | Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. A *null* value allows all source MAC address. |
| source_ip | no | string | Only traffic originating from the respective IPv4 address is allowed. A *null* value allows all source IPs. |
| target_ip | no | string | In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed. A *null* value allows all target IPs. |
| port_range_start | no | string | Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave `port_range_start` and `port_range_end` value as *null* to allow all ports. |
| port_range_end | no | string | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave `port_range_start` and `port_range_end` value as *null* to allow all ports. |
| icmp_type | no | string | Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. A *null* value allows all types. |
| icmp_code | no | string | Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. A *null* value allows all codes. |

After retrieving a firewall rule, either by getting it by id, or as a create response object, you can change its properties and call the `update_firewall_rule` method:

```
fwrule = client.update_firewall_rule(
            datacenter_id='datacenter_id',
            loadbalancer_id='loadbalancer_id',
            nic_id='nic_id',
            firewall_rule_id='firewall_rule_id',
            name="updated_name")
```

---

#### Delete a Firewall Rule

Removes the specific firewall rule.

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| firewall_rule_id | **yes** | string | The ID of the firewall rule. |

After retrieving a firewall rule, either by getting it by id, or as a create response object, you can call the `delete_firewall_rule` method directly on the object:

```
fwrule = client.delete_firewall_rule(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            nic_id='existing_nic_id',
            firewall_rule_id='deleting_firewall_rule_id')
```

---

### Images

#### List Images

Retrieve a list of images.

```
images = client.list_images()
```

---

#### Get an Image

Retrieves the attributes of a specific image.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| image_id | **yes** | string | The ID of the image. |

```
image = client.get_image('existing_image_id')
```

---

#### Update an Image

Updates the attributes of a specific user created image. You cannot update the properties of a public image supplied by ProfitBricks.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| image_id | **yes** | string | The ID of the image. |
| name | no | string | The name of the image. |
| description | no | string | The description of the image. |
| licence_type | no | string | The snapshot's licence type: LINUX, WINDOWS, WINDOWS2016, or OTHER. |
| cpu_hot_plug | no | bool | This volume is capable of CPU hot plug (no reboot required) |
| cpu_hot_unplug | no | bool | This volume is capable of CPU hot unplug (no reboot required) |
| ram_hot_plug | no | bool |  This volume is capable of memory hot plug (no reboot required) |
| ram_hot_unplug | no | bool | This volume is capable of memory hot unplug (no reboot required) |
| nic_hot_plug | no | bool | This volume is capable of NIC hot plug (no reboot required) |
| nic_hot_unplug | no | bool | This volume is capable of NIC hot unplug (no reboot required) |
| disc_virtio_hot_plug | no | bool | This volume is capable of VirtIO drive hot plug (no reboot required) |
| disc_virtio_hot_unplug | no | bool | This volume is capable of VirtIO drive hot unplug (no reboot required) |
| disc_scsi_hot_plug | no | bool | This volume is capable of SCSI drive hot plug (no reboot required) |
| disc_scsi_hot_unplug | no | bool | This volume is capable of SCSI drive hot unplug (no reboot required) |

You can change an image's properties by calling the `update_image` method:

```
image = client.update_image(
            image_id='existing_image_id',
            name='new_name',
            description='new_description',
            licence_type='new_licence_type")
```

---

#### Delete an Image

Deletes a specific user created image. You cannot delete public images supplied by ProfitBricks.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| image_id | **yes** | string | The ID of the image. |

```
image = client.delete_image('existing_image_id')
```

---

### Network Interfaces (NICs)

#### List NICs

Retrieve a list of LANs within the virtual data center.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

```
nics = client.list_nics(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server-id')
```

---

#### Get a NIC

Retrieves the attributes of a given NIC.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |

```
nic = client.get_nic(datacenter_id='existing_datacenter_id',
                                  server_id='existing_server_id',
                                  nic_id='existing_nic_id')
```

---

#### Create a NIC

Adds a NIC to the target server.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string| The ID of the server. |
| name | no | string | The name of the NIC. |
| ips | no | string collection | IPs assigned to the NIC. This can be a collection. |
| dhcp | no | bool | Set to FALSE if you wish to disable DHCP on the NIC. Default: TRUE. |
| lan | **yes** | int | The LAN ID the NIC will sit on. If the LAN ID does not exist it will be created. |
| nat | no | bool | Indicates the private IP address has outbound access to the public internet. |
| firewall_active | no | bool | Once you add a firewall rule this will reflect a true value. |
| firewall_rules | no | string collection | A list of firewall rules associated to the NIC represented as a collection. |

```
i = NIC(
    name='Python SDK Test',
    dhcp=True,
    lan=1,
    nat=False)

nic2 = client.create_nic(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            nic=i)
```

---

#### Update a NIC

You can update -- in full or partially -- various attributes on the NIC; however, some restrictions are in place:

The primary address of a NIC connected to a load balancer can only be changed by changing the IP of the load balancer. You can also add additional reserved, public IPs to the NIC.

The user can specify and assign private IPs manually. Valid IP addresses for private networks are 10.0.0.0/8, 172.16.0.0/12 or 192.168.0.0/16.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string| The ID of the server. |
| nic_id | **yes** | string| The ID of the NIC. |
| name | no | string | The name of the NIC. |
| ips | no | string collection | IPs assigned to the NIC represented as a collection. |
| dhcp | no | bool | Boolean value that indicates if the NIC is using DHCP or not. |
| lan | no | int | The LAN ID the NIC sits on. |
| nat | no | bool | Indicates the private IP address has outbound access to the public internet. |

After retrieving a NIC, either by getting it by id, or as a create response object, you can call the `update_nic` method directly on the object:

```
nic = client.update_nic(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            nic_id='updating_nic_id',
            name='new_name')
```

---

#### Delete a NIC

Deletes the specified NIC.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string| The ID of the server. |
| nic_id | **yes** | string| The ID of the NIC. |

After retrieving a NIC, either by getting it by id, or as a create response object, you can call the `delete_nic` method directly on the object:

```
nic = client.delete_nic(
            datacenter_id='existing_datacenter_id',
            server_id='existing_server_id',
            nic_id='deleting_nic_id')
```

---

### IP Blocks

The IP block operations assist with managing reserved /static public IP addresses.

#### List IP Blocks

Retrieve a list of available IP blocks.

```
ipblocks = client.list_ipblocks()
```

---

#### Get an IP Block

Retrieves the attributes of a specific IP block.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| ipblock_id | **yes** | string | The ID of the IP block. |

```
ipblock = client.get_ipblock('existing_ipblock_id')
```

---

#### Create an IP Block

Creates an IP block. IP blocks are attached to a location, so you must specify a valid `location` along with a `size` parameter indicating the number of IP addresses you want to reserve in the IP block. Servers or other resources using an IP address from an IP block must be in the same `location`.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| location | **yes** | string | This must be one of the locations: us/las, de/fra, de/fkb. |
| size | **yes** | int | The size of the IP block you want. |
| name | no | string | A descriptive name for the IP block |

The following table outlines the locations currently supported:

| Value| Country | City |
|---|---|---|
| us/las | United States | Las Vegas |
| de/fra | Germany | Frankfurt |
| de/fkb | Germany | Karlsruhe |

To create an IP block, establish the parameters and then call `reserve_ipblock`.

```
i = IPBlock(
    name='new_ipblock_name',
    size=4,
    location='de/fkb'
    )

ipblock = client.reserve_ipblock(i)
```

---

#### Delete an IP Block

Deletes the specified IP Block.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| ipblock_id | **yes** | string | The ID of the IP block. |

After retrieving an IP block, either by getting it by id, or as a create response object, you can call the `delete_ipblock` method directly on the object:

```
client.delete_ipblock('deleting_ipblock_id')
```
---

### Requests

Each call to the ProfitBricks Cloud API is assigned a request ID. These operations can be used to get information about the requests that have been submitted and their current status.

#### List Requests

Retrieve a list of requests.

```
requests = client.list_requests()
```

---

#### Get a Request

Retrieves the attributes of a specific request. This operation shares the same `get_request` method used for getting request status, however the response it determined by the boolean value you pass for *status*. To get details about the request itself, you want to pass a *status* of *False*.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| request_id | **yes** | string | The ID of the request. |
| status | **yes** | bool | Set to *False* to have the request details returned. |

```
request = client.get_request(request_id='request-id', status=False)
```

---

#### Get a Request Status

Retrieves the status of a request. This operation shares the same `get_request` method used for getting the details of a request, however the response it determined by the boolean value you pass for *status*. To get the request status, you want to pass a *status* of *True*.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| request_id | **yes** | string | The ID of the request. |
| status | **yes** | boolean | Set to *True* to have the status of the request returned. |

```
request = client.get_request(request_id='request-id', status=True)
```

---

### LANs

#### List LANs

Retrieve a list of LANs within the virtual data center.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |

```
lans = client.list_lans(datacenter_id='existing_datacenter_id')
```

---

#### Create a LAN

Creates a LAN within a virtual data center.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | no | string | The name of your LAN. |
| public | **Yes** | bool | Boolean indicating if the LAN faces the public Internet or not. |
| nics | no | string collection | A collection of NICs associated with the LAN. |

```
lan = client.create_lan(
            datacenter_id='existing_datacenter_id',
            name='new_lan_name',
            public=False)
```

---

#### Get a LAN

Retrieves the attributes of a given LAN.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | int | The ID of the LAN. |

```
lan = client.get_lan(datacenter_id='existing_datacenter_id', lan_id='existing_lan_id')
```

---

#### Update a LAN

Perform updates to attributes of a LAN.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | int | The ID of the LAN. |
| name | no | string | A descriptive name for the LAN. |
| public | no | bool | Boolean indicating if the LAN faces the public Internet or not. |

After retrieving a LAN, either by getting it by id, or as a create response object, you can change its properties and call the `update_lan` method:

```
lan = client.update_lan(
            datacenter_id='existing_datacenter_id',
            lan_id=existing_lan_id,
            name='new_lan_name',
            public=False)
```

---

#### Delete a LAN

Deletes the specified LAN.

The following table describes the request arguments:

| Name| Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | string | The ID of the LAN. |

After retrieving a LAN, either by getting it by id, or as a create response object, you can call the `delete_lan` method directly on the object:

```
lan = client.delete_lan(datacenter_id='datacenter_id', lan_id='lan_id')
```

## Examples

Here are a few examples on how to use the module. In this first one we pull a list of our virtual data centers.

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='username', password='password')

    datacenters = client.list_datacenters()

And in this one we reserve an IP block:

    from profitbricks.client import ProfitBricksService, IPBlock

    client = ProfitBricksService(
        username='username', password='password')

    i = IPBlock(location='de/fra', size=5)

    ipblock = client.reserve_ipblock(i)

Some object creation operations support both simple and complex requests, such as a server which can be created simply by doing this:

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

Or if you want to create a server with some volumes and NICs you would do:

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
        image='IMAGE/SNAPSHOT-ID',
        bus='VIRTIO'
        ssh_keys=['ssh-rsa AAAAB3NzaC1yc2EAAAADAQ...'],
        image_password='s3cr3tpass0rd',
        availability_zone='ZONE_3'
        )

    volume2 = Volume(
        name='volume2',
        size=56,
        image='IMAGE/SNAPSHOT-ID',
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

## Support

You can find additional examples in the repository `examples` directory. If you find any issues, please let us know via the [DevOps Central community](https://devops.profitbricks.com) or [GitHub's issue system](https://github.com/profitbricks/profitbricks-sdk-python/issues) and we'll check it out.

## Testing

You can find a full list of tests inside the `tests` folder. To run all available tests:

    export PROFITBRICKS_USERNAME=username
    export PROFITBRICKS_PASSWORD=password
    
    pip install -r requirements.txt
    python -m unittest discover tests

To run a single test:

    python -m unittest discover tests test_datacenter.py

## Contributing

1. Fork it ( https://github.com/profitbricks/profitbricks-sdk-python/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
