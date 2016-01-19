import unittest

from profitbricks.client import ProfitBricksService
from profitbricks.client import Datacenter, Volume, Server
from profitbricks.client import LAN, NIC, LoadBalancer, FirewallRule

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'


class TestDatacenter(unittest.TestCase):
    def setUp(self):
        self.datacenter = ProfitBricksService(
            username='username', password='password')

    def test_get_all(self):
        datacenters = self.datacenter.list_datacenters()

        self.assertEqual(len(datacenters), 4)
        self.assertEqual(datacenters['items'][0]['id'], datacenter_id)
        # self.assertEqual(
        #     datacenters['items'][0]['properties']['name'], 'datacenter1')
        # self.assertEqual(
        #     datacenters['items'][0]['properties']['description'], 'Description of my DC')
        # self.assertEqual(
        #     datacenters['items'][0]['properties']['location'], 'de/fkb')
        # self.assertEqual(
        #     datacenters['items'][0]['properties']['version'], 4)

    def test_get(self):
        datacenter = self.datacenter.get_datacenter(
            datacenter_id=datacenter_id)

        self.assertEqual(datacenter['id'], datacenter_id)
        self.assertEqual(datacenter['properties']['name'], 'datacenter1')
        self.assertEqual(datacenter['properties']['description'], 'Description of my DC')
        self.assertEqual(datacenter['properties']['version'], 4)
        self.assertEqual(datacenter['properties']['location'], 'de/fkb')

    def test_delete(self):
        datacenter = self.datacenter.delete_datacenter(
            datacenter_id=datacenter_id)

        self.assertTrue(datacenter)

    def test_update(self):
        datacenter = self.datacenter.update_datacenter(
            datacenter_id=datacenter_id,
            name='Partially updated datacenter name')

        self.assertEqual(datacenter['id'], datacenter_id)
        self.assertEqual(datacenter['properties']['name'], 'datacenter1')
        self.assertEqual(datacenter['properties']['description'], 'Description of my DC')
        self.assertEqual(datacenter['properties']['version'], 4)
        self.assertEqual(datacenter['properties']['location'], 'de/fkb')

    def test_create_simple(self):
        i = Datacenter(
            name='datacenter1',
            description='My New Datacenter',
            location='de/fkb'
            )

        response = self.datacenter.create_datacenter(datacenter=i)

        self.assertEqual(response['id'], datacenter_id)
        self.assertEqual(response['properties']['name'], 'datacenter1')
        self.assertEqual(response['properties']['description'], 'My New Datacenter')
        self.assertEqual(response['properties']['version'], 4)
        self.assertEqual(response['properties']['location'], 'de/fkb')

    def test_create_complex(self):
        """
        Creates a complex Datacenter in a single request.

        """
        fwrule1 = FirewallRule(
            name='Open SSH port',
            protocol='TCP',
            source_mac='01:23:45:67:89:00',
            port_range_start=22
            )

        fwrule2 = FirewallRule(
            name='Allow PING',
            protocol='ICMP',
            icmp_type=8,
            icmp_code=0
            )

        fw_rules = [fwrule1, fwrule2]

        nic1 = NIC(
            name='nic1',
            ips=['10.2.2.3'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            firewall_rules=fw_rules
            )

        nic2 = NIC(
            name='nic2',
            ips=['10.2.3.4'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            firewall_rules=fw_rules
            )

        nics = [nic1, nic2]

        volume1 = Volume(
            name='volume1',
            size=56,
            image='<IMAGE/SNAPSHOT-ID>',
            bus='VIRTIO'
            )

        volume2 = Volume(
            name='volume2',
            size=56,
            image='<IMAGE/SNAPSHOT-ID>',
            bus='VIRTIO'
            )

        volumes = [volume2]

        server1 = Server(
            name='server1',
            ram=4096,
            cores=4,
            nics=nics,
            create_volumes=[volume1]
            )

        servers = [server1]

        balancednics = ['<NIC-ID-1>', '<NIC-ID-2>']

        loadbalancer1 = LoadBalancer(
            name='My LB',
            balancednics=balancednics)

        loadbalancers = [loadbalancer1]

        lan1 = LAN(
            name='public Lan 4',
            public=True
            )

        lan2 = LAN(
            name='public Lan 4',
            public=True
            )

        lans = [lan1, lan2]

        d = Datacenter(
            name='datacenter1',
            description='my DC',
            location='de/fkb',
            servers=servers,
            volumes=volumes,
            loadbalancers=loadbalancers,
            lans=lans
            )

        response = self.datacenter.create_datacenter(datacenter=d)
        print(response)

        self.assertEqual(response['id'], datacenter_id)
        self.assertEqual(response['properties']['name'], 'My New Datacenter')
        self.assertEqual(response['properties']['description'], 'Production environment')
        self.assertEqual(response['properties']['version'], 4)
        self.assertEqual(response['properties']['location'], 'de/fkb')

if __name__ == '__main__':
    unittest.main()
