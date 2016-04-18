#!/usr/local/bin/python
# encoding: utf-8
'''
pb_deleteServer -- remove a server completely

pb_deleteServer is a tool to completely remove a server
and attached volumes.


@author:     Jürgen Buchhammer

@copyright:  2016 ProfitBricks GmbH. All rights reserved.

@license:    Apache License 2.0

@contact:    juergen.buchhammer@profitbricks.com
@deffield    updated: Updated
'''

import sys
import os
import traceback
import time

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from base64 import b64encode, b64decode
from subprocess import call

from profitbricks.client import ProfitBricksService


__all__ = []
__version__ = 0.1
__date__ = '2016-02-25'
__updated__ = '2016-02-25'


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
#             print("encoded: {}".format(encoded_cred))
            decoded_cred = b64decode(encoded_cred)
            login = decoded_cred.split(':', 1)
            return (login[0], login[1])
    else:
        if user is None or passwd is None:
            raise ValueError("user and password must not be None")
        print("Writing file {} for Login".format(filename))
        with open(filename, "w") as loginfile:
            encoded_cred = b64encode(user+":"+passwd)
#             print("encoded: {}".format(encoded_cred))
            loginfile.write(encoded_cred)
        return (user, passwd)
# end getLogin()


def getServerInfo(pbclient=None, dc_id=None):
    ''' gets info of servers of a data center'''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc_id is None:
        raise ValueError("argument 'dc_id' must not be None")
    # list of all found server's info
    server_info = []
    # depth 1 is enough for props/meta
    servers = pbclient.list_servers(dc_id, 1)
    for server in servers['items']:
        props = server['properties']
        info = dict(id=server['id'], name=props['name'],
                    state=server['metadata']['state'],
                    vmstate=props['vmState'])
        server_info.append(info)
    # end for(servers)
    return(server_info)
# end getServerInfo()


def select_where(info=None, select=None, **where):
    if info is None:
        raise ValueError("argument 'info' must not be None")
    if len(info) == 0:
        return []
    if select is None:
        select = info[0].keys()
    server_info = []
    for old_si in info:
        w_matches = all(old_si[wk]==wv for (wk,wv) in where.items())
        new_si = {k:v for (k,v) in old_si.items() if k in select and w_matches}
        if len(new_si) > 0:
            server_info.append(new_si)
    # end for(info)
    return(server_info)
# end select_where()


def getServerStates(pbclient=None, dc_id=None, serverid=None, servername=None):
    ''' gets states of a server'''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc_id is None:
        raise ValueError("argument 'dc_id' must not be None")
    server = None
    if serverid is None:
        if servername is None:
            raise ValueError("one of 'serverid' or 'servername' must be specified")
        # so, arg.servername is set (to whatever)
        server_info = select_where(getServerInfo(pbclient, dc_id),
                                   ['id', 'name', 'state', 'vmstate'],
                                   name=servername)
        if len(server_info) > 1:
            raise NameError("ambiguous server name '{}'".format(servername))
        if len(server_info) == 1:
            server = server_info[0]
    else:
        # get by ID may also fail if it's removed
        # in this case, catch exception (message 404) and be quiet for a while
        # unfortunately this has changed from Py2 to Py3
        try:
            server_info = pbclient.get_server(dc_id, serverid, 1)
            server = dict(id=server_info['id'],
                          name=server_info['properties']['name'],
                          state=server_info['metadata']['state'],
                          vmstate=server_info['properties']['vmState'])
        except Exception:
            ex = sys.exc_info()[1]
            if ex.args[0] is not None and ex.args[0] == 404:
                print("Server w/ ID {} not found".format(serverid))
                server = None
            else:
                raise ex
        # end try/except
    # end if/else(serverid)
    return server
# end getServerStates()


def wait_for_server(pbclient=None, dc_id=None, serverid=None,
                    indicator='state', state='AVAILABLE', timeout=300):
    '''
    wait for a server/VM to reach a defined state for a specified time
    indicator := {state|vmstate} specifies if server or VM stat is tested
    state specifies the status the indicator should have
    '''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc_id is None:
        raise ValueError("argument 'dc_id' must not be None")
    if serverid is None:
        raise ValueError("argument 'serverid' must not be None")
    total_sleep_time = 0
    seconds = 5
    while total_sleep_time < timeout:
        time.sleep(seconds)
        total_sleep_time += seconds
        if total_sleep_time == 60:
            # Increase polling interval after one minute
            seconds = 10
        elif total_sleep_time == 600:
            # Increase polling interval after 10 minutes
            seconds = 20
        server = getServerStates(pbclient, dc_id, serverid)
        if server[indicator] == state:
            break
    # end while(total_sleep_time)
    return server
# end wait_for_server()


def wait_for_datacenter(client, data_center_id):
    '''
    Poll the data center to become available (for the next provisionig job)
    '''
    total_sleep_time = 0
    seconds = 5
    while True:
        state = client.get_datacenter(data_center_id)['metadata']['state']
        if verbose:
            print("datacenter is {}".format(state))
        if state == "AVAILABLE":
            break
        time.sleep(seconds)
        total_sleep_time += seconds
        if total_sleep_time == 60:
            # Increase polling interval after one minute
            seconds = 10
        elif total_sleep_time == 600:
            # Increase polling interval after 10 minutes
            seconds = 20
# end wait_for_datacenter()


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
        parser.add_argument('-d', '--datacenterid', dest='dc_id',
                            required=True, default=None,
                            help='datacenter of the server')
        parser.add_argument('-s', '--serverid', dest='serverid', default=None,
                            help='ID of the server')
        parser.add_argument('-n', '--name', dest='servername', default=None,
                            help='name of the server')
        parser.add_argument('-C', '--command', dest='command', default=None,
                            help='remote shell command to use for shutdown')
        parser.add_argument('-v', '--verbose', dest="verbose", action="count",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        global verbose
        verbose = args.verbose
        dc_id = args.dc_id

        if verbose > 0:
            print("Verbose mode on")

        if args.serverid is None and args.servername is None:
            parser.error("one of 'serverid' or 'name' must be specified")

        (user, password) = getLogin(args.loginfile, args.user, args.password)
        if user is None or password is None:
            raise ValueError("user or password resolved to None")
        pbclient = ProfitBricksService(user, password)

        server = getServerStates(pbclient, dc_id, args.serverid,
                                 args.servername)
        if server is None:
            raise Exception(1, "specified server not found")
        print("using server {}(id={}) in state {}, {}"
              .format(server['name'], server['id'], server['state'],
                      server['vmstate']))
        # ! stop/start/reboot_server() simply return 'True' !
        # this implies, that there's NO response nor requestId to track!
        if server['vmstate'] == 'SHUTOFF':
            print("VM is already shut off")
        else:
            if args.command is None:
                print("no command specified for shutdown of VM")
            else:
                print("executing {}".format(args.command))
                cmdrc = call(args.command, shell=True)
                print("executing {} returned {}".format(args.command, cmdrc))
                server = wait_for_server(pbclient, dc_id, server['id'],
                                         indicator='vmstate', state='SHUTOFF',
                                         timeout=300)
        # first we have to delete all attached volumes
        volumes = pbclient.get_attached_volumes(dc_id, server['id'], 0)
        for vol in volumes['items']:
            print("deleting volume {} of server {}"
                  .format(vol['id'], server['name']))
            pbclient.delete_volume(dc_id, vol['id'])
        pbclient.delete_server(dc_id, server['id'])
        wait_for_datacenter(pbclient, dc_id)
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
