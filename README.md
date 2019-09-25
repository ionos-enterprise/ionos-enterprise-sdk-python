
# Python SDK

Version: profitbricks-sdk-python **4.2.0**

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
    * [User Management](#user-management)
        * [List Groups](#list-groups)
        * [Get a Group](#get-a-group)
        * [Create a Group](#create-a-group)
        * [Update a Group](#update-a-group)
        * [Delete a Group](#delete-a-group)
        * [List Shares](#list-shares)
        * [Get a Share](#get-a-share)
        * [Add a Share](#add-a-share)
        * [Update a Share](#update-a-share)
        * [Delete a Share](#delete-a-share)
        * [List Users](#list-users)
        * [Get a User](#get-a-user)
        * [Create a User](#create-a-user)
        * [Update a User](#update-a-user)
        * [Delete a User](#delete-a-user)
        * [List Users in a Group](#list-users-in-a-group)
        * [Add User to Group](#add-user-to-group)
        * [Remove User from a Group](#remove-user-from-a-group)
        * [List Resources](#list-resources)
        * [Get a Resource](#get-a-resource)
    * [Contract Resources](#contract-resources)
        * [List Contract Resources](#list-contract-resources)
    * [Requests](#requests)
        * [List Requests](#list-requests)
        * [Get a Request](#get-a-request)
        * [Get a Request Status](#get-a-request-status)
    * [Kubernetes](#kubernetes)
        * [List Kubernetes Clusters](#list-kubernetes-clusters)
        * [Create a Kubernetes Cluster](#create-a-kubernetes-cluster)
        * [Retrieve a Kubernetes Cluster](#retrieve-a-kubernetes-cluster)
        * [Delete a Kubernetes Cluster](#delete-a-kubernetes-cluster)
        * [Retrieve a Kubernetes Cluster KubeConfig](#retrieve-a-kubernetes-cluster-kubeconfig)
        * [List Kubernetes NodePools](#list-kubernetes-nodepools)
        * [Create a NodePool for a Kubernetes Cluster](#create-a-nodepool-for-a-kubernetes-cluster)
        * [Retrieve a NodePool](#retrieve-a-nodepool)
        * [Delete a NodePool](#delete-a-nodepool)
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

#### Installation

The ProfitBricks SDK for Python is available on [PyPi](https://pypi.python.org/pypi/profitbricks). You can install the latest stable version using `pip`:

    pip install profitbricks

Done!

#### Authenticating

Connecting to ProfitBricks is handled by first setting up your authentication credentials.

    from profitbricks.client import ProfitBricksService

    client = ProfitBricksService(
        username='YOUR_USERNAME', password='YOUR_PASSWORD')

Replace the values for *YOUR_USERNAME* and *YOUR_PASSWORD* with the ProfitBricks credentials you established during sign-up.

You can now use `client` for any future request.

#### Error Handling

The SDK will raise custom exceptions when the Cloud API returns an error. There are five exception types:

| Exception | HTTP Code | Description |
|---|:-:|---|
| PBNotAuthorizedError | 401 | The supplied user credentials are invalid. |
| PBNotFoundError | 404 | The requested resource cannot be found. |
| PBValidationError | 422 | The request body includes invalid JSON. |
| PBRateLimitExceededError | 429 | The Cloud API rate limit has been exceeded. |
| PBError | Other | A generic exception for all other status codes. |

## Reference

This section provides details on all the available operations and the arguments they accept. Brief code snippets demonstrating usage are also included.

`client` is the `ProfitBricksService` class imported `from profitbricks.client import ProfitBricksService`

#### Depth

Many of the *get_* or *list_* operations will accept an optional *depth* argument. Setting this to a value between 0 and 5 affects the amount of data that is returned. The detail returned varies somewhat depending on the resource being queried, however it generally follows this pattern.

| Depth | Description |
|:-:|---|
| 0 | Only direct properties are included. Children are not included. |
| 1 | Direct properties and children's references are returned. |
| 2 | Direct properties and children's properties are returned. |
| 3 | Direct properties, children's properties, and descendant's references are returned. |
| 4 | Direct properties, children's properties, and descendant's properties are returned. |
| 5 | Returns all available properties. |

This SDK sets the *depth=1* by default as that works well in the majority of cases. You may find that setting *depth* to a lower or higher value could simplify a later operation by reducing or increasing the data available in the response object.

## Data Centers

Virtual Data Centers (VDCs) are the foundation of the ProfitBricks platform. VDCs act as logical containers for all other objects you will be creating, e.g., servers. You can provision as many VDCs as you want. VDCs have their own private network and are logically segmented from each other to create isolation.

#### List Data Centers

This operation will list all currently provisioned VDCs that your account credentials provide access to.

There are no request arguments that need to be supplied. You may supply the optional *depth* argument.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. See the [Depth](#depth) section. |

Call `list_datacenters`:

    response = client.list_datacenters()

---

#### Retrieve a Data Center

Use this to retrieve details about a specific VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. See the [Depth](#depth) section. |

Pass the arguments to `get_datacenter`:

    response = client.get_datacenter(datacenter_id='UUID')

---

#### Create a Data Center

Use this operation to create a new VDC. You can create a "simple" VDC by supplying just the required *name* and *location* arguments. This operation also has the capability of provisioning a "complex" VDC by supplying additional arguments for servers, volumes, LANs, and/or load balancers.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter | **yes** | object | A [Datacenter object](#datacenter-resource-object) describing the VDC being created. |

Build the `Datacenter` resource object:

    datacenter = Datacenter(
        name='Data Center Name',
        description='My new data center',
        location='de/fkb')

Pass the object to `create_datacenter`:

    response = client.create_datacenter(datacenter=datacenter)

#### Datacenter Resource Object

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | **yes** | string | The name of the VDC. |
| location | **yes** | string | The physical ProfitBricks location where the VDC will be created. |
| description | no | string | A description for the VDC, e.g. staging, production. |
| servers | no | list | A list of one or more [Server objects](#server-resource-object) to be created. |
| volumes | no | list | A list of one or more [Volume objects](#volume-resource-object) to be created. |
| lans | no | list | A list of one or more [LAN objects](#lan-resource-object) to be created. |
| loadbalancers | no | list | A list of one or more [LoadBalancer objects](#load-balancer-resource-object) to be created. |

The following table outlines the locations currently supported:

| Value| Country | City |
|---|---|---|
| us/las | United States | Las Vegas |
| us/ewr | United States | Newark |
| de/fra | Germany | Frankfurt |
| de/fkb | Germany | Karlsruhe |

**NOTES**:

* The value for `name` cannot contain the following characters: (@, /, , |, ‘’, ‘).
* You cannot change the VDC `location` once it has been provisioned.

---

#### Update a Data Center

After retrieving a VDC, either by ID or as a create response object, you can change its properties by calling the `update_datacenter` method. Some arguments may not be changed using `update_datacenter`.

The following table describes the available request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| name | no | string | The new name of the VDC. |
| description | no | string | The new description of the VDC. |

Pass the arguments to `update_datacenter`:

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

Pass the argument to `delete_datacenter`:

    response = client.delete_datacenter(datacenter_id='UUID')

---

## Locations

Locations are the physical ProfitBricks data centers where you can provision your VDCs.

#### List Locations

The `list_locations` operation will return the list of currently available locations.

There are no request arguments to supply.

    response = client.list_locations()

---

#### Get a Location

Retrieves the attributes of a specific location.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| location_id | **yes** | string | The ID consisting of country/city. |

Pass the argument to `get_location`:

    client.get_location('us/las')

---

## Servers

#### List Servers

You can retrieve a list of all the servers provisioned inside a specific VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes**  | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. See the [Depth](#depth) section. |

Pass the arguments to `list_servers`:

    response = client.list_servers(datacenter_id='UUID')

---

#### Retrieve a Server

Returns information about a specific server such as its configuration, provisioning status, etc.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `get_server`:

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
| server | **yes** | object | A [Server object](#server-resource-object) describing the server being created. |

Build a [Server](#server-resource-object) object:

    server = Server(
        name='Server Name',
        cores=1,
        ram=2048,
        description='My new server',
        location='de/fkb')

Pass the object and other arguments to `create_server`:

    response = client.create_server(
        datacenter_id='UUID',
        server=server)

#### Server Resource Object

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | **yes** | string | The name of the server. |
| cores | **yes** | int | The total number of cores for the server. |
| ram | **yes** | int | The amount of memory for the server in MB, e.g. 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set `ram_hot_plug` to *True* then you must use a minimum of 1024 MB. |
| availability_zone | no | string | The availability zone in which the server should exist. |
| cpu_family | no | string | Sets the CPU type. "AMD_OPTERON" or "INTEL_XEON". Defaults to "AMD_OPTERON". |
| boot_volume_id | no | string | A volume ID that the server will boot from. If not *null* then `boot_cdrom` has to be *null*. |
| boot_cdrom | no | string | A CD-ROM image ID used for booting. If not *null* then `boot_volume_id` has to be *null*. |
| attach_volumes | no | list | A list of existing volume IDs that you want to connect to the server. |
| create_volumes | no | list | One or more [Volume objects](#volume-resource-object) that you want to create and attach to the server.|
| nics | no | list | One or more [NIC objects](#nic-resource-object) that you wish to create at the time the server is provisioned. |

The following table outlines the server availability zones currently supported:

| Availability Zone | Comment |
|---|---|
| AUTO | Automatically Selected Zone |
| ZONE_1 | Fire Zone 1 |
| ZONE_2 | Fire Zone 2 |

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
| boot_volume_id | no | string | A volume ID used for booting. If not *null* then `boot_cdrom` has to be *null*. |
| boot_cdrom | no | string | A CD-ROM image ID used for booting. If not *null* then `boot_volume_id` has to be *null*. |

Pass the arguments to `update_server`:

    response = client.update_server(
        datacenter_id='UUID',
        server_id='UUID',
        name='New Name')

---

#### Delete a Server

This will remove a server from a VDC. **NOTE**: This will not automatically remove the storage volume(s) attached to a server. A separate operation is required to delete a storage volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server that will be deleted. |

Pass the arguments to `delete_server`:

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
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `get_attached_volumes`:

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

Pass the arguments to `attach_volume`:

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

Pass the arguments to `get_attached_volume`:

    response = client.get_attached_volume(
        datacenter_id='UUID',
        server_id='UUID',
        volume_id='UUID')

---

#### Detach a Volume

This will detach the volume from the server. Depending on the volume `hot_unplug` settings, this may result in the server being rebooted. If `disc_virtio_hot_unplug` has been set to *true*, then a reboot should not be required.

This will **NOT** delete the volume from your VDC. You will need to make a separate request to delete a volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| volume_id | **yes** | string | The ID of the attached volume. |

Pass the arguments to `detach_volume`:

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
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `get_attached_cdroms`:

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

Pass the arguments to `attach_cdrom`:

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

Pass the arguments to `get_attached_cdrom`:

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

Pass the arguments to `detach_cdrom`:

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

Pass the arguments to `reboot_server`:

    response = client.reboot_server(
        datacenter_id='UUID',
        server_id='UUID')

---

#### Start a Server

This will start a server. If a DHCP assigned public IP was deallocated when the server was stopped, then a new IP will be assigned.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |

Pass the arguments to `start_server`:

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

Pass the arguments to `stop_server`:

    response = client.stop_server(
        datacenter_id='UUID',
        server_id='UUID')

---

## Images

#### List Images

Retrieve a list of images.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `list_images`:

    response = client.list_images()

---

#### Get an Image

Retrieves the attributes of a specific image.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| image_id | **yes** | string | The ID of the image. |

Pass the arguments to `get_image`:

    response = client.get_image('UUID')

---

#### Update an Image

Updates the attributes of a specific user created image. You **CANNOT** update the properties of a public image supplied by ProfitBricks.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| image_id | **yes** | string | The ID of the image. |
| name | no | string | The name of the image. |
| description | no | string | The description of the image. |
| licence_type | no | string | The snapshot's licence type: LINUX, WINDOWS, WINDOWS2016, UNKNOWN or OTHER. |
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

Pass the arguments to `delete_image`:

    response = client.delete_image('UUID')

---

## Volumes

#### List Volumes

Retrieve a list of volumes within the VDC. If you want to retrieve a list of volumes attached to a server please see the [List Attached Volumes](#list-attached-volumes) entry in the Server section for details.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `list_volumes`:

    response = client.list_volumes(datacenter_id='UUID')

---

#### Get a Volume

Retrieves the attributes of a given volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |

Pass the arguments to `get_volume`:

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
| volume | **yes** | object | A [Volume object](#volume-resource-object) you wish to create. |

Build the `Volume` resource object:

    volume = Volume(
        name='name',
        size=20,
        bus='VIRTIO',
        type='HDD',
        licence_type='LINUX',
        availability_zone='ZONE_3')

Pass the object and arguments to `create_volume`:

    response = client.create_volume(
        datacenter_id='UUID',
        volume=volume)

#### Volume Resource Object

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | no | string | The name of the volume. |
| size | **yes** | int | The size of the volume in GB. |
| bus | no | string | The bus type of the volume (VIRTIO or IDE). Default: VIRTIO. |
| image | **yes** | string | The image or snapshot ID. Can be left empty for a data volume, however you'll need to set the `licence_type`. Default: *null* |
| image_alias | **yes** | string | The alias of the image. |
| type | **yes** | string | The volume type, HDD or SSD. Default: HDD|
| licence_type | **yes** | string | The licence type of the volume. Options: LINUX, WINDOWS, WINDOWS2016, UNKNOWN, OTHER. Default: UNKNOWN |
| image_password | **yes** | string | A password to set on the volume for the appropriate root or administrative account. This field may only be set in creation requests. When reading, it always returns *null*. The password has to contain 8-50 characters. Only these characters are allowed: [abcdefghjkmnpqrstuvxABCDEFGHJKLMNPQRSTUVX23456789] |
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

**Note:** You will need to provide either the `image` or the `licence_type` arguments when creating a volume. A `licence_type` is required, but if `image` is supplied, it is already set and cannot be changed. Either the `image_password` or `ssh_keys` arguments need to be supplied when creating a volume using one of the official ProfitBricks images. Only official ProfitBricks provided images support the `ssh_keys` and `image_password` arguments.

---

#### Update a Volume

You can update various attributes of an existing volume; however, some restrictions are in place:

You can increase the size of an existing storage volume. You cannot reduce the size of an existing storage volume. The volume size will be increased without requiring a reboot if the relevant hot plug settings (`disc_virtio_hot_plug`, `disc_virtio_hot_unplug`, etc.) have been set to *true*. The additional capacity is not added automatically added to any partition, therefore you will need to handle that inside the OS afterwards. Once you have increased the volume size you cannot decrease the volume size.

Since an existing volume is being modified, none of the request arguments are specifically required as long as the changes being made satisfy the requirements for creating a volume.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| volume_id | **yes** | string | The ID of the volume. |
| name | no | string | The name of the volume. |
| size | no | int | The size of the volume in GB. You may only increase the `size` when updating. |
| bus | no | string | The bus type of the volume (VIRTIO or IDE). Default: VIRTIO. |
| licence_type | no | string | The licence type of the volume. Options: LINUX, WINDOWS, WINDOWS2016, UNKNOWN, OTHER. You may get an error trying to update `licence_type` depending on the `image` that was used to create the volume. For example, you cannot update the `licence_type` for a volume created from a ProfitBricks supplied OS image. |

**Note**: Trying to change the `image`, `type`, or `availability_zone` in an update request will result in an error.

Pass the arguments to `update_volume`:

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

Pass the arguments to `delete_volume`:

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

Pass the arguments to `create_snapshot`:

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

Pass the arguments to `restore_snapshot`:

    response = client.restore_snapshot(
        datacenter_id='UUID',
        volume_id='UUID',
        snapshot_id='UUID')

---

## Snapshots

#### List Snapshots

You can retrieve a list of all available snapshots.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `list_snapshots`:

    response = client.list_snapshots()

---

#### Get a Snapshot

Retrieves the attributes of a specific snapshot.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| snapshot_id | **yes** | string | The ID of the snapshot. |

Pass the arguments to `get_snapshot`:

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
| licence_type | no | string | The snapshot's licence type: LINUX, WINDOWS, WINDOWS2016, UNKNOWN or OTHER. |
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

Pass the arguments to `update_snapshot`:

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

Pass the arguments to `delete_snapshot`:

    response = client.delete_snapshot(snapshot_id='deleting_snapshot_id')

---

## IP Blocks

The IP block operations assist with managing reserved /static public IP addresses.

#### List IP Blocks

Retrieve a list of available IP blocks.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `list_ipblocks`:

    response = client.list_ipblocks()

---

#### Get an IP Block

Retrieves the attributes of a specific IP block.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| ipblock_id | **yes** | string | The ID of the IP block. |

Pass the arguments to `get_ipblock`:

    response = client.get_ipblock('UUID')

---

#### Create an IP Block

Creates an IP block. Creating an IP block is a bit different than some of the other available create operations. IP blocks are not attached to a particular VDC, but rather to a location. Therefore, you must specify a valid `location` along with a `size` argument indicating the number of IP addresses you want to reserve in the IP block. Any resources using an IP address from an IP block must be in the same `location`.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| ipblock | **yes** | object | An [IPBlock object](#ipblock-resource-object) you wish to create. |

To create an IP block, define the `IPBlock` resource object:

    ipblock = IPBlock(
        name='IP Block Name',
        size=4,
        location='de/fkb')

Pass it to `reserve_ipblock`:

    response = client.reserve_ipblock(ipblock)

#### IPBlock Resource Object

| Name | Required | Type | Description |
|---|:-:|---|---|
| location | **yes** | string | This must be one of the locations: us/las, us/ewr, de/fra, de/fkb. |
| size | **yes** | int | The size of the IP block you want. |
| name | no | string | A descriptive name for the IP block |

The following table outlines the locations currently supported:

| Value| Country | City |
|---|---|---|
| us/las | United States | Las Vegas |
| us/ewr | United States | Newark |
| de/fra | Germany | Frankfurt |
| de/fkb | Germany | Karlsruhe |

---

#### Delete an IP Block

Deletes the specified IP Block.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| ipblock_id | **yes** | string | The ID of the IP block. |

Pass the arguments to `delete_ipblock`:

    response = client.delete_ipblock('UUID')

---

## LANs

#### List LANs

Retrieve a list of LANs within the VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `list_lans`:

    response = client.list_lans(datacenter_id='UUID')

---

#### Create a LAN

Creates a LAN within a VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan | **yes** | object | A [LAN object](#lan-resource-object) describing the LAN to create. |

Create the `LAN` resource object:

    lan = LAN(
        name='LAN Name',
        public=True)

Pass the object and arguments to `create_lan`:

    response = client.create_lan(
        datacenter_id='UUID',
        lan=lan)

#### LAN Resource Object

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | no | string | The name of your LAN. |
| public | **Yes** | bool | Boolean indicating if the LAN faces the public Internet or not. |
| nics | no | list | One or more NIC IDs attached to the LAN. |

---

#### Get a LAN

Retrieves the attributes of a given LAN.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | int | The ID of the LAN. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. See the [Depth](#depth) section. |

Pass the arguments to `get_lan`:

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
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. See the [Depth](#depth) section. |

Pass the arguments to `get_lan_members`:

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
| ip_failover | no | list | A list of IP fail-over dicts. |

Pass the arguments to `update_lan`:

    ip_failover = dict()
    ip_failover['ip'] = 'IP_address'
    ip_failover['nicUuid'] = 'UUID'

    response = client.update_lan(
        datacenter_id='UUID',
        lan_id=ID,
        name='New LAN Name',
        public=True,
        ip_failover=[ip_failover])

---

#### Delete a LAN

Deletes the specified LAN.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| lan_id | **yes** | string | The ID of the LAN. |

Pass the arguments to `delete_lan`:

    response = client.delete_lan(
        datacenter_id='datacenter_id',
        lan_id=ID)

---

## Network Interfaces (NICs)

#### List NICs

Retrieve a list of LANs within the VDC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. See the [Depth](#depth) section. |

Pass the arguments to `list_nics`:

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
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `get_nic`:

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
| nic | **yes** | object | A [NIC object](#nic-resource-object) describing the NIC to be created. |

Create the `NIC` resource object:

    nic = NIC(
        name='NIC Name',
        dhcp=True,
        lan=1,
        nat=False)

Pass the object and arguments to `create_nic`:

    response = client.create_nic(
        datacenter_id='UUID',
        server_id='UUID',
        nic=nic)

#### NIC Resource Object

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | no | string | The name of the NIC. |
| ips | no | list | IP addresses assigned to the NIC. |
| dhcp | no | bool | Set to *false* if you wish to disable DHCP on the NIC. Default: *true*. |
| lan | **yes** | int | The LAN ID the NIC will sit on. If the LAN ID does not exist it will be created. |
| nat | no | bool | Indicates the private IP address has outbound access to the public internet. |
| firewall_active | no | bool | Set this to *true* to enable the ProfitBricks firewall, *false* to disable. |
| firewall_rules | no | list | A list of [FirewallRule objects](#firewall-rule-resource-object) to be created with the NIC. |

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

Pass the arguments to `update_nic`:

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

Pass the arguments to `delete_nic`:

    response = client.delete_nic(
        datacenter_id='UUID',
        server_id='UUID',
        nic_id='UUID')

---

## Firewall Rules

#### List Firewall Rules

Retrieves a list of firewall rules associated with a particular NIC.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `get_firewall_rules`:

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

Pass the arguments to `get_firewall_rule`:

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
| firewall_rule | **yes** | object | A [FirewallRule object](#firewall-rule-resource-object) describing the firewall rule to be created. |

Create the `FirewallRule` resource object:

    fwrule = FirewallRule(
        name='Allow SSH',
        protocol='TCP',
        source_mac='01:23:45:67:89:00',
        port_range_start=22,
        port_range_end=22)

Pass the object and arguments to `create_firewall_rule`:

    response = client.create_firewall_rule(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID',
        firewall_rule=fwrule)

#### Firewall Rule Resource Object

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | no | string | The name of the firewall rule. |
| protocol | **yes** | string | The protocol for the rule: TCP, UDP, ICMP, ANY. |
| source_mac | no | string | Only traffic originating from the respective MAC address is allowed. Valid format: aa:bb:cc:dd:ee:ff. A *null* value allows all source MAC address. |
| source_ip | no | string | Only traffic originating from the respective IPv4 address is allowed. A *null* value allows all source IPs. |
| target_ip | no | string | In case the target NIC has multiple IP addresses, only traffic directed to the respective IP address of the NIC is allowed. A *null* value allows all target IPs. |
| port_range_start | no | string | Defines the start range of the allowed port (from 1 to 65534) if protocol TCP or UDP is chosen. Leave `port_range_start` and `port_range_end` value as *null* to allow all ports. |
| port_range_end | no | string | Defines the end range of the allowed port (from 1 to 65534) if the protocol TCP or UDP is chosen. Leave `port_range_start` and `port_range_end` value as *null* to allow all ports. |
| icmp_type | no | string | Defines the allowed type (from 0 to 254) if the protocol ICMP is chosen. A *null* value allows all types. |
| icmp_code | no | string | Defines the allowed code (from 0 to 254) if protocol ICMP is chosen. A *null* value allows all codes. |

---

#### Update a Firewall Rule

Perform updates to an existing firewall rule. You will notice that some arguments, such as `protocol` cannot be updated. If the `protocol` needs to be changed, you can [delete](#delete-a-firewall-rule) the firewall rule and then [create](#create-a-firewall-rule) new one to replace it.

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

Pass the arguments to `update_firewall_rule`:

    response = client.update_firewall_rule(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID',
        firewall_rule_id='UUID',
        name="Updated Name")

---

#### Delete a Firewall Rule

Removes a firewall rule.

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| server_id | **yes** | string | The ID of the server. |
| nic_id | **yes** | string | The ID of the NIC. |
| firewall_rule_id | **yes** | string | The ID of the firewall rule. |

Pass the arguments to `delete_firewall_rule`:

    response = client.delete_firewall_rule(
        datacenter_id='UUID',
        server_id='UUID',
        nic_id='UUID',
        firewall_rule_id='UUID')

---

## Load Balancers

#### List Load Balancers

Retrieve a list of load balancers within the data center.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `list_loadbalancers`:

    response = client.list_loadbalancers(datacenter_id='UUID')

---

#### Get a Load Balancer

Retrieves the attributes of a given load balancer.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| datacenter_id | **yes** | string | The ID of the VDC. |
| loadbalancer_id | **yes** | string | The ID of the load balancer. |

Pass the arguments to `get_loadbalancer`:

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
| loadbalancer | **yes** | object | A [LoadBalancer object](#load-balancer-resource-object) describing the load balancer to be created. |

Create the `LoadBalancer` resource object:

    loadbalancer = LoadBalancer(
        name='Load Balancer Name',
        dhcp=True)

Pass the object and arguments to `create_loadbalancer`:

    response = client.create_loadbalancer(
        datacenter_id='UUID',
        loadbalancer=loadbalancer)

#### Load Balancer Resource Object

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | **yes** | string | The name of the load balancer. |
| ip | no | string | IPv4 address of the load balancer. All attached NICs will inherit this IP. |
| dhcp | no | bool | Indicates if the load balancer will reserve an IP using DHCP. |
| balancednics | no | list | List of NIC IDs taking part in load-balancing. All balanced NICs inherit the IP of the load balancer. |

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

Pass the arguments to `update_loadbalancer`:

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

Pass the arguments to `delete_loadbalancer`:

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
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `get_loadbalancer_members`:

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
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `get_loadbalanced_nic`:

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

Pass the arguments to `add_loadbalanced_nics`:

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
| nic_id | **yes** | string | The ID of the NIC you are removing from the load balancer. |

Pass the arguments to `remove_loadbalanced_nic`:

    response = client.remove_loadbalanced_nic(
        datacenter_id='UUID',
        loadbalancer_id='UUID',
        nic_id='UUID')

---

## User Management

#### List Groups

Retrieves a list of all groups.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_groups()

---

#### Get a Group

Retrieves the attributes of a given group.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_group(group_id='UUID')

---

#### Create a Group

Creates a new group and set group privileges.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | **yes** | string | The ID of the group. |
| create_datacenter | no | bool | Indicates if the group is allowed to create virtual data centers. |
| create_snapshot | no | bool | Indicates if the group is allowed to create snapshots. |
| reserve_ip | no | bool | Indicates if the group is allowed to reserve IP addresses. |
| access_activity_log | no | bool | Indicates if the group is allowed to access activity log. |

    group = Group(
        name='my-group',
        create_datacenter=True,
        create_snapshot=False,
        reserve_ip=True,
        access_activity_log=False)

    response = client.create_group(group)

---

#### Update a Group

Updates a group's name or privileges.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| name | **yes** | string | The ID of the group. |
| create_datacenter | no | bool | Indicates if the group is allowed to create virtual data centers. |
| create_snapshot | no | bool | Indicates if the group is allowed to create snapshots. |
| reserve_ip | no | bool | Indicates if the group is allowed to reserve IP addresses. |
| access_activity_log | no | bool | Indicates if the group is allowed to access activity log. |

    response = client.update_group(
        group_id='UUID',
        name='my-group',
        create_datacenter=False,
        create_snapshot=True,
        reserve_ip=False,
        access_activity_log=True)

---

#### Delete a Group

Deletes the specified group.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |

    response = client.delete_group(group_id='UUID')

---

#### List Shares

Retrieves a list of all shares though a group.

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_shares(group_id='UUID')

---

#### Get a Share

Retrieves a specific resource share available to a group.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| resource_id | **yes** | string | The ID of the resource. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_share(
        group_id='UUID',
        resource_id='UUID')

---

#### Add a Share

Shares a resource through a group.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| resource_id | **yes** | string | The ID of the resource. |
| edit_privilege | no | string | Indicates that the group has permission to edit privileges on the resource. |
| share_privilege | no | string | Indicates that the group has permission to share the resource. |

    response = client.add_share(
        group_id='UUID',
        resource_id='UUID',
        edit_privilege=True,
        share_privilege=True)

---

#### Update a Share

Updates the permissions of a group for a resource share.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| resource_id | **yes** | string | The ID of the resource. |
| edit_privilege | no | string | Indicates that the group has permission to edit privileges on the resource. |
| share_privilege | no | string | Indicates that the group has permission to share the resource. |

    response = client.update_share(
        group_id='UUID',
        resource_id='UUID',
        edit_privilege=True,
        share_privilege=True)

---

#### Delete a Share

Removes a resource share from a group.

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| resource_id | **yes** | string | The ID of the resource. |

    response = client.delete_share(
        group_id='UUID',
        resource_id='UUID')

---

#### List Users

Retrieves a list of all users.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_users()

---

#### Get a User

Retrieves a single user.

| Name | Required | Type | Description |
|---|:-:|---|---|
| user_id | **yes** | string | The ID of the user. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_user(user_id='UUID')

---

#### Create a User

Creates a new user.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| firstname | **yes** | string | A name for the user. |
| lastname | **yes**  | bool | A name for the user. |
| email | **yes**  | bool | An e-mail address for the user. |
| password | **yes**  | bool | A password for the user. |
| administrator | no | bool | Assigns the user have administrative rights. |
| force_sec_auth | no | bool | Indicates if secure (two-factor) authentication should be forced for the user. |

    user = User(
        firstname='John',
        lastname='Doe',
        email='no-reply@example.com',
        password='secretpassword123',
        administrator=True,
        force_sec_auth=False)

    response = client.create_user(user)

---

#### Update a User

Updates an existing user.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| user_id | **yes** | string | The ID of the user. |
| firstname | **yes** | string | A name for the user. |
| lastname | **yes**  | bool | A name for the user. |
| email | **yes**  | bool | An e-mail address for the user. |
| administrator | **yes** | bool | Assigns the user have administrative rights. |
| force_sec_auth | **yes** | bool | Indicates if secure (two-factor) authentication should be forced for the user. |

    response = client.update_user(
        user_id='UUID',
        firstname='John',
        lastname='Doe',
        email='no-reply@example.com',
        administrator=True,
        force_sec_auth=False)

---

#### Delete a User

Removes a user.

| Name | Required | Type | Description |
|---|:-:|---|---|
| user_id | **yes** | string | The ID of the user. |

    response = client.delete_user(user_id='UUID')

---

#### List Users in a Group

Retrieves a list of all users that are members of a particular group.

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_group_users(group_id='UUID')

---

#### Add User to Group

Adds an existing user to a group.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| user_id | **yes** | string | The ID of the user. |

    response = client.add_group_user(
        group_id='UUID',
        user_id='UUID')

---

#### Remove User from a Group

Removes a user from a group.

| Name | Required | Type | Description |
|---|:-:|---|---|
| group_id | **yes** | string | The ID of the group. |
| user_id | **yes** | string | The ID of the user. |

    response = client.remove_group_user(
        group_id='UUID',
        user_id='UUID')

---

#### List Resources

Retrieves a list of all resources. Alternatively, Retrieves all resources of a particular type.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| resource_type | no | string | The resource type: `datacenter`, `image`, `snapshot` or `ipblock`. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_resources()

    response = client.list_resources(resource_type='snapshot')

---

#### Get a Resource

Retrieves a single resource of a particular type.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| resource_type | **yes** | string | The resource type: `datacenter`, `image`, `snapshot` or `ipblock`. |
| resource_id | **yes** | string | The ID of the resource. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.get_resource(resource_id='UUID')

    response = client.get_resource(
        resource_type='datacenter',
        resource_id='UUID')

---

## Contract Resources

#### List Contract Resources

Retrieves information about the resource limits for a particular contract and the current resource usage.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned. |

    response = client.list_contracts()

---

## Requests

Each call to the ProfitBricks Cloud API is assigned a request ID. These operations can be used to get information about the requests that have been submitted and their current status.

#### List Requests

Retrieve a list of requests.

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

Pass the arguments to `list_requests`:

    response = client.list_requests()

---

#### Get a Request

Retrieves the attributes of a specific request. This operation shares the same `get_request` method used for getting request status, however the response it determined by the boolean value you pass for *status*. To get details about the request itself, you want to pass a *status* of *False*.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| request_id | **yes** | string | The ID of the request. |
| status | **yes** | bool | Set to *False* to have the request details returned. |

Pass the arguments to `get_request`:

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
| status | **yes** | bool | Set to *True* to have the status of the request returned. |

Pass the arguments to `get_request`:

    response = client.get_request(
        request_id='UUID',
        status=True)

---

## Kubernetes

#### List Kubernetes Clusters

Retrieve the list of Kubernetes clusters.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

    response = client.list_k8s_clusters()

---

#### Create a Kubernetes Cluster

This will create a new Kubernetes Cluster.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| name | **yes** | string | The Kubernetes Cluster Name. |

Create the Kubernetes Cluster:

```python
my_cluster = client.create_k8s_cluster(cluster_name)
```

Wait for the cluster to be active:

```python
client.wait_for(
  fn_request=lambda: client.list_k8s_clusters(),
  fn_check=lambda r: list(filter(
      lambda e: e['properties']['name'] == cluster_name,
      r['items']
    ))[0]['metadata']['state'] == 'ACTIVE',
  console_print='.',
  scaleup=10000
)
```

---

#### Retrieve a Kubernetes Cluster

This will retrieve a Kubernetes Cluster.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| k8s_cluster_id | **yes** | string | The ID of the Kubernetes Cluster. |

Retrieve the Kubernetes Cluster:

```python
client.get_k8s_cluster(my_cluster['id'])
```

---

#### Delete a Kubernetes Cluster

This will delete a Kubernetes Cluster.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| k8s_cluster_id | **yes** | string | The ID of the Kubernetes Cluster. |

Delete the Kubernetes Cluster:

```python
client.delete_k8s_cluster(my_cluster['id'])
```

---

#### Retrieve a Kubernetes Cluster KubeConfig

This will retrieve the KubeConfig for a Kubernetes Cluster.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| k8s_cluster_id | **yes** | string | The ID of the Kubernetes Cluster. |

Retrieve the Kubeconfig for a Kubernetes Cluster:

```python
client.get_k8s_config(my_cluster['id'])
```

---

#### List Kubernetes NodePools

Retrieve the list of nodepools for a Kubernetes cluster.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| k8s_cluster_id | **yes** | string | The ID of the Kubernetes Cluster. |
| depth | no | int | An integer value of 0 - 5 that affects the amount of detail returned.  See the [Depth](#depth) section. |

    response = client.list_k8s_cluster_nodepools(k8s_cluster_id)

---

#### Create a NodePool for a Kubernetes Cluster

This will create a new NodePool for a Kubernetes Cluster.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| k8s_cluster_id | **yes** | string | The ID of the Kubernetes Cluster |
| name | **yes** | string | The NodePool Name |
| datacenter_id | **yes** | string | The ID of the Datacenter to place the NodePool in |
| node_count | **yes** | int |  Number of nodes part of the Node Pool |
| cpu_family | **yes** | string | A valid cpu family name |
| cores_count | **yes** | int | Number of cores for node |
| ram_size | **yes** | int | RAM size for node, minimum size 2048MB is recommended |
| availability_zone | **yes** | string | The availability zone in which the server should exist |
| storage_type | **yes** | string | Hardware type of the volume |
| storage_size | **yes** | int | The size of the volume in GB. The size should be greater than 10GB |

Create the NodePool:

```python
my_nodepool = client.create_k8s_cluster_nodepool(
  my_cluster['id'],
  name='my_demo_pool_name',
  datacenter_id=datacenter_id,
  node_count=4,
  cpu_family='AMD_OPTERON',
  cores_count=2,
  ram_size=4096,
  availability_zone='AUTO',
  storage_type='SSD',
  storage_size=100
)
```

Wait for the nodepool to be active:

```python
client.wait_for(
  fn_request=lambda: client.list_k8s_cluster_nodepools(my_cluster['id']),
  fn_check=lambda r: list(filter(
      lambda e: e['properties']['name'] == pool_name,
      r['items']
    ))[0]['metadata']['state'] == 'ACTIVE',
  console_print='.',
  scaleup=10000
)
```

---

#### Retrieve a NodePool

This will retrieve a NodePool.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| k8s_cluster_id | **yes** | string | The ID of the Kubernetes Cluster. |
| nodepool_id | **yes** | string | The ID of the NodePool. |

Retrieve the NodePool:

```python
client.get_k8s_cluster_nodepool(my_cluster['id'], my_nodepool['id'])
```

---

#### Delete a NodePool

This will delete a NodePool.

The following table describes the request arguments:

| Name | Required | Type | Description |
|---|:-:|---|---|
| k8s_cluster_id | **yes** | string | The ID of the Kubernetes Cluster. |
| nodepool_id | **yes** | string | The ID of the NodePool. |

Delete the NodePool:

```python
client.delete_k8s_cluster_nodepool(my_cluster['id'], my_nodepool['id'])
```

---

## Examples

Below are some examples using the SDK for Python. These examples will assume credentials are being set with environment variables:

    export PROFITBRICKS_USERNAME=username
    export PROFITBRICKS_PASSWORD=password

#### List All Data Centers

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

#### Search for Images

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

#### Reserve an IP Block

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

#### Wait for Resources

The remaining examples will require dependent resources. A volume cannot be attached to a server before the server and volume are finished provisioning. Therefore, we require the `wait_for_completion` method that will stop and wait for the server and volume to finish provisioning before attaching the volume to the server.

#### Component Build

ProfitBricks allows servers to be built by their individual components. That is, by connecting customized components such as servers, volumes, and NICs together. For example, a server can be provisioned in one request followed by one or more NICs and volumes in following requests. The volumes can then be attached separately to the server.

It is important to note that you will need to wait for each individual component to finish provisioning before it can be used in subsequent operations. This behavior is demonstrated below.

    #!/usr/bin/python

    import json
    import os

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
    client.wait_for_completion(response, timeout)
    datacenter_id = response['id']

    # Create public LAN
    lan = LAN(name="Public LAN", public=True)

    response = client.create_lan(datacenter_id, lan=lan)
    client.wait_for_completion(response, timeout)
    lan_id = response['id']

    # Create server
    server = Server(
        name='Python SDK Server',
        ram=4096,
        cores=4,
        cpu_family='INTEL_XEON')

    response = client.create_server(datacenter_id=datacenter_id, server=server)
    client.wait_for_completion(response, timeout)
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
    client.wait_for_completion(response, timeout)
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
    client.wait_for_completion(response, timeout)

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
    client.wait_for_completion(response, timeout)
    volume1_id = response['id']

    # Attach system volume
    response = client.attach_volume(
        datacenter_id=datacenter_id,
        server_id=server_id,
        volume_id=volume1_id)
    client.wait_for_completion(response, timeout)

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
    client.wait_for_completion(response, timeout)
    volume2_id = response['id']

    # Attach data volume
    response = client.attach_volume(
        datacenter_id=datacenter_id,
        server_id=server_id,
        volume_id=volume2_id)
    client.wait_for_completion(response, timeout)

    live_datacenter = client.get_datacenter(datacenter_id=datacenter_id, depth=5)
    print json.dumps(live_datacenter, indent=4)

#### Composite Build

The ProfitBricks platform also allows fully operational servers to be provisioned with a single request. This is accomplished by nesting related resources.

Multiple servers, volumes, LANs, and load balancers can be nested under a data center, multiple NICs and volumes can be nested under servers, and firewall rules under NICs.

This example will demonstrate composite resources.

    #!/usr/bin/python

    import json
    import os

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
    client.wait_for_completion(response)

    datacenter_id = response['id']

    # Set the first LAN to public
    response = client.update_lan(
        datacenter_id=datacenter_id,
        lan_id=1,
        name='Public LAN',
        public=True)

    client.wait_for_completion(response)

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
