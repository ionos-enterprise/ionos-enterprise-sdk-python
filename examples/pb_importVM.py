#!/usr/local/bin/python
# encoding: utf-8
'''
pb_importVM -- import a 3rd party VM

pb_importVM is a tool to create a VM that comes from another
virtualization solution.

It reads out the meta data accompanying the disk files and creates
a VM out of it. The disk images must be uploaded already.

@author:     Jürgen Buchhammer

@copyright:  2016 ProfitBricks GmbH. All rights reserved.

@license:    Apache License 2.0

@contact:    juergen.buchhammer@profitbricks.com
@deffield    updated: Updated
'''

import sys
import os
import traceback

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from time import sleep
from base64 import b64decode, b64encode

import xml.etree.ElementTree as ET

from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Volume, Server
from profitbricks.client import LAN, NIC

__all__ = []
__version__ = 0.1
__date__ = '2016-09-30'
__updated__ = '2016-09-30'


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg
# end class CLIError


def getLogin(filename, user, passwd):
    '''
    write user/passwd to login file or get them from file.
    This method is not Py3 safe (byte vs. str)
    '''
    if filename is None:
        return (user, passwd)
    isPy2 = sys.version_info[0] == 2
    if os.path.exists(filename):
        print("Using file {} for Login".format(filename))
        with open(filename, "r") as loginfile:
            encoded_cred = loginfile.read()
            print("encoded: {}".format(encoded_cred))
            if isPy2:
                decoded_cred = b64decode(encoded_cred)
            else:
                decoded_cred = b64decode(encoded_cred).decode('utf-8')
            login = decoded_cred.split(':', 1)
            return (login[0], login[1])
    else:
        if user is None or passwd is None:
            raise ValueError("user and password must not be None")
        print("Writing file {} for Login".format(filename))
        with open(filename, "wb") as loginfile:
            creds = user+":"+passwd
            if isPy2:
                encoded_cred = b64encode(creds)
            else:
                encoded_cred = b64encode(creds.encode('utf-8'))
            print("encoded: {}".format(encoded_cred))
            loginfile.write(encoded_cred)
        return (user, passwd)
# end getLogin()


def wait_for_request(pbclient, request_id,
                     timeout=0, initial_wait=5, scaleup=10):
    '''
    Waits for a request to finish until timeout.
    timeout==0 is interpreted as infinite wait time.
    Returns a tuple (return code, request status, message) where return code
    0  : request successful
    1  : request failed
    -1 : timeout exceeded
    The wait_period is increased every scaleup steps to adjust for long
    running requests.
    '''
    total_wait = 0
    wait_period = initial_wait
    next_scaleup = scaleup * wait_period
    wait = True
    while wait:
        request_status = pbclient.get_request(request_id, status=True)
        state = request_status['metadata']['status']
        if state == "DONE":
            return(0, state, request_status['metadata']['message'])
        if state == 'FAILED':
            return(1, state, request_status['metadata']['message'])
        print("Request '{}' is in state '{}'. Sleeping for {} seconds..."
              .format(request_id, state, wait_period))
        sleep(wait_period)
        total_wait += wait_period
        if timeout != 0 and total_wait > timeout:
            wait = False
        next_scaleup -= wait_period
        if next_scaleup == 0:
            wait_period += initial_wait
            next_scaleup = scaleup * wait_period
            print("scaling up wait_period to {}, next change in {} seconds"
                  .format(wait_period, next_scaleup))
    # end while(wait)
    return(-1, state, "request not finished before timeout")
# end wait_for_request()


