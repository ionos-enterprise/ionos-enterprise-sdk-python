import re
import time

from helpers import configuration


def resource():
    return {
        'locations': ['us/las', 'de/fra', 'de/fkb'],
        'vm_states': ['RUNNING', 'SHUTOFF'],
        'uuid_match': re.compile(
            '^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'),
        'mac_match': re.compile(
            '^([0-9a-f]{2}[:]){5}([0-9a-f]{2})$'),
        'datacenter': {
            'name': 'Python SDK Test',
            'description': 'Python SDK test datacenter',
            'location': configuration.LOCATION
        },
        'server': {
            'name': 'Python SDK Test',
            'ram': 1024,
            'cores': 1
        },
        'volume': {
            'name': 'Python SDK Test',
            'size': 2,
            'bus': 'VIRTIO',
            'type': 'HDD',
            'licence_type': 'UNKNOWN',
        },
        'volume_failure': {
            'name': 'Negative Python SDK Test',
            'size': 3,
            'bus': 'VIRTIO',
            'type': 'HDD',
            'licence_type': 'UNKNOWN'
        },
        'snapshot': {
            'name': 'Python SDK Test',
            'description': 'Python SDK test snapshot'
        },
        'nic': {
            'name': 'Python SDK Test',
            'dhcp': True,
            'lan': 1,
            'firewall_active': True,
            'nat': False
        },
        'fwrule': {
            'name': 'SSH',
            'protocol': 'TCP',
            'source_mac': '01:23:45:67:89:00',
            'source_ip': None,
            'target_ip': None,
            'port_range_start': 22,
            'port_range_end': 22,
            'icmp_type': None,
            'icmp_code': None,
        },
        'loadbalancer': {
            'name': 'Python SDK Test',
            'dhcp': True
        },
        'lan': {
            # REST API converts names to lowercase.
            'name': 'python sdk test',
            'public': True,
        },
        'ipblock': {
            # REST API converts names to lowercase.
            'name': 'python sdk test',
            'location': configuration.LOCATION,
            'size': 1
        }
    }


def find_image(conn, name):
    '''
    Find image by partial name and location.
    '''
    for item in conn.list_images()['items']:
        if (item['properties']['location'] == configuration.LOCATION and
                    item['properties']['imageType'] == 'HDD' and
                    name in item['properties']['name']):
            return item


def wait_for_completion(conn, promise, msg, wait_timeout=300):
    if not promise:
        return
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        time.sleep(1)
        operation_result = conn.get_request(
            request_id=promise['requestId'],
            status=True)

        if operation_result['metadata']['status'] == "DONE":
            return
        elif operation_result['metadata']['status'] == "FAILED":
            raise Exception(
                'Request failed to complete'.format(
                    msg, str(promise['requestId']))
            )

    raise Exception(
        'Timed out waiting for async operation {0} msg {1} to '
        'complete'.format(
            msg, str(promise['requestId']))
    )
