#!/usr/local/bin/python
# encoding: utf-8
'''
pb_datacenter_inventory -- dump inventory of your Profitbricks data centers to CSV files

pb_datacenter_inventory is a sample script to get an inventory overview
of your data centers via Profitbricks REST-API.

It collects some basic information on
- reserved ip blocks:
    Location,RscType,RscID,State,Size,IP addresses
- images and snapshots
    Visibility(public|private),Location,RscType,SubType(CDROM|HDD),RscID,
    RscName,State,LicType,Size,Created,Modified
- servers
    DCID,DCName,Location,RscType,RscID,RscName,State,LicType,Cores,RAM,
    # NICs,# Volumes,(Total) Storage,---,Created,Modified
  and storage
    DCID,DCName,Location,RscType,RscID,RscName,State,LicType,---,---,---,---,
    (Total) Storage,Connected to,Created,Modified
- networking infrastructure (LANs/NICs)
    DCID,DCName,Location,LAN ID,LAN name,public?,State,# NICs,NIC ID,
    MAC address,DHCP?,IP(s),NIC name,Firewall?,Connected to,ID,Name
from all your datacenters.

This data is written to a resource specific CSV file which can be used
for reports or automatic post processing.


@author:     Jürgen Buchhammer

@copyright:  2016 ProfitBricks GmbH. All rights reserved.

@license:    license

@contact:    juergen.buchhammer@profitbricks.com
@deffield    updated: Updated
'''

import sys
import os
import traceback
import re
import pprint

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from getpass import getpass

import csv

from profitbricks.client import ProfitBricksService

__all__ = []
__version__ = 0.2
__date__ = '2016-01-15'
__updated__ = '2016-01-15'

verbose = 0
DEBUG = 1


def pp(value):
    """
    Returns a pretty print string of the given value.

    @return: pretty print string
    @rtype: str
    """

    pretty_printer = pprint.PrettyPrinter(indent=4)
    return pretty_printer.pformat(value)


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def get_dc_inventory(pbclient, dc=None):
    ''' gets inventory of one data center'''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc is None:
        raise ValueError("argument 'dc' must not be None")
    dc_inv = []   # inventory list to return
    dcid = dc['id']
    # dc_data contains dc specific columns
    dc_data = [dcid, dc['properties']['name'], dc['properties']['location']]
    # first get the servers
    # this will build a hash to relate volumes to servers later
    # depth 3 is enough to get into volume/nic level plus details
    servers = pbclient.list_servers(dcid, 3)
    print("found %i servers in data center %s" % (len(servers['items']), dc['properties']['name']))
    if verbose > 2:
        print(str(servers))
    # this will build a hash to relate volumes to servers later
    bound_vols = dict()   # hash volume-to-server relations
    for server in servers['items']:
        if verbose > 2:
            print("SERVER: %s" % str(server))
        serverid = server['id']
        # server_data contains server specific columns for later output
        server_data = [
            server['type'], serverid, server['properties']['name'],
            server['metadata']['state']
        ]
        # OS is determined by boot device (volume||cdrom), not a server property.
        # Might even be unspecified
        bootOS = "NONE"
        bootdev = server['properties']['bootVolume']
        if bootdev is None:
            bootdev = server['properties']['bootCdrom']
            print("server %s has boot device %s" % (serverid, "CDROM"))
        if bootdev is None:
            print("server %s has NO boot device" % (serverid))
        else:
            bootOS = bootdev['properties']['licenceType']
        server_data += [bootOS, server['properties']['cores'], server['properties']['ram']]
        server_vols = server['entities']['volumes']['items']
        n_volumes = len(server_vols)
        total_disk = 0
        licence_type = ""
        for vol in server_vols:
            total_disk += vol['properties']['size']
            licence_type = str(vol['properties']['licenceType'])
            bound_vols[vol['id']] = serverid
            if verbose:
                print("volume %s is connected to %s w/ OS %s" % (
                    vol['id'], bound_vols[vol['id']], licence_type))
        server_nics = server['entities']['nics']['items']
        n_nics = len(server_nics)
        server_data += [
            n_nics, n_volumes, total_disk, "",
            server['metadata']['createdDate'], server['metadata']['lastModifiedDate']
        ]
        dc_inv.append(dc_data + server_data)
    # end for(servers)

    # and now the volumes...
    volumes = pbclient.list_volumes(dcid, 2)   # depth 2 gives max. details
    for volume in volumes['items']:
        if verbose > 2:
            print("VOLUME: %s" % str(volume))
        volid = volume['id']
        vol_data = [
            volume['type'], volid, volume['properties']['name'], volume['metadata']['state'],
            volume['properties']['licenceType'], "", "", "", "", volume['properties']['size']
        ]
        connect = 'NONE'
        if volid in bound_vols:
            connect = bound_vols[volid]
        vol_data += [
            connect, volume['metadata']['createdDate'], volume['metadata']['lastModifiedDate']
        ]
        dc_inv.append(dc_data + vol_data)
    # end for(volumes)
    return dc_inv
