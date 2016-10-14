#!/usr/local/bin/python
# encoding: utf-8
'''
pb_createDatacenter is a sample script to create a complex datacenter.


@author:     Jürgen Buchhammer

@copyright:  2016 ProfitBricks GmbH. All rights reserved.

@license:    Apache License 2.0

@contact:    juergen.buchhammer@profitbricks.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from datetime import datetime
from time import sleep
import json
from base64 import b64decode, b64encode

from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Volume, Server
from profitbricks.client import LAN, NIC, FirewallRule


__version__ = 0.2
__date__ = '2016-09-26'
__updated__ = __date__


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


def create_datacenter_dict(pbclient, datacenter):
    """
    Creates a Datacenter dict -- both simple and complex are supported.
    This is copied from createDatacenter() and uses private methods.

    """
    server_items = []
    volume_items = []
    lan_items = []
    loadbalancer_items = []

    entities = dict()

    properties = {
        "name": datacenter.name,
        "location": datacenter.location,
    }
    ' Optional Properties'
    if datacenter.description:
        properties['description'] = datacenter.description

    ' Servers '
    if len(datacenter.servers) > 0:
        for server in datacenter.servers:
            server_items.append(pbclient._create_server_dict(server))
        servers = {
            "items": server_items
        }
        server_entities = {
            "servers": servers
        }
        entities.update(server_entities)

    ' Volumes '
    if len(datacenter.volumes) > 0:
        for volume in datacenter.volumes:
            volume_items.append(pbclient._create_volume_dict(volume))
        volumes = {
            "items": volume_items
        }
        volume_entities = {
            "volumes": volumes
        }
        entities.update(volume_entities)

    ' Load Balancers '
    if len(datacenter.loadbalancers) > 0:
        for loadbalancer in datacenter.loadbalancers:
            loadbalancer_items.append(
                pbclient._create_loadbalancer_dict(
                    loadbalancer
                    )
                )
        loadbalancers = {
            "items": loadbalancer_items
        }
        loadbalancer_entities = {
            "loadbalancers": loadbalancers
        }
        entities.update(loadbalancer_entities)

    ' LANs '
    if len(datacenter.lans) > 0:
        for lan in datacenter.lans:
            lan_items.append(
                pbclient._create_lan_dict(lan)
                )
        lans = {
            "items": lan_items
        }
        lan_entities = {
            "lans": lans
        }
        entities.update(lan_entities)

    if len(entities) == 0:
        raw = {
            "properties": properties,
        }
    else:
        raw = {
            "properties": properties,
            "entities": entities
        }

    return raw
# end create_datacenter_dict()


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


#-- build objects from internal dict structures --

def getDatacenterObject(defdict=None):
    if defdict is None or not type(defdict) is dict or len(defdict.keys()) == 0:
        raise ValueError("argument 'defdict' must be non-empty dict")
    props = dict()
    for k, v in defdict['properties'].items():
        # no renaming needed here, but this accounts for optional props too
        props[k] = v
    apiobj = Datacenter(**props)
    return(apiobj)
# end getDatacenterObject()


def getVolumeObject(defdict=None):
    if defdict is None or not type(defdict) is dict or len(defdict.keys()) == 0:
        raise ValueError("argument 'defdict' must be non-empty dict")
    #-- TODO: can we set deviceNumber too? Nope, not supported in Volume()
    # AARGH! some of Volume's fields have different names -> need to convert
    # so make a copy and let source as is
    props = dict()
    for k, v in defdict['properties'].items():
        if k == 'type':
            props['disk_type'] = v
            continue
        if k == 'imagePassword':
            props['image_password'] = v
            continue
        if k == 'licenceType':
            props['licence_type'] = v
            continue
        if k == 'sshKeys':
            props['ssh_keys'] = v
            continue
        props[k] = v
    # end for(defdict)
    apiobj = Volume(**props)
    return(apiobj)
# end getVolumeObject()


def getServerObject(defdict=None):
    if defdict is None or not type(defdict) is dict or len(defdict.keys()) == 0:
        raise ValueError("argument 'defdict' must be non-empty dict")
    # AARGH! some of Servers's fields have different names -> need to convert manually
    # so make a copy and let source as is
    props = dict()
    for k, v in defdict['properties'].items():
        if k == 'availabilityZone':
            props['availability_zone'] = v
            continue
        if k == 'bootCdrom':
            props['boot_cdrom'] = v
            continue
        if k == 'cpuFamily':
            props['cpu_family'] = v
            continue
#-- TODO: if volumes entries have an ID -> attach, else create w/ properties of volume
#         if k == 'bootVolume':
#             props['boot_volume_id'] = v
#             continue
#         if k == 'volumes':
#             props['create_volumes'] = v
#             continue
#         if k == 'volumes':
#             props['attach_volumes'] = v
#             continue
# Server() has no kwargs, so we must exactly match the known keywords
        if k in ['name', 'cores', 'ram']:
            props[k] = v
    # end for(defdict)
    apiobj = Server(**props)
    return(apiobj)
# end getServerObject()


def getNICObject(defdict=None):
    if defdict is None or not type(defdict) is dict or len(defdict.keys()) == 0:
        raise ValueError("argument 'defdict' must be non-empty dict")
    # AARGH! some of NIC's fields have different names -> need to convert manually
    # so make a copy and let source as is
    props = dict()
    for k, v in defdict['properties'].items():
        if k == 'firewallActive':
            props['firewall_active'] = v
            continue
        if k == 'firewallrules':
            # this needs more to do:
            # if we have rules we must get rules objects too, irrespective of being active
            if len(v) != 0:
                rules = [getFwRuleObject(rule) for rule in v]
                props['firewall_rules'] = rules
                continue
        props[k] = v
    # end for(defdict)
    apiobj = NIC(**props)
    return(apiobj)
# end getNICObject()


def getFwRuleObject(defdict=None):
    if defdict is None or not type(defdict) is dict or len(defdict.keys()) == 0:
        raise ValueError("argument 'defdict' must be non-empty dict")
    # AARGH! some of NIC's fields have different names -> need to convert manually
    # so make a copy and let source as is
    props = dict()
    for k, v in defdict['properties'].items():
        if k == 'sourceMac':
            props['source_mac'] = v
            continue
        if k == 'sourceIp':
            props['source_ip'] = v
            continue
        if k == 'targetIp':
            props['target_ip'] = v
            continue
        if k == 'portRangeStart':
            props['port_range_start'] = v
            continue
        if k == 'portRangeEnd':
            props['port_range_end'] = v
            continue
        if k == 'icmpType':
            props['icmp_type'] = v
            continue
        if k == 'icmpCode':
            props['icmp_code'] = v
            continue
        props[k] = v
    # end for(defdict)
    apiobj = FirewallRule(**props)
    return(apiobj)
# end getFwRuleObject()


def getLANObject(defdict=None):
    if defdict is None or not type(defdict) is dict or len(defdict.keys()) == 0:
        raise ValueError("argument 'defdict' must be non-empty dict")
    props = dict()
    for k, v in defdict['properties'].items():
        # no renaming needed here, but this accounts for optional props too
        props[k] = v
    # end for(defdict)
    apiobj = LAN(**props)
    return(apiobj)
# end getLANObject()


#-- the (far too long) main method --

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
    # Setup argument parser
    parser = ArgumentParser(description=program_license,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--user', dest='user', help='the login name')
    parser.add_argument('-p', '--password', dest='password',
                        help='the login password')
    parser.add_argument('-L', '--Login', dest='loginfile', default=None,
                        help='the login file to use')
    parser.add_argument('-i', '--infile', dest='infile', default=None,
                        required=True, help='the input file name')
    parser.add_argument('-D', '--DCname', dest='dcname', default=None,
                        help='new datacenter name')
# TODO: add/overwrite image password for creation
#    parser.add_argument('-P', '--imagepassword', dest='imgpassword',
#                        default=None, help='the image password')
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

    (user, password) = getLogin(args.loginfile, args.user, args.password)
    if user is None or password is None:
        raise ValueError("user or password resolved to None")
    pbclient = ProfitBricksService(user, password)

    usefile = args.infile
    print("read dc from {}".format(usefile))
    dcdef = read_dc_definition(pbclient, usefile)
    if verbose > 0:
        print("using DC-DEF {}".format(json.dumps(dcdef)))

    # setup dc:
    #     + create empty dc
    #     + create volumes (unattached), map uuid to servers (custom dict)
    #     + create servers
    #     + create nics
    #     + attach volumes

    if 'custom' in dcdef and 'id' in dcdef['custom']:
        dc_id = dcdef['custom']['id']
        print("using existing DC w/ id {}".format(str(dc_id)))
    else:
        if args.dcname is not None:
            print("Overwrite DC name w/ '{}'".format(args.dcname))
            dcdef['properties']['name'] = args.dcname
        dc = getDatacenterObject(dcdef)
        # print("create DC {}".format(str(dc)))
        response = pbclient.create_datacenter(dc)
        dc_id = response['id']
        if 'custom' not in dcdef:
            dcdef['custom'] = dict()
        dcdef['custom']['id'] = dc_id
        result = wait_for_request(pbclient, response['requestId'])
        print("wait loop returned {}".format(result))
        tmpfile = usefile+".tmp_postdc"
        write_dc_definition(pbclient, dcdef, tmpfile)

    requests = []
    print("create Volumes {}".format(str(dc)))
    # we do NOT consider dangling volumes, only server-attached ones
    for server in dcdef['entities']['servers']['items']:
        print("- server {}".format(server['properties']['name']))
        if 'volumes' not in server['entities']:
            print(" server {} has no volumes".format(server['properties']['name']))
            continue
        for volume in server['entities']['volumes']['items']:
            if 'custom' in volume and 'id' in volume['custom']:
                vol_id = volume['custom']['id']
                print("using existing volume w/ id {}".format(str(vol_id)))
            else:
                dcvol = getVolumeObject(volume)
                print("OBJ: {}".format(str(dcvol)))
                response = pbclient.create_volume(dc_id, dcvol)
                volume.update({'custom': {'id': response['id']}})
                requests.append(response['requestId'])
        # end for(volume)
    # end for(server)
    if len(requests) != 0:
        result = wait_for_requests(pbclient, requests, initial_wait=10, scaleup=15)
        print("wait loop returned {}".format(str(result)))
        tmpfile = usefile+".tmp_postvol"
        write_dc_definition(pbclient, dcdef, tmpfile)
    else:
        print("all volumes existed already")

    requests = []
    print("create Servers {}".format(str(dc)))
    # we do NOT consider dangling volumes, only server-attached ones
    for server in dcdef['entities']['servers']['items']:
        print("- server {}".format(server['properties']['name']))
        if 'custom' in server and 'id' in server['custom']:
            srv_id = server['custom']['id']
            print("using existing server w/ id {}".format(str(srv_id)))
        else:
            dcsrv = getServerObject(server)
            print("OBJ: {}".format(str(dcsrv)))
            response = pbclient.create_server(dc_id, dcsrv)
            server.update({'custom': {'id': response['id']}})
            requests.append(response['requestId'])
    # end for(server)
    if len(requests) != 0:
        result = wait_for_requests(pbclient, requests, initial_wait=10, scaleup=15)
        print("wait loop returned {}".format(str(result)))
        tmpfile = usefile+".tmp_postsrv"
        write_dc_definition(pbclient, dcdef, tmpfile)
    else:
        print("all servers existed already")

# TODO: only do this if we have lan entities
    requests = []
    # Huuh, looks like we get unpredictable order for LANs!
    # Nope, order of creation determines the LAN id,
    # thus we better wait for each request 
    print("create LANs {}".format(str(dc)))
    for lan in dcdef['entities']['lans']['items']:
        print("- lan {}".format(lan['properties']['name']))
        dclan = getLANObject(lan)
        print("OBJ: {}".format(str(dclan)))
        response = pbclient.create_lan(dc_id, dclan)
        lan.update({'custom': {'id': response['id']}})
        result = wait_for_request(pbclient, response['requestId'])
        print("wait loop returned {}".format(str(result)))
    # end for(lan)
    tmpfile = usefile+".tmp_postlan"
    write_dc_definition(pbclient, dcdef, tmpfile)

    requests = []
    # Attention:
    # NICs appear in OS in the order, they are created.
    # But DCD rearranges the display by ascending MAC addresses.
    # This does not change the OS order.
    # MAC may not be available from create response,
    # thus we wait for each request :-(
    print("create NICs {}".format(str(dc)))
    for server in dcdef['entities']['servers']['items']:
        print("- server {}".format(server['properties']['name']))
        srv_id = server['custom']['id']
        if 'nics' not in server['entities']:
            print(" server {} has no NICs".format(server['properties']['name']))
            continue
        macmap = dict()
        for nic in server['entities']['nics']['items']:
            dcnic = getNICObject(nic)
            response = pbclient.create_nic(dc_id, srv_id, dcnic)
            # print("dcnic response {}".format(str(response)))
            # mac = response['properties']['mac'] # we don't get it here !?
            nic_id = response['id']
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(str(result)))
            response = pbclient.get_nic(dc_id, srv_id, nic_id, 2)
            mac = response['properties']['mac']
            print("dcnic has MAC {} for {}".format(mac, nic_id))
            macmap[mac] = nic_id
        # end for(nic)
        macs = sorted(macmap)
        print("macs will be displayed by DCD in th following order:")
        for mac in macs:
            print("mac {} -> id{}".format(mac, macmap[mac]))
    # end for(server)
    tmpfile = usefile+".tmp_postnic"
    write_dc_definition(pbclient, dcdef, tmpfile)

    requests = []
    # don't know if we get a race here too, so better wait for each request :-/
    print("attach volumes {}".format(str(dc)))
    for server in dcdef['entities']['servers']['items']:
        print("- server {}".format(server['properties']['name']))
        if 'volumes' not in server['entities']:
            print(" server {} has no volumes".format(server['properties']['name']))
            continue
        srv_id = server['custom']['id']
        for volume in server['entities']['volumes']['items']:
            print("OBJ: {}".format(volume['properties']['name']))
            response = pbclient.attach_volume(dc_id, srv_id, volume['custom']['id'])
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(str(result)))
        # end for(volume)
    # end for(server)
    tmpfile = usefile+".tmp_postatt"
    write_dc_definition(pbclient, dcdef, tmpfile)

    # TODO: do we need to set boot volume for each server?
    # looks like it's working without

    return 0

# end main()

if __name__ == "__main__":
    sys.exit(main())
