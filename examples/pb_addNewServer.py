#!/usr/local/bin/python
# encoding: utf-8
'''
pb_addNewServer -- adds a new server to a data center

pb_addNewServer is a tool to add a new server/storage composite to an
existing data center. The server may be set up by a disk or cdrom image.


@author:     Jürgen Buchhammer

@copyright:  2016 ProfitBricks GmbH. All rights reserved.

@license:    Apache License 2.0

@contact:    juergen.buchhammer@profitbricks.com
@deffield    updated: Updated
'''

import sys
import os
import traceback

from time import sleep
from datetime import datetime

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from base64 import b64encode, b64decode

from profitbricks.client import ProfitBricksService, Server, Volume, NIC


__all__ = []
__version__ = 0.1
__date__ = '2016-02-16'
__updated__ = '2016-02-16'


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
    if os.path.exists(filename):
        print("Using file {} for Login".format(filename))
        with open(filename, "r") as loginfile:
            encoded_cred = loginfile.read()
            decoded_cred = b64decode(encoded_cred)
            login = decoded_cred.split(':', 1)
            return (login[0], login[1])
    else:
        if user is None or passwd is None:
            raise ValueError("user and password must not be None")
        print("Writing file {} for Login".format(filename))
        with open(filename, "w") as loginfile:
            encoded_cred = b64encode(user+":"+passwd)
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
        if verbose > 0:
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
            if verbose > 0:
                print("scaling up wait_period to {}, next change in {} seconds"
                      .format(wait_period, next_scaleup))
    # end while(wait)
    return(-1, state, "request not finished before timeout")
# end wait_for_request()


def main(argv=None):
    '''Parse command line options and create a server/volume composite.'''

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

  Created by J. Buchhammer on %s.
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
        parser.add_argument('-d', '--datacenterid', dest='datacenterid',
                            required=True, default=None,
                            help='datacenter of the new server')
        parser.add_argument('-l', '--lanid', dest='lanid', required=True,
                            default=None, help='LAN of the new server')
        parser.add_argument('-n', '--name', dest='servername',
                            default="SRV_"+datetime.now().isoformat(),
                            help='name of the new server')
        parser.add_argument('-c', '--cores', dest='cores', type=int,
                            default=2, help='CPU cores')
        parser.add_argument('-r', '--ram', dest='ram', type=int, default=4,
                            help='RAM in GB')
        parser.add_argument('-s', '--storage', dest='storage', type=int,
                            default=4, help='storage in GB')
        parser.add_argument('-b', '--boot', dest='bootdevice', default="HDD",
                            help='boot device')
        parser.add_argument('-i', '--imageid', dest='imageid', default=None,
                            help='installation image')
        parser.add_argument('-P', '--imagepassword', dest='imgpassword',
                            default=None, help='the image password')
        parser.add_argument('-v', '--verbose', dest="verbose", action="count",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        global verbose
        verbose = args.verbose
        dc_id = args.datacenterid
        lan_id = args.lanid
        servername = args.servername

        if verbose > 0:
            print("Verbose mode on")
            print("start {} with args {}".format(program_name, str(args)))

        # Test images (location de/fra)
        # CDROM: 7fc885b3-c9a6-11e5-aa10-52540005ab80   # debian-8.3.0-amd64-netinst.iso
        # HDD:   28007a6d-c88a-11e5-aa10-52540005ab80   # CentOS-7-server-2016-02-01
        hdimage = args.imageid
        cdimage = None
        if args.bootdevice == "CDROM":
            hdimage = None
            cdimage = args.imageid
        print("using boot device {} with image {}"
              .format(args.bootdevice, args.imageid))

        (user, password) = getLogin(args.loginfile, args.user, args.password)
        if user is None or password is None:
            raise ValueError("user or password resolved to None")
        pbclient = ProfitBricksService(user, password)

        first_nic = NIC(name="local", ips=[], dhcp=True, lan=lan_id)
        volume = Volume(name=servername+"-Disk", size=args.storage,
                        image=hdimage, image_password=args.imgpassword)
        server = Server(name=servername, cores=args.cores, ram=args.ram*1024,
                        create_volumes=[volume], nics=[first_nic],
                        boot_cdrom=cdimage)
        print("creating server..")
        if verbose > 0:
            print("SERVER: {}".format(str(server)))
        response = pbclient.create_server(dc_id, server)
        print("wait for provisioning..")
        wait_for_request(pbclient, response["requestId"])
        server_id = response['id']
        print("Server provisioned with ID {}".format(server_id))
        nics = pbclient.list_nics(dc_id, server_id, 1)
        # server should have exactly one nic, but we only test empty nic list
        if len(nics['items']) == 0:
            raise CLIError("No NICs found for newly created server {}"
                           .format(server_id))
        nic0 = nics['items'][0]
        if verbose > 0:
            print("NIC0: {}".format(str(nic0)))
        (nic_id, nic_mac) = (nic0['id'], nic0['properties']['mac'])
        print("NIC of new Server has ID {} and MAC {}".format(nic_id, nic_mac))
        print("{} finished w/o errors".format(program_name))
        return 0

    except KeyboardInterrupt:
        # handle keyboard interrupt #
        return 0
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2
# end main()

if __name__ == "__main__":
    sys.exit(main())