# end get_dc_inventory()


def get_images(pbclient):
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    print("getting images..")
    images = pbclient.list_images()
    print("found %i images" % len(images['items']))
    img_inv = []
    for image in images['items']:
        if verbose > 2:
            print("IMAGE: %s" % str(image))
        img_data = [
            ('public' if image['properties']['public'] else 'private'),
            image['properties']['location'], image['type'],
            image['properties']['imageType'], image['id'], image['properties']['name'],
            image['metadata']['state'], image['properties']['licenceType'],
            image['properties']['size'],
            image['metadata']['createdDate'], image['metadata']['lastModifiedDate']
        ]
        img_inv.append(img_data)
    return img_inv
# end get_images()


def get_snapshots(pbclient):
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    print("getting snapshots..")
    snapshots = pbclient.list_snapshots()
    print("found %i snapshots" % len(snapshots['items']))
    snap_inv = []
    for snap in snapshots['items']:
        if verbose > 2:
            print("SNAPSHOT: %s" % str(snap))
        snap_data = [
            "private", snap['properties']['location'],
            snap['type'], "HDD", snap['id'], snap['properties']['name'],
            snap['metadata']['state'], snap['properties']['licenceType'],
            snap['properties']['size'],
            snap['metadata']['createdDate'], snap['metadata']['lastModifiedDate']
        ]
        # print("SNAPSHOT: %s" % str(snap_data))
        snap_inv.append(snap_data)
    # end for(snapshots)
    return snap_inv
# end get_snapshots()


def get_ipblocks(pbclient):
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    print("getting IP blocks..")
    ipblocks = pbclient.list_ipblocks()
    print("found %i IP blocks" % len(ipblocks['items']))
    ip_inv = []
    if verbose > 1:
        print(str(ipblocks))
    for block in ipblocks['items']:
        ip_data = [
            block['properties']['location'], block['type'], block['id'],
            block['metadata']['state'], block['properties']['size']
        ]
        ip_data.extend(block['properties']['ips'])
        # print str(ip_data)
        ip_inv.append(ip_data)
    # end for(ipblocks)
    return ip_inv
# end get_ipblocks()


def get_dc_network(pbclient, dc=None):
    ''' gets inventory of one data center'''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc is None:
        raise ValueError("argument 'dc' must not be None")
    print("getting networks..")
    dcid = dc['id']
    # dc_data contains dc specific columns
    dc_data = [dcid, dc['properties']['name'], dc['properties']['location']]
    lbs = pbclient.list_loadbalancers(dcid, 2)
    # build lookup hash for loadbalancer's ID->name
    lbnames = dict([(lb['id'], lb['properties']['name']) for lb in lbs['items']])
    if verbose > 2:
        print("LBs: %s" % (str(lbs)))
    lans = pbclient.list_lans(dcid, 3)
    lan_inv = []
    # lookup hash for server's ID->name
    servernames = dict()
    for lan in lans['items']:
        if verbose > 1:
            print("LAN: %s" % str(lan))
        lan_data = dc_data + [
            "LAN "+lan['id'], lan['properties']['name'], lan['properties']['public'],
            lan['metadata']['state']
        ]
        nics = lan['entities']['nics']['items']
        lan_data.append(len(nics))
        if len(nics) > 0:
            for nic in nics:
                nic_props = nic['properties']
                # get the serverid of this nic by href
                # !!! HUUUUH this might also be a loadbalancer ID,
                # although it's '/servers/<id>/...' !!!
                serverid = re.sub(r'^.*servers/([^/]+)/nics.*', r'\1', nic['href'])
                if serverid in lbnames:
                    servertype = "LB"
                    servername = lbnames[serverid]
                    print("server entry for %s is LOADBALANCER %s" % (serverid, servername))
                else:
                    servertype = "Server"
                    if serverid not in servernames:
                        if verbose:
                            print("add server entry for %s" % serverid)
                        server = pbclient.get_server(dcid, serverid, 0)
                        servernames[serverid] = server['properties']['name']
                    servername = servernames[serverid]
                # end if/else(serverid)
                ips = [str(ip) for ip in nic_props['ips']]
                nic_data = [
                    nic['id'], nic_props['mac'], nic_props['dhcp'], ips, nic_props['name'],
                    nic_props['firewallActive'], servertype, serverid, servername
                ]
                lan_inv.append(lan_data+nic_data)
            # end for(nics)
        else:
            lan_inv.append(lan_data)
    # end for(lans)
    return lan_inv
# end get_networks()


def get_requests(pbclient):
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    print("getting requests..")
    requests = pbclient.list_requests()   # higher depth gives no more details (API-doc BUG)
    print("found %i requests" % len(requests['items']))
    if verbose:
        print("global: %s" % str(requests))
    for req in requests['items']:
        reqid = req['id']
        # False: get request (w/ body), True: get request status (DONE,..)
        req_data = pbclient.get_request(reqid)
        # False: get request (w/ body), True: get request status (DONE,..)
        req_stat = pbclient.get_request(reqid, True)
        if verbose > 2:
            print("REQ: %s\n     %s" % (str(req_data), str(req_stat)))
        if verbose > 1:
            print(
                "request %s|%s|%s" % (
                    str(reqid), str(req_data['metadata']), str(req_stat['metadata'])
                )
            )
    # end for(requests)
