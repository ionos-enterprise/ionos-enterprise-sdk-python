import unittest

from profitbricks.client import ProfitBricksService, FirewallRule, NIC

server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
nic_id = '<NIC-ID>'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'


class TestNIC(unittest.TestCase):
    def setUp(self):
        self.nic = ProfitBricksService(
            username='username', password='password')

    def test_list_nics(self):
        nics = self.nic.list_nics(
            datacenter_id=datacenter_id,
            server_id=server_id)

        self.assertEqual(len(nics), 4)
        self.assertEqual(nics['items'][0]['id'], nic_id)
        self.assertEqual(nics['items'][0]['properties']['name'], 'nic1')
        self.assertEqual(
            nics['items'][0]['properties']['mac'], 'AB:21:23:09:78:C2')
        self.assertEqual(nics['items'][0]['properties']['dhcp'], 'true')
        self.assertEqual(nics['items'][0]['properties']['lan'], 1)

    def test_get_nic(self):
        nic = self.nic.get_nic(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id)

        self.assertEqual(nic['id'], nic_id)
        self.assertEqual(nic['properties']['name'], 'nic1')
        self.assertEqual(nic['properties']['mac'], 'AB:21:23:09:78:C2')
        self.assertEqual(nic['properties']['dhcp'], 'true')
        self.assertEqual(nic['properties']['lan'], 1)

    def test_delete_nic(self):
        nic = self.nic.delete_nic(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id)

        self.assertTrue(nic)

    def test_update_nic(self):
        nic = self.nic.update_nic(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id,
            ips=['10.2.2.3', '10.2.3.4'])

        self.assertEqual(nic['id'], nic_id)
        self.assertEqual(nic['properties']['name'], 'nic1')
        self.assertEqual(nic['properties']['mac'], 'AB:21:23:09:78:C2')
        self.assertEqual(nic['properties']['dhcp'], 'true')
        self.assertEqual(nic['properties']['lan'], 1)

    def test_create_complex(self):
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

        i = NIC(
            name='nic1',
            ips=['10.2.2.3', '10.2.3.4'],
            dhcp='true',
            lan=1,
            firewall_active=True,
            firewall_rules=fw_rules
            )

        response = self.nic.create_nic(
            datacenter_id=datacenter_id,
            server_id=server_id, nic=i)

        self.assertEqual(response['id'], nic_id)
        self.assertEqual(response['properties']['name'], 'nic1')
        self.assertEqual(
            response['properties']['mac'], 'AB:21:23:09:78:C2')
        self.assertEqual(response['properties']['dhcp'], 'true')
        self.assertEqual(response['properties']['lan'], 1)
        self.assertListEqual(
            response['properties']['ips'], ['10.2.2.3'])

    def test_create_simple(self):
        i = NIC(
            name='nic1',
            ips=['10.2.2.3', '10.2.3.4'],
            dhcp='true',
            lan=1,
            firewall_active=True
            )

        response = self.nic.create_nic(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic=i)

        self.assertEqual(response['id'], nic_id)
        self.assertEqual(response['properties']['name'], 'nic1')
        self.assertEqual(
            response['properties']['mac'], 'AB:21:23:09:78:C2')
        self.assertEqual(response['properties']['dhcp'], 'true')
        self.assertEqual(response['properties']['lan'], 1)
        self.assertListEqual(
            response['properties']['ips'], ['10.2.2.3'])

if __name__ == '__main__':
    unittest.main()