def wait_for_requests(pbclient, request_ids=[],
                      timeout=0, initial_wait=5, scaleup=10):
    '''
    Waits for a list of requests to finish until timeout.
    timeout==0 is interpreted as infinite wait time.
    Returns a dict of request_id -> result.
    result is a tuple (return code, request status, message) where return code
    0  : request successful
    1  : request failed
    -1 : timeout exceeded
    The wait_period is increased every scaleup steps to adjust for long
    running requests.
    '''
    done = dict()
    if len(request_ids) == 0:
        print("empty request list")
        return done
    total_wait = 0
    wait_period = initial_wait
    next_scaleup = scaleup * wait_period
    wait = True
    while wait:
        for request_id in request_ids:
            if request_id in done:
                continue
            request_status = pbclient.get_request(request_id, status=True)
            state = request_status['metadata']['status']
            if state == "DONE":
                done[request_id] = (0, state, request_status['metadata']['message'])
                print("Request '{}' is in state '{}'.".format(request_id, state))
            if state == 'FAILED':
                done[request_id] = (1, state, request_status['metadata']['message'])
                print("Request '{}' is in state '{}'.".format(request_id, state))
        # end for(request_ids)
        if len(done) == len(request_ids):
            wait = False
        else:
            print("{} of {} requests are finished. Sleeping for {} seconds..."
                  .format(len(done), len(request_ids), wait_period))
            sleep(wait_period)
            total_wait += wait_period
            if timeout != 0 and total_wait > timeout:
                wait = False
            next_scaleup -= wait_period
            if next_scaleup == 0:
                wait_period += initial_wait
                next_scaleup = scaleup * wait_period
                print("scaling up wait_period to {}, next change in {} seconds"
                      .format(wait_period, next_scaleup))
        # end if/else(done)
    # end while(wait)
    if len(done) != len(request_ids):
        for request_id in request_ids:
            if request_id in done:
                continue
            done[request_id] = (-1, state, "request not finished before timeout")
    return done
# end wait_for_requests()


def get_disk_image_by_name(pbclient, location, image_name):
    """
    Returns all disk images within a location with a given image name.
    The name must match exactly.
    The list may be empty.
    """
    all_images = pbclient.list_images()
    matching = [i for i in all_images['items'] if
                i['properties']['name'] == image_name and
                i['properties']['imageType'] == "HDD" and
                i['properties']['location'] == location]
    return matching
# end get_disk_image_by_name()


# -- OVF parsing --

