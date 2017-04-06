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
    * [Create a Data Center](#create-a-data-center)
    * [Update a Data Center](#update-a-data-center)
    * [Delete a Data Center](#delete-a-data-center)
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
  * [Images](#images)
    * [List Images](#list-images)
    * [Get an Image](#get-an-image)
    * [Update an Image](#update-an-image)
    * [Delete an Image](#delete-an-image)
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
  * [IP Blocks](#ip-blocks)
    * [List IP Blocks](#list-ip-blocks)
    * [Get an IP Block](#get-an-ip-block)
    * [Create an IP Block](#create-an-ip-block)
    * [Delete an IP Block](#delete-an-ip-block)
  * [LANs](#lans)
    * [List LANs](#list-lans)
    * [Create a LAN](#create-a-lan)
    * [Get a LAN](#get-a-lan)
    * [Get LAN Members](#get-lan-members)
    * [Update a LAN](#update-a-lan)
    * [Delete a LAN](#delete-a-lan)
  * [Network Interfaces (NICs)](#network-interfaces-nics)
    * [List NICs](#list-nics)
    * [Get a NIC](#get-a-nic)
    * [Create a NIC](#create-a-nic)
    * [Update a NIC](#update-a-nic)
    * [Delete a NIC](#delete-a-nic)
  * [Firewall Rules](#firewall-rules)
    * [List Firewall Rules](#list-firewall-rules)
    * [Get a Firewall Rule](#get-a-firewall-rule)
    * [Create a Firewall Rule](#create-a-firewall-rule)
    * [Update a Firewall Rule](#update-a-firewall-rule)
    * [Delete a Firewall Rule](#delete-a-firewall-rule)
  * [Load Balancers](#load-balancers)
    * [List Load Balancers](#list-load-balancers)
    * [Get a Load Balancer](#get-a-load-balancer)
    * [Create a Load Balancer](#create-a-load-balancer)
    * [Update a Load Balancer](#update-a-load-balancer)
    * [List Load Balanced NICs](#list-load-balanced-nics)
    * [Get a Load Balanced NIC](#get-a-load-balanced-nic)
    * [Associate NIC to a Load Balancer](#associate-nic-to-a-load-balancer)
    * [Remove a NIC Association](#remove-a-nic-association)
  * [Requests](#requests)
    * [List Requests](#list-requests)
    * [Get a Request](#get-a-request)
    * [Get a Request Status](#get-a-request-status)
* [Examples](#examples)
    * [List All Data Centers](#list-all-data-centers)
    * [Search for Images](#search-for-images)
    * [Reserve an IP Block](#reserve-an-ip-block)
    * [Wait for Resources](#wait-for-resources)
    * [Component Build](#component-build)
    * [Composite Build](#composite-build)
* [Support](#support)
* [Testing](#testing)
* [Contributing](#contributing)

## Description

The ProfitBricks SDK for Python provides you with access to the ProfitBricks Cloud API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python.

This guide will walk you through getting setup with the library and performing various actions against the API.

The SDK for Python wraps the ProfitBricks Cloud API. All API operations are performed over SSL and authenticated using your ProfitBricks portal credentials. The API can be accessed within an instance running in ProfitBricks or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response.

## Getting Started

Before you begin you will need to have [signed-up](https://www.profitbricks.com/signup) for a ProfitBricks account. The credentials you setup during sign-up will be used to authenticate against the Cloud API.

### Installation

The ProfitBricks SDK for Python is available on [PyPi](https://pypi.python.org/pypi/profitbricks). You can install the latest stable version using `pip`:

    pip install profitbricks

Done!

### Authenticating

Connecting to ProfitBricks is handled by first setting up your authentication credentials.

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='YOUR_USERNAME', password='YOUR_PASSWORD')

Replace the values for *YOUR_USERNAME* and *YOUR_PASSWORD* with the ProfitBricks credentials you established during sign-up.

You can now use `client` for any future request.

### Error Handling

The SDK will raise custom exceptions when the Cloud API returns an error. There are five exception types:

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

Many of the *get_* or *list_* operations will accept an optional *depth* parameter. Setting this to a value between 0 and 5 affects the amount of data that is returned. The detail returned varies somewhat depending on the resource being queried, however it generally follows this pattern.

| Depth | Description |
|:-:|---|
| 0 | Only direct properties are included. Children are not included. |
| 1 | Direct properties and children's references are returned. |
| 2 | Direct properties and children's properties are returned. |
| 3 | Direct properties, children's properties, and descendant's references are returned. |
| 4 | Direct properties, children's properties, and descendant's properties are returned. |
| 5 | Returns all available properties. |

This SDK sets the *depth=1* by default as that works well in the majority of cases. You may find that setting *depth* to a lower or higher value could simplify a later operation by reducing or increasing the data available in the response object.

### Data Centers

Virtual Data Centers (VDCs) are the foundation of the ProfitBricks platform. VDCs act as logical containers for all other objects you will be creating, e.g., servers. You can provision as many VDCs as you want. VDCs have their own private network and are logically segmented from each other to create isolation.

#### List Data Centers

This operation will list all currently provisioned VDCs that your account credentials provide access to.

There are no request arguments that need to be supplied. You may supply the optional *depth* parameter.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |


    response = client.list_datacenters()

---

#### Retrieve a Data Center

Use this to retrieve details about a specific VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_datacenter(datacenter_id='UUID')

---

#### Create a Data Center

Use this operation to create a new VDC. You can create a "simple" VDC by supplying just the required *name* and *location* parameters. This operation also has the capability of provisioning a "complex" VDC by supplying additional parameters for servers, volumes, LANs, and/or load balancers.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | **yes** | string | The name of the VDC. |
| location | **yes** | string | The physical ProfitBricks location where the VDC will be created. |
| description | no | string | A description for the VDC, e.g. staging, production. |
| servers | no | list | Details about creating one or more servers. See [create a server](#create-a-server). |
| volumes | no | list | Details about creating one or more volumes. See [create a volume](#create-a-volume). |
| lans | no | list | Details about creating one or more LANs. See [create a lan](#create-a-lan). |
| loadbalancers | no | list | Details about creating one or more load balancers. See [create a load balancer](#create-a-load-balancer). |

The following table outlines the locations currently supported:

| Value| Country | City |
|---|---|---|
| us/las | United States | Las Vegas |
| de/fra | Germany | Frankfurt |
| de/fkb | Germany | Karlsruhe |

    datacenter = Datacenter(
        name='Data Center Name',
        description='My new data center',
        location='de/fkb')

    response = client.create_datacenter(datacenter=datacenter)

**NOTES**:
* The value for `name` cannot contain the following characters: (@, /, , |, ‘’, ‘).
* You cannot change the VDC `location` once it has been provisioned.

---

#### Update a Data Center

After retrieving a VDC, either by ID or as a create response object, you can change its properties by calling the `update_datacenter` method. Some parameters may not be changed using `update_datacenter`.

The following table describes the available request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | no | string | The new name of the VDC. |
| description | no | string | The new description of the VDC. |

    response = client.update_datacenter(
        datacenter_id='UUID',
        name='New Name'
        description='New description')

---

#### Delete a Data Center

This will remove all objects within the VDC and remove the VDC object itself.

**NOTE**: This is a highly destructive operation which should be used with extreme caution!

The following table describes the available request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC that you want to delete. |

    response = client.delete_datacenter(datacenter_id='UUID')

---

### Locations

Locations are the physical ProfitBricks data centers where you can provision your VDCs.

#### List Locations

The `list_locations` operation will return the list of currently available locations.

There are no request parameters to supply.

    response = client.list_locations()

---

#### Get a Location

Retrieves the attributes of a specific location.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| location_id | **yes** | string | The ID consisting of country/city. |

    client.get_location('us/las')

---

### Servers

#### List Servers

You can retrieve a list of all the servers provisioned inside a specific VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes**  | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_servers(datacenter_id='UUID')

---

#### Retrieve a Server

Returns information about a specific server such as its configuration, provisioning status, etc.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_server(
        datacenter_id='UUID',
        server_id='UUID')

---

#### Create a Server

Creates a server within an existing VDC. You can configure additional properties such as specifying a boot volume and connecting the server to a LAN.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | **yes** | string | The name of the server. |
| cores | **yes** | int | The total number of cores for the server. |
| ram | **yes** | int | The amount of memory for the server in MB, e.g. 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set `ram_hot_plug` to *True* then you must use a minimum of 1024 MB. |
| availability_zone | no | string | The availability zone in which the server should exist. |
| cpu_family | no | string | Sets the CPU type. "AMD_OPTERON" or "INTEL_XEON". Defaults to "AMD_OPTERON". |
| boot_volume_id | no | string | Reference to a volume used for booting. If not *null* then `boot_cdrom` has to be *null*. |
| boot_cdrom | no | string | Reference to a CD-ROM used for booting. If not *null* then `boot_volume_id` has to be *null*. |
| attach_volumes | no | list | A list of volumes that you want to connect to the server. |
| create_volumes | no | list | A list of volumes that you want to create and attach to the server.|
| nics | no | list | A list of NICs you wish to create at the time the server is provisioned. |

The following table outlines the server availability zones currently supported:

| Availability Zone | Comment |
|---|---|
| AUTO | Automatically Selected Zone |
| ZONE_1 | Fire Zone 1 |
| ZONE_2 | Fire Zone 2 |

    server = Server(
        name='Server Name',
        cores=1,
        ram=2048,
        description='My new server',
        location='de/fkb')

    response = client.create_server(
        datacenter_id='UUID',
        server=server)

---

#### Update a Server

Perform updates to the attributes of a server.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| name | no | string | The name of the server. |
| cores | no | int | The number of cores for the server. |
| ram | no | int | The amount of memory in the server. |
| availability_zone | no | string | The new availability zone for the server. |
| cpu_family | no | string | Sets the CPU type. "AMD_OPTERON" or "INTEL_XEON". Defaults to "AMD_OPTERON". |
| boot_volume_id | no | string | Reference to a volume used for booting. If not *null* then `boot_cdrom` has to be *null*. |
| boot_cdrom | no | string | Reference to a CD-ROM used for booting. If not *null* then `boot_volume_id` has to be *null*. |

After retrieving a server, either by ID or as a create response object, you can change its properties and call the `update_server` method:

    response = client.update_server(
        datacenter_id='UUID',
        server_id='UUID',
        name='New Name')

---

#### Delete a Server

This will remove a server from a data center. **NOTE**: This will not automatically remove the storage volume(s) attached to a server. A separate operation is required to delete a storage volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by ID or as a create response object, you can call the `delete_server` method directly on the object:

    response = client.delete_server(
        datacenter_id='UUID',
        server_id='UUID')

---

#### List Attached Volumes

Retrieves a list of volumes attached to the server.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

After retrieving a server, either by ID or as a create response object, you can call the `get_attached_volumes` method directly on the object:

    response = client.get_attached_volumes(
        datacenter_id='UUID',
        server_id='UUID')

---

#### Attach a Volume

This will attach a pre-existing storage volume to the server.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| volume_id | **yes** | string | The ID of a storage volume. |

After retrieving a server, either by ID or as a create response object, you can call the `attach_volume` method directly on the object:

    response = client.attach_volume(
        datacenter_id='UUID',
        server_id='UUID',
        volume_id='UUID')

---

#### Retrieve an Attached Volume

This will retrieve the properties of an attached volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| volume_id | **yes** | string | The ID of the attached volume. |

After retrieving a server, either by ID or as a create response object, you can call the `get_attached_volume` method directly on the object:

    response = client.get_attached_volume(
        datacenter_id='UUID',
        server_id='UUID',
        volume_id='UUID')

---

#### Detach a Volume

This will detach the volume from the server. Depending on the volume `hot_unplug` settings, this may result in the server being rebooted.

This will NOT delete the volume from your VDC. You will need to make a separate request to delete a volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| volume_id | **yes** | string | The ID of the attached volume. |

After retrieving a server, either by ID or as a create response object, you can call the `detach_volume` method directly on the object:

    response = client.detach_volume(
        datacenter_id='UUID',
        server_id='UUID',
        volume_id='UUID')

---

#### List Attached CD-ROMs

Retrieves a list of CD-ROMs attached to a server.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

After retrieving a server, either by ID or as a create response object, you can call the `get_attached_cdroms` method directly on the object:

    response = client.get_attached_cdroms(
        datacenter_id='UUID',
        server_id='UUID')

---

#### Attach a CD-ROM

You can attach a CD-ROM to an existing server.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| cdrom_id | **yes** | string | The ID of a CD-ROM. |

After retrieving a server, either by ID or as a create response object, you can call the `attach_cdrom` method directly on the object:

    response = client.attach_cdrom(
        datacenter_id='UUID',
        server_id='UUID',
        cdrom_id='UUID')

---

#### Retrieve an Attached CD-ROM

You can retrieve a specific CD-ROM attached to the server.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| cdrom_id | **yes** | string | The ID of the attached CD-ROM. |

After retrieving a server, either by ID or as a create response object, you can call the `get_attached_cdrom` method directly on the object:

    response = client.get_attached_cdrom(
        datacenter_id='UUID',
        server_id='UUID',
        cdrom_id='UUID')

---

#### Detach a CD-ROM

This will detach a CD-ROM from the server.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| cdrom_id | **yes** | string | The ID of the attached CD-ROM. |

After retrieving a server, either by ID or as a create response object, you can call the `detach_cdrom` method directly on the object:

    response = client.detach_cdrom(
        datacenter_id='UUID',
        server_id='UUID',
        cdrom_id='UUID')

---

#### Reboot a Server

This will force a hard reboot of the server. Do not use this method if you want to gracefully reboot the machine. This is the equivalent of powering off the machine and turning it back on.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by ID or as a create response object, you can call the `reboot_server` method directly on the object:

    response = client.reboot_server(
        datacenter_id='UUID',
        server_id='UUID')

---

#### Start a Server

This will start a server. If the server's public IP was deallocated then a new IP will be assigned.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by ID or as a create response object, you can call the `start_server` method directly on the object:

    response = client.start_server(
        datacenter_id='UUID',
        server_id='UUID')

---

#### Stop a Server

This will stop a server. The machine will be forcefully powered off, billing will cease, and the public IP, if one is allocated, will be deallocated.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

After retrieving a server, either by ID or as a create response object, you can call the `stop_server` method directly on the object:

    response = client.stop_server(
        datacenter_id='UUID',
        server_id='UUID')

---

### Images

#### List Images

Retrieve a list of images.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_images()

---

#### Get an Image

Retrieves the attributes of a specific image.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| image_id | **yes** | string | The ID of the image. |

    response = client.get_image('UUID')

---

#### Update an Image

Updates the attributes of a specific user created image. You cannot update the properties of a public image supplied by ProfitBricks.

The following table describes the request arguments:

| Name | Required | Type | Description |
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

    response = client.update_image(
        image_id='UUID',
        name='New Name',
        description='New description',
        licence_type='LINUX')

---

#### Delete an Image

Deletes a specific user created image. You cannot delete public images supplied by ProfitBricks.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| image_id | **yes** | string | The ID of the image. |

    response = client.delete_image('UUID')

---

### Volumes

#### List Volumes

Retrieve a list of volumes within the VDC. If you want to retrieve a list of volumes attached to a server please see the [List Attached Volumes](#list-attached-volumes) entry in the Server section for details.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_volumes(datacenter_id='UUID')

---

#### Get a Volume

Retrieves the attributes of a given volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |

    response = client.get_volume(
        datacenter_id='UUID',
        volume_id='UUID')

---

#### Create a Volume

Creates a volume within the VDC. This will NOT attach the volume to a server. Please see the [Attach a Volume](#attach-a-volume) entry in the Server section for details on how to attach storage volumes.

The following table describes the request arguments:

| Name | Required | Type | Description |
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

**Note:** You will need to provide either the `image` or the `licence_type` parameters when creating a volume. A `licence_type` is required, but if `image` is supplied, it is already set and cannot be changed. Either the `image_password` or `ssh_keys` parameters need to be supplied when creating a volume using one of the official ProfitBricks images. Only official ProfitBricks provided images support the `ssh_keys` and `image_password` parameters.

    volume = Volume(
        name='name',
        size=20,
        bus='VIRTIO',
        type='HDD',
        licence_type='LINUX',
        availability_zone='ZONE_3')

    response = client.create_volume(
        datacenter_id='UUID',
        volume=volume)

---

#### Update a Volume

You can update -- in full or partially -- various attributes on the volume; however, some restrictions are in place:

You can increase the size of an existing storage volume. You cannot reduce the size of an existing storage volume. The volume size will be increased without requiring a reboot if the relevant hot plug settings have been set to *true*. The additional capacity is not added automatically added to any partition, therefore you will need to handle that inside the OS afterwards. Once you have increased the volume size you cannot decrease the volume size.

Since an existing volume is being modified, none of the request parameters are specifically required as long as the changes being made satisfy the requirements for creating a volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
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

After retrieving a volume, either by ID or as a create response object, you can change its properties and call the `update_volume` method:

    response = client.update_volume(
        datacenter_id='UUID',
        volume_id='UUID',
        size=6,
        name='New Name')

---

#### Delete a Volume

Deletes the specified volume. This will result in the volume being removed from your data center. Use this with caution.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |

After retrieving a volume, either by ID or as a create response object, you can call the `delete_volume` method directly on the object:

    response = client.delete_volume(
        datacenter_id='UUID',
        volume_id='UUID')

---

#### Create a Volume Snapshot

Creates a snapshot of a volume within the VDC. You can use a snapshot to create a new storage volume or to restore a storage volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |
| name | no | string | The name of the snapshot. |
| description | no | string | The description of the snapshot. |

After retrieving a volume, either by ID or as a create response object, you can call the `create_snapshot` method directly on the object:

    response = client.create_snapshot(
        datacenter_id='UUID',
        volume_id='UUID',
        name='Snapshot Name',
        description='Snapshot description')

---

#### Restore a Volume Snapshot

This will restore a snapshot onto a volume. A snapshot is created as just another image that can be used to create new volumes or to restore an existing volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |
| snapshot_id | **yes** | string |  The ID of the snapshot. |

After retrieving a volume, either by ID or as a create response object, you can call the `restore_snapshot` method directly on the object:

    response = client.restore_snapshot(
        datacenter_id='UUID',
        volume_id='UUID',
        snapshot_id='UUID')

---

### Snapshots

#### List Snapshots

You can retrieve a list of all available snapshots.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_snapshots()

---

#### Get a Snapshot

Retrieves the attributes of a specific snapshot.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| snapshot_id | **yes** | string | The ID of the snapshot. |

    response = client.get_snapshot(snapshot_id='UUID')

---

#### Update a Snapshot

Perform updates to attributes of a snapshot.

The following table describes the request arguments:

| Name | Required | Type | Description |
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

After retrieving a snapshot, either by ID or as a create response object, you can change its properties and call the `update_snapshot` method:

    response = client.update_snapshot(
        snapshot_id='UUID',
        name='New Name',
        description='New description')

---

#### Delete a Snapshot

Deletes the specified snapshot.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| snapshot_id | **yes** | string | The ID of the snapshot. |

After retrieving a snapshot, either by ID or as a create response object, you can call the `delete_snapshot` method directly on the object:

    response = client.delete_snapshot(snapshot_id='deleting_snapshot_id')

---

### IP Blocks

The IP block operations assist with managing reserved /static public IP addresses.

#### List IP Blocks

Retrieve a list of available IP blocks.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_ipblocks()

---

#### Get an IP Block

Retrieves the attributes of a specific IP block.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| ipblock_id | **yes** | string | The ID of the IP block. |

    response = client.get_ipblock('UUID')

---

#### Create an IP Block

Creates an IP block. IP blocks are attached to a location, so you must specify a valid `location` along with a `size` parameter indicating the number of IP addresses you want to reserve in the IP block. Servers or other resources using an IP address from an IP block must be in the same `location`.

The following table describes the request arguments:

| Name | Required | Type | Description |
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

    ipblock = IPBlock(
        name='IP Block Name',
        size=4,
        location='de/fkb')

    response = client.reserve_ipblock(ipblock)

---

#### Delete an IP Block

Deletes the specified IP Block.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| ipblock_id | **yes** | string | The ID of the IP block. |

After retrieving an IP block, either by ID or as a create response object, you can call the `delete_ipblock` method directly on the object:

    response = client.delete_ipblock('UUID')

---

### LANs

#### List LANs

Retrieve a list of LANs within the VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_lans(datacenter_id='UUID')

---

#### Create a LAN

Creates a LAN within a VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | no | string | The name of your LAN. |
| public | **Yes** | bool | Boolean indicating if the LAN faces the public Internet or not. |
| nics | no | list | A list of NICs associated with the LAN. |

    response = client.create_lan(
        datacenter_id='UUID',
        name='LAN Name',
        public=False)

---

#### Get a LAN

Retrieves the attributes of a given LAN.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | int | The ID of the LAN. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_lan(
        datacenter_id='UUID',
        lan_id=ID)

---

#### Get LAN Members

Retrieves the list of NICs that are part of the LAN.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | int | The ID of the LAN. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_lan_members(
        datacenter_id='UUID',
        lan_id=ID)

---

#### Update a LAN

Perform updates to attributes of a LAN.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | int | The ID of the LAN. |
| name | no | string | A descriptive name for the LAN. |
| public | no | bool | Boolean indicating if the LAN faces the public Internet or not. |

After retrieving a LAN, either by ID or as a create response object, you can change its properties and call the `update_lan` method:

    response = client.update_lan(
        datacenter_id='UUID',
        lan_id=ID,
        name='New LAN Name',
        public=False)

---

#### Delete a LAN

Deletes the specified LAN.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | string | The ID of the LAN. |

After retrieving a LAN, either by ID or as a create response object, you can call the `delete_lan` method directly on the object:

    response = client.delete_lan(
        datacenter_id='datacenter_id',
        lan_id=ID)

---

### Network Interfaces (NICs)

#### List NICs

Retrieve a list of LANs within the VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_nics(
        datacenter_id='UUID',
        server_id='UUID')

---

#### Get a NIC

Retrieves the attributes of a given NIC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_nic(
        datacenter_id='UUID',
        server_id='UUID',
        nic_id='UUID')

---

#### Create a NIC

Adds a NIC to the target server.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string| The ID of the server. |
| name | no | string | The name of the NIC. |
| ips | no | list | IP addresses assigned to the NIC. |
| dhcp | no | bool | Set to *false* if you wish to disable DHCP on the NIC. Default: *true*. |
| lan | **yes** | int | The LAN ID the NIC will sit on. If the LAN ID does not exist it will be created. |
| nat | no | bool | Indicates the private IP address has outbound access to the public internet. |
| firewall_active | no | bool | Set this to *true* to enable the ProfitBricks firewall, *false* to disable. |
| firewall_rules | no | list | A list of firewall rules associated with the NIC. |

    nic = NIC(
        name='NIC Name',
        dhcp=True,
        lan=1,
        nat=False)

    response = client.create_nic(
        datacenter_id='UUID',
        server_id='UUID',
        nic=nic)

---

#### Update a NIC

You can update -- in full or partially -- various attributes on the NIC; however, some restrictions are in place:

The primary address of a NIC connected to a load balancer can only be changed by changing the IP of the load balancer. You can also add additional reserved, public IPs to the NIC.

The user can specify and assign private IPs manually. Valid IP addresses for private networks are 10.0.0.0/8, 172.16.0.0/12 or 192.168.0.0/16.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string| The ID of the server. |
| nic_id | **yes** | string| The ID of the NIC. |
| name | no | string | The name of the NIC. |
| ips | no | list | IPs assigned to the NIC represented as a list of strings. |
| dhcp | no | bool | Boolean value that indicates if the NIC is using DHCP or not. |
| lan | no | int | The LAN ID the NIC sits on. |
| nat | no | bool | Indicates the private IP address has outbound access to the public internet. |
| firewall_active | no | bool | Set this to *true* to enable the ProfitBricks firewall, *false* to disable. |

After retrieving a NIC, either by ID or as a create response object, you can call the `update_nic` method directly on the object:

    response = client.update_nic(
        datacenter_id='UUID',
        server_id='UUID',
        nic_id='UUID',
        name='New Name')

---

#### Delete a NIC

Deletes the specified NIC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string| The ID of the server. |
| nic_id | **yes** | string| The ID of the NIC. |

After retrieving a NIC, either by ID or as a create response object, you can call the `delete_nic` method directly on the object:

    response = client.delete_nic(
        datacenter_id='UUID',
        server_id='UUID',
        nic_id='UUID')

---

### Firewall Rules

#### List Firewall Rules

Retrieves a list of firewall rules associated with a particular NIC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_firewall_rules(
        datacenter_id='UUID',
        server_id='UUID',
        nic_id='UUID')

---

#### Get a Firewall Rule

Retrieves the attributes of a given firewall rule.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| firewall_rule_id | **yes** | string | The ID of the firewall rule. |

    response = client.get_firewall_rule(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID',
        firewall_rule_id='UUID')

---

#### Create a Firewall Rule

This will add a firewall rule to the NIC.

The following table describes the request arguments:

| Name | Required | Type | Description |
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

    fwrule = FirewallRule(
        name='Allow SSH',
        protocol='TCP',
        source_mac='01:23:45:67:89:00',
        port_range_start=22,
        port_range_end=22)

    response = client.create_firewall_rule(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID',
        firewall_rule=fwrule)

---

#### Update a Firewall Rule

Perform updates to attributes of a firewall rule.

The following table describes the request arguments:

| Name | Required | Type | Description |
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

After retrieving a firewall rule, either by ID or as a create response object, you can change its properties and call the `update_firewall_rule` method:

    response = client.update_firewall_rule(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID',
        firewall_rule_id='UUID',
        name="Updated Name")

---

#### Delete a Firewall Rule

Removes the specific firewall rule.

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| firewall_rule_id | **yes** | string | The ID of the firewall rule. |

After retrieving a firewall rule, either by ID or as a create response object, you can call the `delete_firewall_rule` method directly on the object:

    response = client.delete_firewall_rule(
        datacenter_id='UUID',
        server_id='UUID',
        nic_id='UUID',
        firewall_rule_id='UUID')

---

### Load Balancers

#### List Load Balancers

Retrieve a list of load balancers within the data center.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_loadbalancers(datacenter_id='UUID')

---

#### Get a Load Balancer

Retrieves the attributes of a given load balancer.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |

    response = client.get_loadbalancer(
        datacenter_id='UUID',
        loadbalancer_id='UUID')

---

#### Create a Load Balancer

Creates a load balancer within the VDC. Load balancers can be used for public or private IP traffic.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | **yes** | string | The name of the load balancer. |
| ip | no | string | IPv4 address of the load balancer. All attached NICs will inherit this IP. |
| dhcp | no | bool | Indicates if the load balancer will reserve an IP using DHCP. |
| balancednics | no | list | List of NICs taking part in load-balancing. All balanced NICs inherit the IP of the load balancer. |

    loadbalancer = LoadBalancer(
        name='Load Balancer Name',
        dhcp=True)

    response = client.create_loadbalancer(
        datacenter_id='UUID',
        loadbalancer=loadbalancer)

---

#### Update a Load Balancer

Perform updates to attributes of a load balancer.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | no | string | The name of the load balancer. |
| ip | no | string | The IP of the load balancer. |
| dhcp | no | bool | Indicates if the load balancer will reserve an IP using DHCP. |

After retrieving a load balancer, either by ID or as a create response object, you can change it's properties and call the `update_loadbalancer` method:

    response = client.update_loadbalancer(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        name="New Name")

---

#### Delete a Load Balancer

Deletes the specified load balancer.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| load_balancer_id | **yes** | string | The ID of the load balancer. |

After retrieving a load balancer, either by ID or as a create response object, you can call the `delete_loadbalancer` method directly on the object:

    response = client.delete_loadbalancer(
        datacenter_id='UUID',
        loadbalancer_id='UUID')

---

#### List Load Balanced NICs

This will retrieve a list of NICs associated with the load balancer.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

After retrieving a load balancer, either by ID or as a create response object, you can call the `get_loadbalancer_members` method directly on the object:

    response = client.get_loadbalancer_members(
        datacenter_id='UUID',
        loadbalancer_id='UUID')

---

#### Get a Load Balanced NIC

Retrieves the attributes of a given load balanced NIC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |
| nic_id | **yes** | string | The ID of the NIC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

After retrieving a load balancer, either by ID or as a create response object, you can call the `get_loadbalanced_nic` method directly on the object:

    response = client.get_loadbalanced_nic(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID')

---

#### Associate NIC to a Load Balancer

This will associate a NIC to a load balancer, enabling the NIC to participate in load-balancing.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |
| nic_id | **yes** | string | The ID of the NIC. |

After retrieving a load balancer, either by ID or as a create response object, you can call the `add_loadbalanced_nics` method directly on the object:

    response = client.add_loadbalanced_nics(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID')

---

#### Remove a NIC Association

Removes the association of a NIC with a load balancer.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |
| nic_id | **yes** | string | The ID of the load balancer. |

After retrieving a load balancer, either by ID or as a create response object, you can call the `remove_loadbalanced_nic` method directly on the object:

    response = client.remove_loadbalanced_nic(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID')

---

### Requests

Each call to the ProfitBricks Cloud API is assigned a request ID. These operations can be used to get information about the requests that have been submitted and their current status.

#### List Requests

Retrieve a list of requests.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_requests()

---

#### Get a Request

Retrieves the attributes of a specific request. This operation shares the same `get_request` method used for getting request status, however the response it determined by the boolean value you pass for *status*. To get details about the request itself, you want to pass a *status* of *False*.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| request_id | **yes** | string | The ID of the request. |
| status | **yes** | bool | Set to *False* to have the request details returned. |

    response = client.get_request(
        request_id='UUID',
        status=False)

---

#### Get a Request Status

Retrieves the status of a request. This operation shares the same `get_request` method used for getting the details of a request, however the response it determined by the boolean value you pass for *status*. To get the request status, you want to pass a *status* of *True*.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| request_id | **yes** | string | The ID of the request. |
| status | **yes** | boolean | Set to *True* to have the status of the request returned. |

    response = client.get_request(
        request_id='UUID',
        status=True)

---

## Examples

Below are some examples using the SDK for Python. These examples will assume credentials are being set with environment variables:

    export PROFITBRICKS_USERNAME=username
    export PROFITBRICKS_PASSWORD=password

### List All Data Centers

This simple example will list all data centers under an account.

    #!/usr/bin/python

    import json
    import os

    from profitbricks.client import ProfitBricksService

    # Instatiate ProfitBricks connection
    client = ProfitBricksService(
        username=os.getenv('PROFITBRICKS_USERNAME'),
        password=os.getenv('PROFITBRICKS_PASSWORD'))

    # List data centers
    datacenters = client.list_datacenters()
    print json.dumps(datacenters, indent=4)

### Search for Images

The following example will provide a method for retrieving a list of images based on a partial case-insensitive name and location match.

    #!/usr/bin/python

    import os

    from profitbricks.client import ProfitBricksService


    def find_image(conn, name, location):
        '''
        Find image by partial name and location
        '''
        images = []
        for item in conn.list_images()['items']:
            if (item['properties']['location'] == location and
               item['properties']['imageType'] == 'HDD' and
               name.lower() in item['properties']['name'].lower()):
                images.append(item)
        return images

    # Instantiate ProfitBricks connection
    client = ProfitBricksService(
        username=os.getenv('PROFITBRICKS_USERNAME'),
        password=os.getenv('PROFITBRICKS_PASSWORD'))

    # Search criteria based on partial case-insensitive name and location
    name = 'Ubuntu'
    location = 'de/fkb'

    # Find images based on above search criteria
    for image in find_image(client, name, location):
        print "{0}\t{1}\t{2}".format(
            image['id'],
            image['properties']['name'],
            image['properties']['location'])

### Reserve an IP Block

Here we will reserve a public IP block.

    #!/usr/bin/python

    import json
    import os

    from profitbricks.client import ProfitBricksService, IPBlock


    # Instatiate ProfitBricks connection
    client = ProfitBricksService(
        username=os.getenv('PROFITBRICKS_USERNAME'),
        password=os.getenv('PROFITBRICKS_PASSWORD'))

    ipblock = IPBlock(location='us/las', size=5)

    response = client.reserve_ipblock(ipblock)

    print json.dumps(response, indent=4)

### Wait for Resources

The remaining examples will require dependent resources. A volume cannot be attached to a server before the server and volume are finished provisioning. Therefore, we require a `wait_for_completion` method that will stop and wait for the server and volume to finish provisioning before attaching the volume to the server.

The below `wait_for_completion` method example will utilize the `Request` operation to poll the status until a request is finished. This method will be called in additional examples.

    #!/usr/bin/python

    import time


    def wait_for_completion(conn, response, timeout):
        '''
        Poll resource request status until resource is provisioned.
        '''
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

### Component Build

ProfitBricks allows servers to be built by their individual components. That is, by connecting customized components such as servers, volumes, and NICs together. For example, a server can be provisioned in one request followed by one or more NICs and volumes in following requests. The volumes can then be attached separately to the server.

It is important to note that you will need to wait for each individual component to finish provisioning before it can be used in subsequent operations. This behavior is demonstrated below.

    #!/usr/bin/python

    import json
    import os

    from common import wait_for_completion
    from profitbricks.client import ProfitBricksService
    from profitbricks.client import (
        Datacenter, LAN, Server, NIC, Volume, FirewallRule)

    client = ProfitBricksService(
        username=os.getenv('PROFITBRICKS_USERNAME'),
        password=os.getenv('PROFITBRICKS_PASSWORD'))

    timeout = 1800

    # Create data center
    datacenter = Datacenter(
        name='Python SDK Data Center',
        description='Python SDK data center',
        location='us/las')

    response = client.create_datacenter(datacenter=datacenter)
    wait_for_completion(client, response, timeout)
    datacenter_id = response['id']

    # Create public LAN
    lan = LAN(name="Public LAN", public=True)

    response = client.create_lan(datacenter_id, lan=lan)
    wait_for_completion(client, response, timeout)
    lan_id = response['id']

    # Create server
    server = Server(
        name='Python SDK Server',
        ram=4096,
        cores=4,
        cpu_family='INTEL_XEON')

    response = client.create_server(datacenter_id=datacenter_id, server=server)
    wait_for_completion(client, response, timeout)
    server_id = response['id']

    # Create public NIC
    nic = NIC(
        name='Public NIC',
        dhcp=True,
        lan=lan_id,
        firewall_active=True,
        nat=False)

    response = client.create_nic(
        datacenter_id=datacenter_id,
        server_id=server_id,
        nic=nic)
    wait_for_completion(client, response, timeout)
    nic_id = response['id']

    # Create firwall rule
    fwrule = FirewallRule(
        name='Allow SSH',
        protocol='TCP',
        source_ip='0.0.0.0',
        port_range_start=22,
        port_range_end=22,
        icmp_type=None)

    response = client.create_firewall_rule(
        datacenter_id=datacenter_id,
        server_id=server_id,
        nic_id=nic_id,
        firewall_rule=fwrule)
    wait_for_completion(client, response, timeout)

    # Create system volume
    volume1 = Volume(
        name='System Volume',
        size=20,
        image='0d4f97f0-1689-11e7-97ce-525400f64d8d',
        bus='VIRTIO',
        type='HDD',
        ssh_keys=['ssh-rsa AAAAB3NzaC1yc2EAAAADAQ...'],
        image_password='s3cr3tpass0rd',
        availability_zone='ZONE_3')

    response = client.create_volume(
        datacenter_id=datacenter_id,
        volume=volume1)
    wait_for_completion(client, response, timeout)
    volume1_id = response['id']

    # Attach system volume
    response = client.attach_volume(
        datacenter_id=datacenter_id,
        server_id=server_id,
        volume_id=volume1_id)
    wait_for_completion(client, response, timeout)

    # Create data volume
    volume2 = Volume(
        name='Data Volume',
        size=100,
        type='SSD',
        bus='VIRTIO',
        license_type='OTHER')

    response = client.create_volume(
        datacenter_id=datacenter_id,
        volume=volume2)
    wait_for_completion(client, response, timeout)
    volume2_id = response['id']

    # Attach data volume
    response = client.attach_volume(
        datacenter_id=datacenter_id,
        server_id=server_id,
        volume_id=volume2_id)
    wait_for_completion(client, response, timeout)

    live_datacenter = client.get_datacenter(datacenter_id=datacenter_id, depth=5)
    print json.dumps(live_datacenter, indent=4)

### Composite Build

The ProfitBricks platform also allows fully operational servers to be provisioned with a single request. This is accomplished by nesting related resources.

Multiple servers, volumes, LANs, and load balancers can be nested under a data center, multiple NICs and volumes can be nested under servers, and firewall rules under NICs.

This example will demonstrate composite resources.

    #!/usr/bin/python

    import json
    import os

    from common import wait_for_completion
    from profitbricks.client import ProfitBricksService
    from profitbricks.client import Datacenter, Server, NIC, Volume, FirewallRule

    # Instatiate ProfitBricks connection
    client = ProfitBricksService(
        username=os.getenv('PROFITBRICKS_USERNAME'),
        password=os.getenv('PROFITBRICKS_PASSWORD'))

    # Define a firewall rule
    fwrule1 = FirewallRule(
        name='Allow SSH',
        protocol='TCP',
        source_ip='0.0.0.0',
        port_range_start=22,
        port_range_end=22,
        icmp_type=None)

    # Define a public NIC
    nic1 = NIC(
        name='Public NIC',
        dhcp=True,
        lan=1,
        firewall_active=True,
        firewall_rules=[fwrule1],
        nat=False)

    # Define a private NIC
    nic2 = NIC(
        name='Private NIC',
        dhcp=True,
        lan=2)

    # Define a system volume
    volume1 = Volume(
        name='System Volume',
        size=20,
        image='0d4f97f0-1689-11e7-97ce-525400f64d8d',
        bus='VIRTIO',
        type='HDD',
        ssh_keys=['ssh-rsa AAAAB3NzaC1yc2EAAAADAQ...'],
        image_password='s3cr3tpass0rd',
        availability_zone='ZONE_3')

    # Define a data volume
    volume2 = Volume(
        name='Data Volume',
        size=100,
        type='SSD',
        bus='VIRTIO',
        licence_type='OTHER')

    # Define a server with associated NICs and volumes
    server = Server(
        name='Python SDK Server',
        ram=4096,
        cores=4,
        cpu_family='INTEL_XEON',
        nics=[nic1, nic2],
        create_volumes=[volume1, volume2])

    # Define a data center with the server
    datacenter = Datacenter(
        name='Python SDK Data Center',
        description='Python SDK data center',
        location='us/las',
        servers=[server])

    # Initiate the data center and nested resource provisioning
    response = client.create_datacenter(datacenter)

    # Wait for the data center and nested resources to finish provisioning
    wait_for_completion(client, response, 1800)

    datacenter_id = response['id']

    # Set the first LAN to public
    response = client.update_lan(
        datacenter_id=datacenter_id,
        lan_id=1,
        name='Public LAN',
        public=True)

    wait_for_completion(client, response, 1800)

    # Print the data center properties and nested resources
    response = client.get_datacenter(datacenter_id=datacenter_id, depth=5)
    print json.dumps(response, indent=4)

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
