import unittest

from profitbricks.client import ProfitBricksService, FirewallRule

server_id = '700e1cab-99b2-4c30-ba8c-1d273ddba023'
nic_id = '<NIC-ID>'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
firewall_rule_id = '<RULE1-ID>'


class TestFirewall(unittest.TestCase):
    def setUp(self):
        self.firewall = ProfitBricksService(username='username', password='password')

    def test_get_all(self):
        firewalls = self.firewall.get_firewall_rules(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id)

        self.assertEqual(len(firewalls), 4)
        self.assertEqual(firewalls['items'][0]['id'], firewall_rule_id)
        self.assertEqual(firewalls['items'][0]['properties']['name'], 'Open SSH port')
        self.assertEqual(firewalls['items'][0]['properties']['portRangeStart'], 22)

    def test_get(self):
        firewall = self.firewall.get_firewall_rule(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id,
            firewall_rule_id=firewall_rule_id)

        self.assertEqual(firewall['id'], firewall_rule_id)
        self.assertEqual(firewall['properties']['name'], 'Open SSH port')
        self.assertEqual(firewall['properties']['portRangeStart'], 22)

    def test_delete(self):
        firewall = self.firewall.delete_firewall_rule(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id,
            firewall_rule_id=firewall_rule_id)

        self.assertTrue(firewall)

    def test_update(self):
        firewall = self.firewall.update_firewall_rule(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id,
            firewall_rule_id=firewall_rule_id,
            source_mac='01:98:22:22:44:22',
            target_ip='123.100.101.102')

        self.assertEqual(firewall['id'], firewall_rule_id)
        self.assertEqual(firewall['properties']['name'], 'Open SSH port')
        self.assertEqual(firewall['properties']['portRangeStart'], 22)
        self.assertEqual(
            firewall['properties']['sourceMac'], '01:98:22:22:44:22')
        self.assertEqual(
            firewall['properties']['targetIp'], '123.100.101.102')

    def test_create(self):
        i = FirewallRule(
            name='Open SSH port',
            protocol='TCP'
            )

        response = self.firewall.create_firewall_rule(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id,
            firewall_rule=i)

        self.assertEqual(response['id'], firewall_rule_id)
        self.assertEqual(response['properties']['name'], 'Open SSH port')
        self.assertEqual(response['properties']['portRangeStart'], 22)
        self.assertEqual(response['properties']['protocol'], 'TCP')
        self.assertEqual(
            response['properties']['sourceMac'], '01:23:45:67:89:00')

    def test_create_optional_value(self):
        i = FirewallRule(
            name='Open SSH port',
            protocol='TCP',
            source_mac='01:23:45:67:89:00',
            source_ip='12.2.11.22',
            port_range_start=22,
            port_range_end=1000
            )

        response = self.firewall.create_firewall_rule(
            datacenter_id=datacenter_id,
            server_id=server_id,
            nic_id=nic_id,
            firewall_rule=i)

        self.assertEqual(response['id'], firewall_rule_id)
        self.assertEqual(response['properties']['name'], 'Open SSH port')
        self.assertEqual(response['properties']['portRangeStart'], 22)
        self.assertEqual(response['properties']['protocol'], 'TCP')

if __name__ == '__main__':
    unittest.main()