class OFVData():
    '''OFV meta data - the data is only available after calling OFVData.parse'''
    def __init__(self, file=None):
        '''OVF meta data initializer'''
        # namespaces, dflt is default namespace xmlns, others are xmlns:<ns>
        # @TODO: read these from <Envelope> because version may change
        #        e.g. OVF 2.0 exists: xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/2"
        self._ns = {#'dflt': "http://schemas.dmtf.org/ovf/envelope/1", # same as ovf!?!
                    'cim': "http://schemas.dmtf.org/wbem/wscim/1/common",
                    'ovf': "http://schemas.dmtf.org/ovf/envelope/1",
                    'rasd': "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData",
                    'vmw': "http://www.vmware.com/schema/ovf",
                    'vssd': "http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData"}
        self.file = file
        self.root = None
        self.name = None
        self.osid = None
        self.licenseType = "OTHER"
        self.cpus = None
        self.ram = None
        self.disks = []
        self.lans = dict()
        self.nics = []
        self.resourceTypes = {
                                '1': 'Other',
                                '2': 'Computer System',
                                '3': 'Processor',
                                '4': 'Memory',
                                '5': 'IDE Controller',
                                '6': 'Parallel SCSI HBA',
                                '7': 'FC HBA',
                                '8': 'iSCSI HBA',
                                '9': 'IB HCA',
                                '10': 'Ethernet Adapter',
                                '11': 'Other Network Adapter',
                                '12': 'I/O Slot',
                                '13': 'I/O Device',
                                '14': 'Floppy Drive',
                                '15': 'CD Drive',
                                '16': 'DVD drive',
                                '17': 'Disk Drive',
                                '18': 'Tape Drive',
                                '19': 'Storage Extent',
                                '20': 'Other storage device',
                                '21': 'Serial port',
                                '22': 'Parallel port',
                                '23': 'USB Controller',
                                '24': 'Graphics controller',
                                '25': 'IEEE 1394 Controller',
                                '26': 'Partitionable Unit',
                                '27': 'Base Partitionable Unit',
                                '28': 'Power',
                                '29': 'Cooling Capacity',
                                '30': 'Ethernet Switch Port',
                                '31': 'Logical Disk',
                                '32': 'Storage Volume',
                                '33': 'Ethernet Connection',
                                '..': 'DMTF reserved',
                                '0x8000..0xFFFF': 'Vendor Reserved'
                              }   # end resourceType
        self.osTypeOther = {
                            '0': 'Unknown',
                            '1': 'Other',
                            '2': 'MACOS',
                            '3': 'ATTUNIX',
                            '4': 'DGUX',
                            '5': 'DECNT',
                            '6': 'Tru64 UNIX',
                            '7': 'OpenVMS',
                            '8': 'HPUX',
                            '9': 'AIX',
                            '10': 'MVS',
                            '11': 'OS400',
                            '12': 'OS/2',
                            '13': 'JavaVM',
                            '14': 'MSDOS',
                            '15': 'WIN3x',
                            '16': 'WIN95',
                            '17': 'WIN98',
                            '18': 'WINNT',
                            '19': 'WINCE',
                            '20': 'NCR3000',
                            '21': 'NetWare',
                            '22': 'OSF',
                            '23': 'DC/OS',
                            '24': 'Reliant UNIX',
                            '25': 'SCO UnixWare',
                            '26': 'SCO OpenServer',
                            '27': 'Sequent',
                            '28': 'IRIX',
                            '29': 'Solaris',
                            '30': 'SunOS',
                            '31': 'U6000',
                            '32': 'ASERIES',
                            '33': 'HP NonStop OS',
                            '34': 'HP NonStop OSS',
                            '35': 'BS2000',
                            '37': 'Lynx',
                            '38': 'XENIX',
                            '39': 'VM',
                            '40': 'Interactive UNIX',
                            '41': 'BSDUNIX',
                            '42': 'FreeBSD',
                            '43': 'NetBSD',
                            '44': 'GNU Hurd',
                            '45': 'OS9',
                            '46': 'MACH Kernel',
                            '47': 'Inferno',
                            '48': 'QNX',
                            '49': 'EPOC',
                            '50': 'IxWorks',
                            '51': 'VxWorks',
                            '52': 'MiNT',
                            '53': 'BeOS',
                            '54': 'HP MPE',
                            '55': 'NextStep',
                            '56': 'PalmPilot',
                            '57': 'Rhapsody',
                            '59': 'Dedicated',
                            '60': 'OS/390',
                            '61': 'VSE',
                            '62': 'TPF',
                            '64': 'Caldera Open UNIX',
                            '65': 'OpenBSD',
                            '66': 'Not Applicable',
                            '68': 'z/OS',
                            '78': 'FreeBSD 64-Bit',
                            '81': 'Solaris 64-Bit',
                            '86': 'Novell OES',
                            '87': 'Novell Linux Desktop',
                            '88': 'Sun Java Desktop System',
                            '102': 'Other 64-Bit',
                            '104': 'VMware ESXi',
                            '110': 'eComStation 32-bitx',
                           }   # end osTypeOther
        self.osTypeLinux = {
                            '36': 'LINUX',
                            '79': 'RedHat Enterprise Linux',
                            '80': 'RedHat Enterprise Linux 64-Bit',
                            '82': 'SUSE',
                            '83': 'SUSE 64-Bit',
                            '84': 'SLES',
                            '85': 'SLES 64-Bit',
                            '89': 'Mandriva',
                            '90': 'Mandriva 64-Bit',
                            '91': 'TurboLinux',
                            '92': 'TurboLinux 64-Bit',
                            '93': 'Ubuntu',
                            '94': 'Ubuntu 64-Bit',
                            '95': 'Debian',
                            '96': 'Debian 64-Bit',
                            '97': 'Linux 2.4.x',
                            '98': 'Linux 2.4.x 64-Bit',
                            '99': 'Linux 2.6.x',
                            '100': 'Linux 2.6.x 64-Bit',
                            '101': 'Linux 64-Bit',
                            '106': 'CentOS 32-bit',
                            '107': 'CentOS 64-bit',
                            '108': 'Oracle Linux 32-bit',
                            '109': 'Oracle Linux 64-bit',
                           }   # end osTypeLinux
        self.osTypeWindows = {
                                '58': 'Windows 2000',
                                '63': 'Windows (R) Me',
                                '67': 'Windows XP',
                                '69': 'Microsoft Windows Server 2003',
                                '70': 'Microsoft Windows Server 2003 64-Bit',
                                '71': 'Windows XP 64-Bit',
                                '72': 'Windows XP Embedded',
                                '73': 'Windows Vista',
                                '74': 'Windows Vista 64-Bit',
                                '75': 'Windows Embedded for Point of Service',
                                '76': 'Microsoft Windows Server 2008',
                                '77': 'Microsoft Windows Server 2008 64-Bit',
                                '103': 'Microsoft Windows Server 2008 R2',
                                '105': 'Microsoft Windows 7',
                                '111': 'Microsoft Windows Server 2011',
                                '113': 'Microsoft Windows Server 2012',
                                '114': 'Microsoft Windows 8',
                                '115': 'Microsoft Windows 8 64-bit',
                                '116': 'Microsoft Windows Server 2012 R2'
                              }   # end osTypeWindows
    # end __init__()

    def parse(self):
        tree = ET.parse(self.file)
        self.root = tree.getroot()
        print("parsed file, root element is '{} w/ attributes {}"
              .format(self.root.tag, self.root.attrib))
        self._collect_system_data()
        self._collect_disk_data()
        self._collect_nic_data()
    # end parse()

    def _nsattr(self, attr, ns=None):
        ''' returns an attribute name w/ namespace prefix'''
        if ns is None:
            return attr
        else:
            return '{'+self._ns[ns]+'}'+attr
    # end _nsattr()

    def _collect_system_data(self):
        virtsys = self.root.find('ovf:VirtualSystem', self._ns)
        self.name = virtsys.find('ovf:Name', self._ns).text
        virtos = virtsys.find('ovf:OperatingSystemSection', self._ns)
        self.osid = virtos.get(self._nsattr('id', 'ovf'))
        if self.osid in self.osTypeLinux:
            self.licenseType = "LINUX"
            osname = self.osTypeLinux[self.osid]
        else:
            if self.osid in self.osTypeWindows:
                self.licenseType = "WINDOWS"
                osname = self.osTypeWindows[self.osid]
            else:
                osname = self.osTypeOther[self.osid]
        print("VM '{}' has {}-type OS '{}'(id:{})"
              .format(self.name, self.licenseType, osname, self.osid))
        virtcpu = virtsys.find('./ovf:VirtualHardwareSection/ovf:Item/[rasd:ResourceType="3"]', self._ns)
        self.cpus = virtcpu.find('rasd:VirtualQuantity', self._ns).text
        # !!! VMware also as vmw:CoresPerSocket !!!
        # we currently exclude this, so there may be cores missing in VM!
        virtmem = virtsys.find('./ovf:VirtualHardwareSection/ovf:Item/[rasd:ResourceType="4"]', self._ns)
        # we assume that RAM is specified in MB (or 'byte * 2^20')
        self.ram = virtmem.find('rasd:VirtualQuantity', self._ns).text
        print("VM '{}' has {} CPUs and {} MB RAM"
              .format(self.name, self.cpus, self.ram))
    # end _collect_system_data()

    # get the disks
    def _collect_disk_data(self):
        filerefs = self.root.findall('./ovf:References/ovf:File', self._ns)
        files = dict()
        for ref in filerefs:
            name = ref.get(self._nsattr('href', 'ovf'))
            fileid = ref.get(self._nsattr('id', 'ovf'))
            files[fileid] = name
        print("found filerefs {}".format(files))
        diskrefs = self.root.findall('./ovf:DiskSection/ovf:Disk', self._ns)
        disks = dict()
        for ref in diskrefs:
            # Note: we assume ovf:capacityAllocationUnits="byte * 2^30" == GiB
            capacity = ref.get(self._nsattr('capacity', 'ovf'))
            # reference to file references above
            fref = ref.get(self._nsattr('fileRef', 'ovf'))
            # the virt. HW section refers to '/disk/vmdisk1' not 'vmdisk1'
            diskid = 'ovf:/disk/'+ref.get(self._nsattr('diskId', 'ovf'))
            # we resolve fref here, we only need the name from now on
            disks[diskid] = {'capacity': capacity, 'file': files[fref]}
        print("found disks {}".format(disks))
        virtsys = self.root.find('ovf:VirtualSystem', self._ns)
        virthds = virtsys.findall('./ovf:VirtualHardwareSection/ovf:Item/[rasd:ResourceType="17"]', self._ns)
        devices = dict()
        for hdd in virthds:
            # print("hdd is {}".format(hdd))
            diskref = hdd.find('rasd:HostResource', self._ns).text
            address = hdd.find('rasd:AddressOnParent', self._ns)
            if address is None:
                print("no address for sorting found for {}, use InstanceId"
                      .format(diskref))
                devNr = hdd.find('rasd:InstanceId', self._ns).text
                print("disk {} has InstanceId {}".format(diskref, devNr))
            else:
                devNr = address.text
                print("disk {} has address {}".format(diskref, devNr))
            devices[devNr] = disks[diskref]
        print("devices : {}".format(devices))
        self.disks = [devices[devNr] for devNr in sorted(devices)]
        print("disks : {}".format(self.disks))
    # end _collect_disk_data()

    # get the nics
    def _collect_nic_data(self):
        # the NetworkSection contains only name and description
        # maybe that helps for better LAN assignment one day
        vnets = self.root.findall('./ovf:NetworkSection/ovf:Network', self._ns)
        lanid = 1
        for net in vnets:
            self.lans[net.get(self._nsattr('name', 'ovf'))] = lanid
            lanid += 1
        print("LANs found: {}".format(self.lans))
        virtsys = self.root.find('ovf:VirtualSystem', self._ns)
        virtnics = virtsys.findall('./ovf:VirtualHardwareSection/ovf:Item/[rasd:ResourceType="10"]', self._ns)
        devices = dict()
        for nic in virtnics:
            # print("nic is {}".format(nic))
            nicname = nic.find('rasd:ElementName', self._ns).text
            connection = nic.find('rasd:Connection', self._ns).text
            address = nic.find('rasd:AddressOnParent', self._ns)
            if address is None:
                print("no address for sorting found for {}, use InstanceId"
                      .format(nicname))
                devNr = nic.find('rasd:InstanceId', self._ns).text
                print("nic '{}' has InstanceId {}".format(nicname, devNr))
            else:
                devNr = address.text
                print("nic '{}' has address {}".format(nicname, devNr))
            devices[devNr] = {'nic': nicname, 'lan': connection,
                              'lanid': self.lans[connection]}
        print("devices : {}".format(devices))
        self.nics = [devices[devNr] for devNr in sorted(devices)]
        print("nics : {}".format(self.nics))
    # end _collect_nic_data()
