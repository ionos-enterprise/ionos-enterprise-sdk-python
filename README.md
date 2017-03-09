The ProfitBricks Client Library for Python provides you with access to the ProfitBricks Cloud API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python.

This guide will walk you through getting setup with the library and performing various actions against the API.

## Table of Contents

* [Getting Started](#getting-started)
  * [Installation](#installation)
  * [Authentication](#authentication)
  * [Error Handling](#Error Handling)
* [Operations](#operations)
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
    * [Retrieve an Attached CD-ROM](retrieve-an-attached-cd-rom)
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
* [Support](#Support)
  * [Contributing](#contributing)

## Concepts

The Python Client Library wraps version 3 of the ProfitBricks Cloud API. All API operations are performed over SSL and authenticated using your ProfitBricks portal credentials. The API can be accessed within an instance running in ProfitBricks or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response.

## Getting Started

Before you begin you will need to have [signed-up](https://www.profitbricks.com/signup) for a ProfitBricks account. The credentials you setup during sign-up will be used to authenticate against the API.

### Installation

The Python Client Library is available on [PyPi](https://pypi.python.org/pypi/profitbricks). You can install the latest stable version using `pip`:

    pip install profitbricks

Done!

### Authenticating

Connecting to ProfitBricks is handled by first setting up your authentication.

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='username', password='password')

You can now use `client` for any future request.

### Error Handling

The Python Client Library will raise custom exceptions when the Cloud API returns an error. There are five exception types:

| EXCEPTION | HTTP CODE | DESCRIPTION |
|---|---|---|
| PBNotAuthorizedError | 401 | The supplied user credentials are invalid. |
| PBNotFoundError | 404 | The requested resource cannot be found. |
| PBValidationError | 422 | The request body includes invalid JSON. |
| PBRateLimitExceededError | 429 | The Cloud API rate limit has been exceeded. |
| PBError | Other | A generic exception for all other status codes. |


## Operations
`client` is the `ProfitBricksService` class imported `from profitbricks.client import ProfitBricksService`

### Data Centers

Virtual Data Centers (VDCs) are the foundation of the ProfitBricks platform. VDCs act as logical containers for all other objects you will be creating, e.g., servers. You can provision as many data centers as you want. Data centers have their own private network and are logically segmented from each other to create isolation.

#### List Data Centers

```
datacenters = client.list_datacenters()
```
---

#### Retrieve a Data Center

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |

```
   datacenter = client.get_datacenter(
            datacenter_id='datacenter_id')
```
---

#### Create a Data Center

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| name | string | The name of the data center. | Yes |
| location | string | The physical location where the data center will be created. This will be where all of your servers live. | Yes |
| description | string | A description for the data center, e.g. staging, production. | No|

The following table outlines the locations currently supported:

| VALUE| COUNTRY | CITY |
|---|---|---|
| us/las | United States | Las Vegas |
| de/fra | Germany | Frankfurt |
| de/fkb | Germany | Karlsruhe |

```
i = Datacenter(
    name='name',
    description='My New Datacenter',
    location='de/fkb'
    )
response = client.create_datacenter(datacenter=i)
```

*NOTES*:
- The value for `name` cannot contain the following characters: (@, /, , |, ‘’, ‘).
- You cannot change a data center's `location` once it has been provisioned.

---

#### Update a Data Center

After retrieving a data center, either by getting it by id, or as a create response object, you can change it's properties and call the `update` method:

```
datacenter = client.update_datacenter(
	datacenter_id='datacenter_id',
	name='name'
        description='description')
```

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
| --- | --- | --- | --- |
| name | string | The new name of the data center. | No|
| description | string | The new description of the data center. | No |

---

#### Delete a Data Center

This will remove all objects within the data center and remove the data center object itself.

**NOTE**: This is a highly destructive operation which should be used with extreme caution.

```
response = client.delete_datacenter(
           datacenter_id='datacenter_id'])
```

---

### Locations

Locations represent regions where you can provision your Virtual Data Centers.

#### List Locations

```
locations = client.list_locations()
```

---

#### Get a Location

Retrieves the attributes of a given location.

The following table describes the request arguments:

| NAME | TYPE | DESCRIPTION | REQUIRED |
| --- | --- | --- | --- |
| location_id | string | The resource's unique identifier consisting of country/city. | Yes|

```
self.client.get_location('us/las')
```

---

### Servers

#### List Servers

You can retrieve a list of all servers within a data center.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |

```
servers = client.list_servers(datacenter_id=datacenter_id)
```

---

#### Retrieve a Server

Returns information about a server such as its configuration, provisioning status, etc.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| server-id | string | 	The unique ID of the server. | Yes |

```
server = client.get_server(
            datacenter_id=s'datacenter_id',
            server_id='server-id'
        )
```

---

#### Create a Server

Creates a server within an existing data center. You can configure additional properties such as specifying a boot volume and connecting the server to an existing LAN.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| name | string | The hostname of the server. | Yes |
| cores | int | The total number of cores for the server. | Yes |
| ram | int | The amount of memory for the server in MB, e.g. 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set ramHotPlug to TRUE then you must use a minimum of 1024 MB. | Yes |
| availabilityZone | string |The availability zone in which the server should exist. | No |
| licenceType | string | Sets the OS type of the server. If undefined the OS type will be inherited from the boot image or boot volume. | No* |
| boot_volume_id | string | Reference to a Volume used for booting. If not ‘null’ then bootCdrom has to be ‘null’. | No |
| boot_cdrom | string | Reference to a CD-ROM used for booting. If not 'null' then bootVolume has to be 'null'. | No |
| attach_volumes | collection | A collection of volume IDs that you want to connect to the server. | No |
| create_volumes | collection | A collection of volume objects that you want to create and attach to the server.| No |
| nics | collection | A collection of NICs you wish to create at the time the server is provisioned. | No |
| cpu_family | string | Sets the CPU type. "AMD_OPTERON" or "INTEL_XEON". Defaults to "AMD_OPTERON". | No |

The following table outlines the various licence types you can define:

| LICENCE TYPE | COMMENT |
|---|---|
| WINDOWS | You must specify this if you are using your own, custom Windows image due to Microsoft's licensing terms. |
| LINUX ||
| UNKNOWN | If you are using an image uploaded to your account your OS Type will inherit as UNKNOWN. |

The following table outlines the availability zones currently supported:

| LICENCE TYPE | COMMENT |
|---|---|
| AUTO | Automatically Selected Zone |
| ZONE_1 | Fire Zone 1 |
| ZONE_2 | Fire Zone 2 |

```
i = Server(
    name='name',
    cores=1,
    ram=1,
    description='My New Datacenter',
    location='de/fkb'
    )
server = client.create_server(
            datacenter_id='datacenter_id',
            server=i)
```

**NOTE**: When creating a volume, you must specify either the `licence_type` or an `image`.

---

#### Update a Server

Perform updates to attributes of a server.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |
| name | string | The name of the server. | No |
| cores | int | The number of cores for the server. | No |
| ram | int | The amount of memory in the server. | No |
| availabilityZone | string | The new availability zone for the server. | No |
| licenceType | string | The licence type for the server. | No |
| boot_volume | string | Reference to a Volume used for booting. If not ‘null’ then bootCdrom has to be ‘null’ | No |
| bootCdrom | string | Reference to a CD-ROM used for booting. If not 'null' then bootVolume has to be 'null'. | No |

After retrieving a server, either by getting it by id, or as a create response object, you can change it's properties and call the `update` method:

```
server = client.update_server(
            datacenter_id='datacenter_id',
            server_id'server-id',
            name='name')
```

---

#### Delete a Server

This will remove a server from a data center. NOTE: This will not automatically remove the storage volume(s) attached to a server. A separate API call is required to perform that action.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `delete` method directly on the object:

```
response = client.delete_server(
            datacenter_id='datacenter_id',
            server_id='server-id'
        )
```

---

#### List Attached Volumes

Retrieves a list of volumes attached to the server.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| server-id | string | 	The unique ID of the server. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `get_volumes` method directly on the object:

```
servers = client.get_attached_volumes(
          datacenter_id='datacenter_id',
          server_id='server-id')
```

---

#### Attach a Volume

This will attach a pre-existing storage volume to the server.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |
| volume_id | string | The unique ID of a storage volume. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `attach_volume` method directly on the object:

```
 volume = client.attach_volume(
            datacenter_id='datacenter_id',
            server_id='server-id',
            volume_id='volume_id')
```

---

#### Retrieve an Attached Volume

This will retrieve the properties of an attached volume.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |
| volume-id | string | The unique ID of the attached volume. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `get_attached_volume` method directly on the object:

```
server = client.get_attached_volume(
            datacenter_id='datacenter_id',
            server_id='server-id',
            volume_id='volume_id')
```

---

#### Detach a Volume

This will detach the volume from the server. Depending on the volume "hot_unplug" settings, this may result in the server being rebooted.

This will NOT delete the volume from your data center. You will need to make a separate request to delete a volume.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |
| volume-id | string | The unique ID of the attached volume. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `detach_volume` method directly on the object:

```
volume = client.detach_volume(
           datacenter_id='datacenter_id',
           server_id='server-id',
           volume_id='volume_id')
```

---

#### List Attached CD-ROMs

Retrieves a list of CD-ROMs attached to the server.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `get_cdroms` method directly on the object:

```
cdroms = client.get_attached_cdroms(
            datacenter_id='datacenter_id',
            server_id='server-id')
```

---

#### Attach a CD-ROM

You can attach a CD-ROM to an existing server.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |
| cdrom_id | string | The unique ID of a CD-ROM. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `attach_cdrom` method directly on the object:

```
attached_cdrom = client.attach_cdrom(
            datacenter_id='datacenter_id',
            server_id='server-id',
            cdrom_id='cdrom-image-id')
```

---

#### Retrieve an Attached CD-ROM

You can retrieve a specific CD-ROM attached to the server.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |
| cdrom-id | string | The unique ID of the attached CD-ROM. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `get_attached_cdrom` method directly on the object:

```
attached_cdrom = client.attach_cdrom(
            datacenter_id='datacenter_id',
            server_id='server-id',
            cdrom_id='cdrom-id')
```

---

#### Detach a CD-ROM

This will detach a CD-ROM from the server.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |
| cdrom-id | string | The unique ID of the attached CD-ROM. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `detach_cdrom` method directly on the object:

```
detached_cd = client.detach_cdrom(
            datacenter_id='datacenter_id',
            server_id='server-id',
            cdrom_id='cdrom-id')
```

---

#### Reboot a Server

This will force a hard reboot of the server. Do not use this method if you want to gracefully reboot the machine. This is the equivalent of powering off the machine and turning it back on.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `reboot` method directly on the object:

```
server = client.reboot_server(
            datacenter_id='datacenter_id',
            server_id='server-id')
```

---

#### Start a Server

This will start a server. If the server's public IP was deallocated then a new IP will be assigned.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `start` method directly on the object:

```
server = client.start_server(
           datacenter_id='datacenter_id',
           server_id='server-id')
```

---

#### Stop a Server

This will stop a server. The machine will be forcefully powered off, billing will cease, and the public IP, if one is allocated, will be deallocated.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |

After retrieving a server, either by getting it by id, or as a create response object, you can call the `stop` method directly on the object:

```
server = client.stop_server(
           datacenter_id='datacenter_id',
           server_id='server-id')
```

---

### Volumes

#### List Volumes

Retrieve a list of volumes within the data center. If you want to retrieve a list of volumes attached to a server please see the [Servers](#servers) section for examples on how to do so.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |

```
volumes = client.list_volumes(
            datacenter_id='datacenter_id')
```

---

#### Get a Volume

Retrieves the attributes of a given volume.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| volume-id | string | 	The unique ID of the volume. | Yes |

```
volume = client.get_volume(
            datacenter_id='datacenter_id',
            volume_id='volume-id')
```

---

#### Create a Volume

Creates a volume within the data center. This will NOT attach the volume to a server. Please see the [Servers](#servers) section for details on how to attach storage volumes.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| name | string | The name of the volume. | No |
| size | int | The size of the volume in GB. | Yes |
| bus | string | The bus type of the volume (VIRTIO or IDE). Default: VIRTIO. | No |
| image | string | The image or snapshot ID. | Yes* |
| type | string | The volume type, HDD or SSD. | Yes |
| licenceType | string | The licence type of the volume. Options: LINUX, WINDOWS, UNKNOWN, OTHER | Yes* |
| imagePassword | string | One-time password is set on the Image for the appropriate account. This field may only be set in creation requests. When reading, it always returns null. Password has to contain 8-50 characters. Only these characters are allowed: [abcdefghjkmnpqrstuvxABCDEFGHJKLMNPQRSTUVX23456789] | Yes* |
| sshKeys | string | SSH keys to allow access to the volume via SSH | Yes* |
| availabilityZone | string | The storage availability zone assigned to the volume. Valid values: AUTO, ZONE_1, ZONE_2, or ZONE_3. This only applies to HDD volumes. Leave blank or set to AUTO when provisioning SSD volumes. | No |

*You will need to provide either the `image` or the `licenceType` parameters. `licenceType` is required, but if `image` is supplied, it is already set and cannot be changed. Similarly either the `imagePassword` or `sshKeys` parameters need to be supplied when creating a volume. We recommend setting a valid value for `imagePassword` even when using `sshKeys` so that it is possible to authenticate using the remote console feature of the DCD.

```
i = Volume(
    name='name',
    size=2,
    bus='VIRTIO',
    type='HDD',
    licence_type='LINUX',
    availabilityZone='ZONE_3')
volume = client.create_volume(
            datacenter_id='datacenter_id',
            volume=i))
```

---

#### Update a Volume

You can update -- in full or partially -- various attributes on the volume; however, some restrictions are in place:

You can increase the size of an existing storage volume. You cannot reduce the size of an existing storage volume. The volume size will be increased without reboot if the hot plug settings have been set to true. The additional capacity is not added to any partition therefore you will need to partition it afterwards. Once you have increased the volume size you cannot decrease the volume size.

Since an existing volume is being modified , none of the request parameters are specifically required as long as the changes being made satisfy the requirements for creating a volume.

After retrieving a volume, either by getting it by id, or as a create response object, you can change it's properties and call the `update` method:

```
volume = client.update_volume(
            datacenter_id='datacenter_id',
            volume_id='volume_id',
            size=6,
            name='name')
```

---

#### Delete a Volume

Deletes the specified volume. This will result in the volume being removed from your data center. Use this with caution.

After retrieving a volume, either by getting it by id, or as a create response object, you can call the `delete` method directly on the object:

```
volume = client.delete_volume(
            datacenter_id='datacenter_id',
            volume_id='volume_id')
```

---

#### Create a Volume Snapshot

Creates a snapshot of a volume within the data center. You can use a snapshot to create a new storage volume or to restore a storage volume.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| name | string | The name of the snapshot. ||
| description | string | The description of the snapshot. ||

After retrieving a volume, either by getting it by id, or as a create response object, you can call the `create_snapshot` method directly on the object:

```
snapshot = client.create_snapshot(
            datacenter_id='datacenter_id',
            volume_id='volume_id',
            name='name',
            description='description')
```

---

#### Restore a Volume Snapshot

This will restore a snapshot onto a volume. A snapshot is created as just another image that can be used to create new volumes or to restore an existing volume.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| snapshotId | string |  The ID of the snapshot. | Yes |

After retrieving a volume, either by getting it by id, or as a create response object, you can call the `restore_snapshot` method directly on the object:

```
 response = client.restore_snapshot(
            datacenter_id='datacenter_id',
            volume_id='volume_id',
            snapshot_id='snapshot_id')
```

---

### Snapshots

#### List Snapshots

You can retrieve a list of all snapshots.

```
snapshots = client.list_snapshots()
```

---

#### Get a Snapshot

Retrieves the attributes of a specific snapshot.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| snapshotId | string |  The ID of the snapshot. | Yes |

```
snapshot = client.get_snapshot(snapshot_id='snapshotId')
```

---

#### Update a Snapshot

Perform updates to attributes of a snapshot.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| snapshotId | string |  The ID of the snapshot. | Yes |
| name | string |  The name of the snapshot. ||
| description | string | The description of the snapshot. ||
| cpuHotPlug | bool |  This volume is capable of CPU hot plug (no reboot required) ||
| cpuHotUnplug | bool |  	This volume is capable of CPU hot unplug (no reboot required) ||
| ramHotPlug | bool |  This volume is capable of memory hot plug (no reboot required) ||
| ramHotUnplug | bool |  	This volume is capable of memory hot unplug (no reboot required) ||
| nicHotPlug | bool | This volume is capable of NIC hot plug (no reboot required) ||
| nicHotUnplug | bool |  This volume is capable of NIC hot unplug (no reboot required) ||
| discVirtioHotPlug | bool |  This volume is capable of Virt-IO drive hot plug (no reboot required) ||
| discVirtioHotUnplug | bool |  This volume is capable of Virt-IO drive hot unplug (no reboot required) ||
| discScsiHotPlug | bool |  This volume is capable of SCSI drive hot plug (no reboot required) ||
| discScsiHotUnplug | bool |  This volume is capable of SCSI drive hot unplug (no reboot required) ||
| licencetype | string |  The snapshot's licence type: LINUX, WINDOWS, or UNKNOWN. ||

After retrieving a snapshot, either by getting it by id, or as a create response object, you can change it's properties and call the `update` method:

```
snapshot = client.update_snapshot(
            snapshot_id='snapshotId',
            name='name',
            description='description')
```

---

#### Delete a Snapshot

Deletes the specified snapshot.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| snapshotId | string |  The ID of the snapshot. | Yes |

After retrieving a snapshot, either by getting it by id, or as a create response object, you can call the `delete` method directly on the object:

```
snapshot = client.delete_snapshot(snapshot_id='snapshotId')
```

---

### Load Balancers

#### List Load Balancers

Retrieve a list of load balancers within the data center.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |

```
loadbalancers = client.list_loadbalancers(
            datacenter_id='datacenter_id')
```

---

#### Get a Load Balancer

Retrieves the attributes of a given load balancer.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| load_balancer_id | string | The unique ID of the load balancer. | Yes |

```
loadbalancer = client.get_loadbalancer(
            datacenter_id='datacenter_id',
            loadbalancer_id='load_balancer_id')
```

---

#### Create a Load Balancer

Creates a load balancer within the data center. Load balancers can be used for public or private IP traffic.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| name | string | The name of the load balancer. | Yes |
| ip | string | IPv4 address of the load balancer. All attached NICs will inherit this IP. | No |
| dhcp | bool | Indicates if the load balancer will reserve an IP using DHCP. | No |
| balancednics | string collection | List of NICs taking part in load-balancing. All balanced nics inherit the IP of the load balancer. | No |

```
i = LoadBalancer(
    name='name',
    dhcp=True)
self.loadbalancer = client.create_loadbalancer(
            datacenter_id='datacenter_id',
            loadbalancer=i
        )
```

---

#### Update a Load Balancer

Perform updates to attributes of a load balancer.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| name | string | The name of the load balancer. | No |
| ip | string | 	The IP of the load balancer. | No |
| dhcp | bool | Indicates if the load balancer will reserve an IP using DHCP. | No |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can change it's properties and call the `update` method:

```
loadbalancer = client.update_loadbalancer(
            datacenter_id='datacenter_id',
            loadbalancer_id='loadbalancer_id',
            name="updated name")
```

---

#### Delete a Load Balancer

Deletes the specified load balancer.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| load_balancer_id | string | The unique ID of the load balancer. | Yes |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `delete` method directly on the object:

```
loadbalancer = client.delete_loadbalancer(
            datacenter_id='datacenter_id',
            loadbalancer_id='loadbalancer_id')
```

---

#### List Load Balanced NICs

This will retrieve a list of NICs associated with the load balancer.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| load_balancer_id | string | The unique ID of the load balancer. | Yes |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `get_nics` method directly on the object:

```
 balanced_nics = client.get_loadbalancer_members(
            datacenter_id='datacenter_id',
            loadbalancer_id='loadbalancer_id')
```

---

#### Get a Load Balanced NIC

Retrieves the attributes of a given load balanced NIC.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| load_balancer_id | string | The unique ID of the load balancer. | Yes |
| nic_id | string | The unique ID of the load balancer. | Yes |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `get_nic` method directly on the object:

```
balanced_nic = client.get_loadbalanced_nic(
            datacenter_id='datacenter_id',
            loadbalancer_id='loadbalancer_id',
            nic_id='nic_id')
```

---

#### Associate NIC to a Load Balancer

This will associate a NIC to a Load Balancer, enabling the NIC to participate in load-balancing.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| load_balancer_id | string | The unique ID of the load balancer. | Yes |
| nic_id | string | The unique ID of the load balancer. | Yes |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `associate_nic` method directly on the object:

```
associated_nic = client.get_loadbalanced_nic(
             datacenter_id='datacenter_id',
             loadbalancer_id='loadbalancer_id',
             nic_id='nic_id')
```

---

#### Remove a NIC Association

Removes the association of a NIC with a load balancer.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| load_balancer_id | string | The unique ID of the load balancer. | Yes |
| nic_id | string | The unique ID of the load balancer. | Yes |

After retrieving a load balancer, either by getting it by id, or as a create response object, you can call the `remove_nic_association` method directly on the object:

```
remove_nic = client.remove_loadbalanced_nic(
             datacenter_id='datacenter_id',
             loadbalancer_id='loadbalancer_id',
             nic_id='nic_id')
```

---

### Firewall Rules

#### List Firewall Rules

Retrieves a list of firewall rules associated with a particular NIC.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server_id | string | The unique ID of the server. | Yes |
| nic_id | string | The unique ID of the NIC. | Yes |

```
fwrules = client.get_firewall_rules(
             datacenter_id='datacenter_id',
             loadbalancer_id='loadbalancer_id',
             nic_id='nic_id')
```

---

#### Get a Firewall Rule

Retrieves the attributes of a given firewall rule.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server_id | string | The unique ID of the server. | Yes |
| nic_id | string | The unique ID of the NIC. | Yes |
| firewall_rule_id | string | The unique ID of the firewall rule. | Yes |

```
fwrule = client.get_firewall_rule(
             datacenter_id='datacenter_id',
             loadbalancer_id='loadbalancer_id',
             nic_id='nic_id',
             firewall_rule_id='firewall_rule_id')
```

---

#### Create a Firewall Rule

This will add a firewall rule to the NIC.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| server_id | string | The unique ID of the server. | Yes |
| nic_id | string | The unique ID of the NIC. | Yes |
| name | string | The name of the Firewall Rule. ||
| protocol | string | The protocol for the rule: TCP, UDP, ICMP, ANY. | Yes |
| source_mac | string | Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. Value null allows all source MAC address. ||
| source_ip | string | Only traffic originating from the respective IPv4 address is allowed. Value null allows all source IPs. ||
| target_ip | string | In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed. Value null allows all target IPs. ||
| port_range_start | string | Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd value null to allow all ports. ||
| port_range_end | string | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd null to allow all ports. ||
| icmp_type | string | Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. Value null allows all types. ||
| icmp_code | string | Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. Value null allows all codes. ||

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

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| server_id | string | The unique ID of the server. | Yes |
| nic_id | string | The unique ID of the NIC. | Yes |
| firewall_rule_id | string | The unique ID of the firewall rule. | Yes |
| name | string | The name of the Firewall Rule. ||
| sourceMac | string | Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. Value null allows all source MAC address. ||
| sourceIp | string | Only traffic originating from the respective IPv4 address is allowed. Value null allows all source IPs. ||
| targetIp | string | In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed. Value null allows all target IPs. ||
| portRangeStart | string |	Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd value null to allow all ports. ||
| portRangeEnd | string | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave portRangeStart and portRangeEnd null to allow all ports. ||
| icmpType | string | Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. Value null allows all types. ||
| icmpCode | string | Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. Value null allows all codes. ||

After retrieving a firewall rule, either by getting it by id, or as a create response object, you can change its properties and call the `update` method:

```
fwrule = client.update_firewall_rule(
            datacenter_id='datacenter_id',
            loadbalancer_id='loadbalancer_id',
            nic_id='nic_id',
            firewall_rule_id='firewall_rule_id',
            name="updated name")
```

---

#### Delete a Firewall Rule

Removes the specific firewall rule.

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server_id | string | The unique ID of the server. | Yes |
| nic_id | string | The unique ID of the NIC. | Yes |
| firewall_rule_id | string | The unique ID of the firewall rule. | Yes |

After retrieving a firewall rule, either by getting it by id, or as a create response object, you can call the `delete` method directly on the object:

```
fwrule = client.delete_firewall_rule(
            datacenter_id='datacenter_id',
            server_id='server_id',
            nic_id='nic_id',
            firewall_rule_id='firewall_rule_id')
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

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| image-id | string | The unique ID of the image. | Yes |

```
image = client.get_image('image-id')
```

---

### Network Interfaces (NICs)

#### List NICs

Retrieve a list of LANs within the data center.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |

```
nics = client.list_nics(
            datacenter_id='datacenter_id',
            server_id='server-id')
```

---

#### Get a NIC

Retrieves the attributes of a given NIC.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server-id | string | The unique ID of the server. | Yes |
| nic-id | string | The unique ID of the NIC. | Yes |

```
nic = client.get_nic(datacenter_id='datacenter_id',
                                  server_id='server-id',
                                  nic_id='nic-id')
```

---

#### Create a NIC

Adds a NIC to the target server.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server_id | string| The unique ID of the server. | Yes |
| name | string | The name of the NIC. ||
| ips | string collection | IPs assigned to the NIC. This can be a collection. ||
| dhcp | bool | Set to FALSE if you wish to disable DHCP on the NIC. Default: TRUE. ||
| lan | int | The LAN ID the NIC will sit on. If the LAN ID does not exist it will be created. | Yes |
| nat | bool | Indicates the private IP address has outbound access to the public internet. ||
| firewallActive | bool | Once you add a firewall rule this will reflect a true value. ||
| firewallrules | string collection | A list of firewall rules associated to the NIC represented as a collection. ||

```
i = NIC(
    name='Python SDK Test',
    dhcp=True,
    lan=1,
    firewall_active=True,
    nat=False)
nic2 = client.create_nic(
            datacenter_id='datacenter_id',
            server_id='server-id',
            nic=i)
```

---

#### Update a NIC

You can update -- in full or partially -- various attributes on the NIC; however, some restrictions are in place:

The primary address of a NIC connected to a load balancer can only be changed by changing the IP of the load balancer. You can also add additional reserved, public IPs to the NIC.

The user can specify and assign private IPs manually. Valid IP addresses for private networks are 10.0.0.0/8, 172.16.0.0/12 or 192.168.0.0/16.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server_id | string| The unique ID of the server. | Yes |
| nic-id | string| The unique ID of the NIC. | Yes |
| name | string | The name of the NIC. ||
| ips | string collection | IPs assigned to the NIC represented as a collection. ||
| dhcp | bool | Boolean value that indicates if the NIC is using DHCP or not. ||
| lan | int | The LAN ID the NIC sits on. ||
| nat | bool | Indicates the private IP address has outbound access to the public internet. ||

After retrieving a NIC, either by getting it by id, or as a create response object, you can call the `update` method directly on the object:

```
nic = client.update_nic(
            datacenter_id='datacenter_id',
            server_id='server-id',
            nic_id='nic_id',
            name='name')
```

---

#### Delete a NIC

Deletes the specified NIC.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| server_id | string| The unique ID of the server. | Yes |
| nic-id | string| The unique ID of the NIC. | Yes |

After retrieving a NIC, either by getting it by id, or as a create response object, you can call the `delete` method directly on the object:

```
nic = client.delete_nic(
            datacenter_id='datacenter_id',
            server_id='server-id',
            nic_id='nic_id')
```

---

### IP Blocks

#### List IP Blocks

Retrieve a list of IP Blocks.

```
ipblocks = client.list_ipblocks()
```

---

#### Get an IP Block

Retrieves the attributes of a specific IP Block.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| ipblock-id | string | The unique ID of the IP block. | Yes |

```
ipblock = client.get_ipblock('ipblock-id')
```

---

#### Create an IP Block

Creates an IP block.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| location | string | 	This must be one of the locations: us/las, de/fra, de/fkb. | Yes |
| size | int | The size of the IP block you want. | Yes |
| name | string | A descriptive name for the IP block | No |

```
i = IPBlock(
    name='name',
    size=4,
    location='de/fkb'
    )
ipblock = client.reserve_ipblock(i)
```

---

#### Delete an IP Block

Deletes the specified IP Block.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| ipblock-id | string | The unique ID of the IP block. | Yes |

After retrieving an IP block, either by getting it by id, or as a create response object, you can call the `delete` method directly on the object:

```
client.delete_ipblock('ipblock-id')
```
---

### Requests

#### List Requests

Retrieve a list of requests.

```
requests = client.list_requests()
```

---

#### Get a Request

Retrieves the attributes of a specific request.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| request-id | string | The unique ID of the request. | Yes |
| status | boolean | Defins the type of the request status or request. | Yes |

```
request = client.get_request(request_id='request-id', status=False)
```

---

#### Get a Request Status

Retrieves the status of a request.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| request-id | string | The unique ID of the request. | Yes |
| status | boolean | Defins the type of the request status or request. | Yes |

```
request = client.get_request(request_id='request-id', status=True)
```

---

### LANs

#### List LANs

Retrieve a list of LANs within the data center.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |

```
lans = client.list_lans(datacenter_id='datacenter_id')
```

---

#### Create a LAN

Creates a LAN within a data center.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| server_id | string| The unique ID of the server. | Yes |
| name | string | The name of your LAN. ||
| public | bool | Boolean indicating if the LAN faces the public Internet or not. ||
| nics | 	string collection | A collection of NICs associated with the LAN. ||

```
i = NIC(
    name='name',
    public=True)
nic = client.create_nic(
            datacenter_id='datacenter_id',
            server_id='server_id',
            nic=i)
```

---

#### Get a LAN

Retrieves the attributes of a given LAN.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| lan-id | string | The unique ID of the LAN. | Yes |

```
lan = client.get_lan(datacenter_id='datacenter_id', lan_id='lan-id')
```

---

#### Update a LAN

Perform updates to attributes of a LAN.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | The unique ID of the data center. | Yes |
| lan-id | string | The unique ID of the LAN. | Yes |
| name | string | A descriptive name for the LAN. ||
| public | bool | Boolean indicating if the LAN faces the public Internet or not. ||

After retrieving a LAN, either by getting it by id, or as a create response object, you can change it's properties and call the `update` method:

```
lan = client.update_lan(
            datacenter_id='datacenter_id',
            lan_id='lan_id',
            name='name',
            public=False)
```

---

#### Delete a LAN

Deletes the specified LAN.

The following table describes the request arguments:

| NAME| TYPE | DESCRIPTION | REQUIRED |
|---|---|---|---|
| datacenter_id | string | 	The unique ID of the data center. | Yes |
| lan-id | string | The unique ID of the LAN. | Yes |

After retrieving a LAN, either by getting it by id, or as a create response object, you can call the `delete` method directly on the object:

```
lan = client.delete_lan(datacenter_id='datacenter_id', lan_id='lan_id')
```

## Examples

Here are a few examples on how to use the module. In this first one we pull a list of our virtual data centers.

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

##Support

You can find additional examples in the repo `examples` directory. If you find any issues, please let us know via the [DevOps Central community](https://devops.profitbricks.com) or [GitHub's issue system](https://github.com/profitbricks/profitbricks-sdk-python/issues) and we'll check it out.