# end get_requests()


def main(argv=None):                # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by J.Buchhammer on %s.
  Copyright 2016 ProfitBricks GmbH. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            '-u', '--user', dest='user', required=True, help='the login name')
        parser.add_argument(
            '-p', '--password', dest='password', help='the login password')
        parser.add_argument(
            '-d', '--datacenter', '--datacenterid', dest='datacenterid', nargs='?', const='*',
            help='show server/storage of datacenter(s)')
        parser.add_argument(
            '-i', '--image', dest='show_images', action="store_true",
            help='show images and snapshots')
        parser.add_argument(
            '-b', '--ipblock', dest='show_ipblocks', action="store_true",
            help='show reserved IP blocks')
        parser.add_argument(
            '-n', '--network', dest='show_networks', action="store_true",
            help='show network assignments')
#        parser.add_argument(
#            '-r', '--request', dest='show_requests', action="store_true",
#            help='show requests')
        parser.add_argument(
            "-v", "--verbose", dest="verbose", action="count", default=0,
            help="set verbosity level [default: %(default)s]")
        parser.add_argument(
            '-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        global verbose
        verbose = args.verbose   # this is a global to be used in methods
        user = args.user
        password = args.password
        datacenterid = args.datacenterid

        print("Welcome to PB-API %s\n" % user)
        if password is None:
            password = getpass()
        if verbose > 0:
            print("Verbose mode on")
            print("using python ", sys.version_info)

        pbclient = ProfitBricksService(user, password)

        if datacenterid is not None:
            datacenters = {}
            if datacenterid == '*':
                # the default depth=1 is sufficient, higher values don't provide more details
                datacenters = pbclient.list_datacenters()
            else:
                datacenters['items'] = []
                datacenters['items'] = [pbclient.get_datacenter(datacenterid, 1)]
            if verbose > 1:
                print(pp(datacenters))
            print("retrieved %i datacenters " % len(datacenters['items']))

            # dump inventory to file
            with open("pb_datacenter_inventory.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                csvwriter.writerow([
                    'DCID', 'DCName', 'Loc', 'RscType', 'RscID', 'RscName', 'State', 'LicType',
                    'Cores', 'RAM', '# NICs', '# Volumes', '(Total) Storage', 'Connected to',
                    'Created', 'Modified'
                ])
                for dc in datacenters['items']:
                    try:
                        dc_inv = get_dc_inventory(pbclient, dc)
                        if verbose:
                            print("DC %s has %i inventory entries" % (dc['id'], len(dc_inv)))
                        for row in dc_inv:
                            csvwriter.writerow(row)
                    except Exception:
                        traceback.print_exc()
                        exit(2)
                # end for(datacenters)

        if args.show_images:
            with open("pb_datacenter_images.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                csvwriter.writerow([
                    'Visibility', 'Loc', 'RscType', 'SubType', 'RscID', 'RscName',
                    'State', 'LicType', 'Size', 'Created', 'Modified'
                ])
                img_inv = get_images(pbclient)
                for row in img_inv:
                    csvwriter.writerow(row)
                snap_inv = get_snapshots(pbclient)
                for row in snap_inv:
                    csvwriter.writerow(row)

        if args.show_ipblocks:
            with open("pb_datacenter_ipblocks.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                csvwriter.writerow([
                    'Loc', 'RscType', 'RscID', 'State', 'Size', 'IP addresses'])
                ipblocks = get_ipblocks(pbclient)
                for row in ipblocks:
                    csvwriter.writerow(row)

        # file is automatically closed after with block
        if args.show_networks:
            # the default depth=1 is sufficient, higher values don't provide more details
            datacenters = pbclient.list_datacenters()
            print("retrieved %i datacenters " % len(datacenters['items']))
            with open("pb_datacenter_networks.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                csvwriter.writerow([
                    'DCID', 'DCName', 'Loc',
                    'LAN ID', 'LAN name', 'public', 'State', '# NICs',
                    'NIC ID', 'MAC address', 'DHCP', 'IP(s)', 'NIC name', 'Firewall',
                    'Connected to', 'ID', 'Name'])

                for dc in datacenters['items']:
                    try:
                        dc_net = get_dc_network(pbclient, dc)
                        if verbose:
                            print("DC %s has %i network entries" % (dc['id'], len(dc_net)))
                        for row in dc_net:
                            csvwriter.writerow(row)
                    except Exception:
                        traceback.print_exc()
                        exit(2)
                # end for(datacenters)

        # just for fun:
#         if args.show_requests:
#             get_requests(pbclient)
        print("%s finished w/o errors" % program_name)
        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