# end class OVFData


# -- MAIN --

def main(argv=None):
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Jürgen Buchhammer on %s.
  Copyright 2016 ProfitBricks GmbH. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-u', '--user', dest='user', help='the login name')
        parser.add_argument('-p', '--password', dest='password',
                            help='the login password')
        parser.add_argument('-L', '--Login', dest='loginfile', default=None,
                            help='the login file to use')
        parser.add_argument('-t', '--type', dest='metatype',
                            default="OVF",
                            help='type of VM meta data')
        parser.add_argument('-m', '--metadata', dest='metafile',
                            required=True, default=None,
                            help='meta data file')
        parser.add_argument('-d', '--datacenterid', dest='datacenterid',
                            default=None,
                            help='datacenter of the new server')
        parser.add_argument('-D', '--DCname', dest='dcname', default=None,
                            help='new datacenter name')
        parser.add_argument('-l', '--location', dest='location', default=None,
                            help='location for new datacenter')
        parser.add_argument('-v', '--verbose', dest="verbose", action="count",
                            default=0,
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        global verbose
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")
            print("start {} with args {}".format(program_name, str(args)))

        (user, password) = getLogin(args.loginfile, args.user, args.password)
        if user is None or password is None:
            raise ValueError("user or password resolved to None")
        pbclient = ProfitBricksService(user, password)

        if args.metatype == 'OVF':
            metadata = OFVData(args.metafile)
            metadata.parse()
        else:
            sys.stderr.write("Metadata type '{}' is not supported"
                             .format(args.metatype))
            return 1

        # we need the DC first to have the location defined
        dc_id = None
        if args.datacenterid is None:
            if args.dcname is None or args.location is None:
                sys.stderr.write("Either '-d <id>' or '-D <name> -l <loc>'  must be specified")
                return 1
            # else: we will create the DC later after parsing the meta data
        else:
            dc_id = args.datacenterid

        if dc_id is None:
            location = args.location
            dc = Datacenter(name=args.dcname, location=location,
                            description="created by pb_importVM")
            print("create new DC {}".format(str(dc)))
            response = pbclient.create_datacenter(dc)
            dc_id = response['id']
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(result))
        else:
            dc = pbclient.get_datacenter(dc_id)
            location = dc['properties']['location']
            print("use existing DC {} in location {}"
                  .format(dc['properties']['name'], location))

        # check if images exist
        for disk in metadata.disks:
            disk_name = disk['file']
            images = get_disk_image_by_name(pbclient, location, disk_name)
            if len(images) == 0:
                raise ValueError("No HDD image with name '{}' found in location {}"
                                 .format(disk_name, location))
            if len(images) > 1:
                raise ValueError("Ambigous image name '{}' in location {}"
                                 .format(disk_name, location))
            disk['image'] = images[0]['id']

        # now we're ready to create the VM
        # Server
        server = Server(name=metadata.name,
                        cores=metadata.cpus, ram=metadata.ram)
        print("create server {}".format(str(Server)))
        response = pbclient.create_server(dc_id, server)
        srv_id = response['id']
        result = wait_for_request(pbclient, response['requestId'])
        print("wait loop returned {}".format(str(result)))
        # NICs (note that createing LANs may be implicit)
        for nic in metadata.nics:
            dcnic = NIC(name=nic['nic'], lan=nic['lanid'])
            print("create NIC {}".format(str(dcnic)))
            response = pbclient.create_nic(dc_id, srv_id, dcnic)
            nic_id = response['id']
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(str(result)))
            response = pbclient.get_nic(dc_id, srv_id, nic_id, 2)
            mac = response['properties']['mac']
            print("dcnic has MAC {} for {}".format(mac, nic_id))
        # end for(nics)
        # Volumes (we use the image name as volume name too
        requests = []
        for disk in metadata.disks:
            dcvol = Volume(name=disk['file'], size=disk['capacity'],
                           image=disk['image'],
                           licence_type=metadata.licenseType)
            print("create Volume {}".format(str(dcvol)))
            response = pbclient.create_volume(dc_id, dcvol)
            requests.append(response['requestId'])
            disk['volume_id'] = response['id']
        # end for(disks)
        if len(requests) != 0:
            result = wait_for_requests(pbclient, requests, initial_wait=10, scaleup=15)
            print("wait loop returned {}".format(str(result)))
        for disk in metadata.disks:
            print("attach volume {}".format(disk))
            response = pbclient.attach_volume(dc_id, srv_id, disk['volume_id'])
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(str(result)))
        # end for(disks)

        print("import of VM succesfully finished")
        return 0

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2
# end main()

if __name__ == "__main__":
    sys.exit(main())
