#!/usr/local/bin/python
# encoding: utf-8
'''
pb_snapshotDatacenter is a sample script to make a snapshot of a complete datacenter.
pb_snapshotDatacenter
- makes a snap shot of each server volume
- dumps the datacenter inventory to a file

You can use this information to restore or clone a datacenter
or use it as a starting point for new data centers.


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

from datetime import datetime
from time import sleep
import json
from base64 import b64decode, b64encode

from profitbricks.client import ProfitBricksService


__all__ = []
__version__ = 0.1
__date__ = '2016-09-02'
__updated__ = '2016-09-02'


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


def write_dc_definition(pbclient, dcdef=None, filename=None):
    with open(filename, 'w') as outfile:
        json.dump(dcdef, outfile, indent=2)
    return 0
# end write_dc_definition()


def read_dc_definition(pbclient, filename=None):
    with open(filename) as infile:
        dcdef = json.load(infile)
    return dcdef
# end read_dc_definition()


# --- request status (see pb_createDatacenter.py)

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


# ---- server states and control (see pb_controlServerStates.py)


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
        sleep(seconds)
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


def controlServerState(pbclient=None, dc_id=None,
                       serverid=None, servername=None, action=None):
    server = getServerStates(pbclient, dc_id,
                             serverid, servername)
    if server is None:
        raise Exception(1, "specified server not found")
    print("using server {}(id={}) in state {}, {}"
          .format(server['name'], server['id'], server['state'],
                  server['vmstate']))
    # !!! stop/start/reboot_server() simply return 'True' !!!
    # this implies, that there's NO response nor requestId to track!

    if action == 'POWEROFF':
        if server['state'] == 'INACTIVE':
            print("server is already powered off")
        else:
            # currently use 'forced' poweroff
            if server['vmstate'] != 'SHUTOFF':
                print("VM is in state {}, {} may lead to inconsistent state"
                      .format(server['vmstate'], action))
            pbclient.stop_server(dc_id, server['id'])
            server = wait_for_server(pbclient, dc_id, server['id'],
                                     state='INACTIVE', timeout=300)
    elif action == 'POWERON':
        if server['vmstate'] == 'RUNNING':
            print("VM is already up and running")
        else:
            pbclient.start_server(dc_id, server['id'])
            server = wait_for_server(pbclient, dc_id, server['id'],
                                     indicator='vmstate', state='RUNNING',
                                     timeout=300)
    elif action == 'START':
        # this is the same as POWERON
        if server['vmstate'] == 'RUNNING':
            print("VM is already up and running")
        else:
            pbclient.start_server(dc_id, server['id'])
            server = wait_for_server(pbclient, dc_id, server['id'],
                                     indicator='vmstate', state='RUNNING',
                                     timeout=300)
    elif action == 'SHUTOFF':
        if server['vmstate'] == 'SHUTOFF':
            print("VM is already shut off")
        else:
            print("no command specified for shutdown of VM")
    # end if/else(action)
    print("server {}(id={}) now in state {}, {}"
          .format(server['name'], server['id'], server['state'],
                  server['vmstate']))
# end controlServerState()


def main(argv=None):
    '''Parse command line options and dump a datacenter to snapshots and file.'''

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
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-u', '--user', dest='user', help='the login name')
        parser.add_argument('-p', '--password', dest='password',
                            help='the login password')
        parser.add_argument('-L', '--Login', dest='loginfile', default=None,
                            help='the login file to use')
        parser.add_argument('-d', '--datacenterid', dest='dc_id',
                            required=True, default=None,
                            help='datacenter ID of the server')
        parser.add_argument('-o', '--outfile', dest='outfile',
                            default='dc-def_'+datetime.now().strftime('%Y-%m-%d_%H%M%S'),
                            help='the output file name')
        parser.add_argument('-S', '--Stopalways', dest='stopalways', action='store_true',
                            help='power off even when VM is running')
        parser.add_argument('-v', '--verbose', dest="verbose", action="count",
                            default=0, help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        global verbose
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")
            print("start {} with args {}".format(program_name, str(args)))

        outfile = args.outfile
        if outfile.endswith(".json"):
            outfile = os.path.splitext(outfile)
        print("Using output file base name '{}'".format(outfile))

        (user, password) = getLogin(args.loginfile, args.user, args.password)
        if user is None or password is None:
            raise ValueError("user or password resolved to None")
        pbclient = ProfitBricksService(user, password)

        dc_id = args.dc_id

        # first get all server's VM and OS state to see if we can start
        srv_info = getServerInfo(pbclient, dc_id)
        srvon = 0
        for server in srv_info:
            if server['vmstate'] != 'SHUTOFF':
                print("VM {} is in state {}, but should be SHUTOFF"
                      .format(server['name'], server['vmstate']))
                srvon += 1
        # end for(srv_info)
        if srvon > 0 and not args.stopalways:
            print("shutdown running OS before trying again")
            return 1
        # now power off all VMs before starting the snapshots
        for server in srv_info:
            controlServerState(pbclient, dc_id, server['id'], action='POWEROFF')

        # now let's go
        dcdef = pbclient.get_datacenter(dc_id, 5)
        print("starting dump of datacenter {}".format(dcdef['properties']['name']))
        dcdef_file = outfile+'_source.json'
        print("write source dc to {}".format(dcdef_file))
        write_dc_definition(pbclient, dcdef, dcdef_file)
        print("get existing Snapshots")
        # first get existing snapshots
        known_snapshots = dict()
        snapshots = pbclient.list_snapshots()
        for snap in snapshots['items']:
            print("SNAP : {}".format(json.dumps(snap)))
            known_snapshots[snap['properties']['name']] = snap['id']
        print("create Snapshots, this may take a while ..")
        # we do NOT consider dangling volumes, only server-attached ones
        vol_snapshots = dict()   # map volume id==snapshot name snapshot id
        for server in dcdef['entities']['servers']['items']:
            print("- server {}".format(server['properties']['name']))
            if 'volumes' not in server['entities']:
                print(" server {} has no volumes"
                      .format(server['properties']['name']))
                continue
            # The volumes are attached by order of creation
            # Thus we must sort them to keep the order in the clone
            print("setting volume order by deviceNumber")
            volumes = server['entities']['volumes']['items']
            new_order = sorted(volumes, key=lambda vol: vol['properties']['deviceNumber'])
            server['entities']['volumes']['items'] = new_order
            for volume in server['entities']['volumes']['items']:
                vol_id = volume['id']   # this will be the name too
                if vol_id in known_snapshots:
                    print("use existing snapshot {} of volume {}"
                          .format(vol_id, volume['properties']['name']))
                    vol_snapshots[vol_id] = known_snapshots[vol_id]
                else:
                    print("taking snapshot {} of volume {}"
                          .format(vol_id, volume['properties']['name']))
                    response = pbclient.create_snapshot(dc_id, vol_id, vol_id,
                                                        "auto-created by pb_snapshotDatacenter")
                    # response has no request id, need to check metadata state (BUSY, AVAILABLE..)
                    vol_snapshots[vol_id] = response['id']
                    print("snapshot in progress: {}".format(str(response)))
            # end for(volume)
        # end for(server)
        print("Waiting for snapshots to complete")
        snapdone = dict()
        while len(snapdone) != len(vol_snapshots):
            sleep(10)
            for snap_id in vol_snapshots.values():
                print("looking for {}".format(snap_id))
                if snap_id in snapdone:
                    continue
                snapshot = pbclient.get_snapshot(snap_id)
                print("snapshot {} is in state {}"
                      .format(snap_id, snapshot['metadata']['state']))
                if snapshot['metadata']['state'] == 'AVAILABLE':
                    snapdone[snap_id] = snapshot['metadata']['state']
            # end for(vol_snapshots)
        # end while(snapdone)

        # now replace the volumes image IDs
        print("setting snapshot id to volumes")
        for server in dcdef['entities']['servers']['items']:
            print("- server {}".format(server['properties']['name']))
            if 'volumes' not in server['entities']:
                print(" server {} has no volumes"
                      .format(server['properties']['name']))
                continue
            for volume in server['entities']['volumes']['items']:
                vol_id = volume['id']   # this will be the name too
                volume['properties']['image'] = vol_snapshots[vol_id]
            # end for(volume)
        # end for(server)

        # As it came out, the LAN id is rearranged by order of creation
        # Thus we must sort the LANs to keep the order in the clone
        print("setting LAN order by id")
        lans = dcdef['entities']['lans']['items']
        new_order = sorted(lans, key=lambda lan: lan['id'])
        dcdef['entities']['lans']['items'] = new_order

        # now sort unordered NICs by MAC and save the dcdef
        # reason is, that NICs seem to be ordered by MAC, but API response
        # doesn't guarantee the order, which we need for re-creation
        print("setting NIC order by MAC")
        for server in dcdef['entities']['servers']['items']:
            print("- server {}".format(server['properties']['name']))
            if 'nics' not in server['entities']:
                print(" server {} has no nics"
                      .format(server['properties']['name']))
                continue
            nics = server['entities']['nics']['items']
            # print("NICs before {}".format(json.dumps(nics)))
            new_order = sorted(nics, key=lambda nic: nic['properties']['mac'])
            # print("NICs after {}".format(json.dumps(new_order)))
            server['entities']['nics']['items'] = new_order
        # end for(server)
        dcdef_file = outfile+'.json'
        print("write snapshot dc to {}".format(dcdef_file))
        write_dc_definition(pbclient, dcdef, dcdef_file)

        return 0

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())
    