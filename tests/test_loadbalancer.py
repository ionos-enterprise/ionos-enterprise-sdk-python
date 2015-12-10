import unittest

from profitbricks.client import ProfitBricksService, LoadBalancer

loadbalancer_id = '<LB-ID>'
nic_id = '<NIC-ID>'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'


class TestLoadBalancer(unittest.TestCase):
    def setUp(self):
        self.loadbalancer = ProfitBricksService(username='username', password='password')

    def test_get_all(self):
        loadbalancers = self.loadbalancer.list_loadbalancers(
            datacenter_id=datacenter_id)

        self.assertEqual(len(loadbalancers), 4)
        self.assertEqual(loadbalancers['items'][0]['id'], loadbalancer_id)
        self.assertEqual(loadbalancers['items'][0]['properties']['name'], 'My LB')

    def test_get_loadbalancer(self):
        loadbalancer = self.loadbalancer.get_loadbalancer(
            datacenter_id=datacenter_id,
            loadbalancer_id=loadbalancer_id)

        self.assertEqual(loadbalancer['properties']['name'], 'My LB')
        self.assertEqual(loadbalancer['properties']['ip'], '10.2.2.3')
        self.assertTrue(loadbalancer['properties']['dhcp'])

    def test_delete_loadbalancer(self):
        loadbalancer = self.loadbalancer.delete_loadbalancer(
            datacenter_id=datacenter_id,
            loadbalancer_id=loadbalancer_id)

        self.assertTrue(loadbalancer)

    def test_update_loadbalancer(self):
        loadbalancer = self.loadbalancer.update_loadbalancer(
            datacenter_id=datacenter_id,
            loadbalancer_id=loadbalancer_id,
            ip='10.2.2.4')

        self.assertEqual(loadbalancer['properties']['name'], 'My LB')
        self.assertEqual(loadbalancer['properties']['ip'], '10.2.2.4')
        self.assertTrue(loadbalancer['properties']['dhcp'])

    def test_create_loadbalancer(self):
        i = LoadBalancer(
            name='My LB')

        response = self.loadbalancer.create_loadbalancer(
            datacenter_id=datacenter_id, loadbalancer=i)

        self.assertEqual(response['properties']['name'], 'My LB')
        self.assertEqual(response['properties']['ip'], '10.2.2.3')
        self.assertTrue(response['properties']['dhcp'])

    def test_create_with_balancednics(self):
        balancednics = ['<NIC-ID-1>', '<NIC-ID-2>']

        i = LoadBalancer(
            name='My LB',
            balancednics=balancednics)

        response = self.loadbalancer.create_loadbalancer(
            datacenter_id=datacenter_id, loadbalancer=i)

        self.assertEqual(response['properties']['name'], 'My LB')
        self.assertEqual(response['properties']['ip'], '10.2.2.3')
        self.assertTrue(response['properties']['dhcp'])

    def test_create_optional_value(self):
        i = LoadBalancer(
            name='My LB',
            ip='10.2.2.3',
            dhcp=True)

        response = self.loadbalancer.create_loadbalancer(
            datacenter_id=datacenter_id, loadbalancer=i)

        self.assertEqual(response['properties']['name'], 'My LB')
        self.assertEqual(response['properties']['ip'], '10.2.2.3')
        self.assertTrue(response['properties']['dhcp'])

    def test_get_loadbalancer_members(self):
        members = self.loadbalancer.get_loadbalancer_members(
            datacenter_id=datacenter_id,
            loadbalancer_id=loadbalancer_id)

        self.assertEqual(len(members), 4)
        self.assertEqual(members['items'][0]['id'], '<NIC-ID>')
        self.assertEqual(members['items'][0]['properties']['name'], 'nic1')
        self.assertEqual(
            members['items'][0]['properties']['mac'], 'AB:21:23:09:78:C2')

    def test_add_loadbalanced_nic(self):
        nic = '<NIC-ID-1'

        response = self.loadbalancer.add_loadbalanced_nics(
            datacenter_id=datacenter_id,
            loadbalancer_id=loadbalancer_id,
            nic_id=nic)

        self.assertEqual(response['properties']['name'], 'nic1')
        self.assertEqual(response['properties']['mac'], 'AB:21:23:09:78:C2')
        self.assertTrue(response['properties']['dhcp'])

    def test_get_balanced_nic(self):
        response = self.loadbalancer.get_loadbalanced_nic(
            datacenter_id=datacenter_id,
            loadbalancer_id=loadbalancer_id,
            nic_id=nic_id)

        self.assertEqual(response['properties']['name'], 'nic1')
        self.assertEqual(response['properties']['mac'], 'AB:21:23:09:78:C2')
        self.assertTrue(response['properties']['dhcp'])

    def test_remove_balanced_nic(self):
        loadbalancer = self.loadbalancer.remove_loadbalanced_nic(
            datacenter_id=datacenter_id,
            loadbalancer_id=loadbalancer_id,
            nic_id=nic_id)

        self.assertTrue(loadbalancer)

if __name__ == '__main__':
    unittest.main()
