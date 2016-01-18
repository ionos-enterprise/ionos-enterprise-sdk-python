import re
import time
from helpers import configuration

def resource():
    return {
        'locations': ['us/lasdev', 'us/las', 'de/fra', 'de/fkb'],
        'vm_states': ['RUNNING', 'SHUTOFF'],
        'uuid_match': re.compile(
            '^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
        ),
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
            'size': 5,
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
            'firewall_active': True
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
            'name': 'Python SDK Test',
            'public': True,
        },
        'ipblock': {
            'location': configuration.LOCATION,
            'size': 1
        }
    }


def wait_for_completion(conn, promise, msg, wait_timeout=300):
    if not promise:
        return
    wait_timeout = time.time() + wait_timeout
    while wait_timeout > time.time():
        time.sleep(5)
        operation_result = conn.get_request(
            request_id=promise['requestId'],
            status=True)

        if operation_result['metadata']['status'] == "DONE":
            return
        elif operation_result['metadata']['status'] == "FAILED":
            raise Exception(
                'Request failed to complete to complete.'.format(
                    msg, str(promise['requestId']))
            )

    raise Exception(
        'Timed out waiting for async operation {0} msg {1} to '
        'complete'.format(
            msg, str(promise['requestId']))
    )
