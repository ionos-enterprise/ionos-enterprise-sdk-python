import unittest

from profitbricks.client import ProfitBricksService, LAN

lan_id = '4'
datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'


class TestLan(unittest.TestCase):
    def setUp(self):
        self.lan = ProfitBricksService(username='username', password='password')

    def test_list_lans(self):
        lans = self.lan.list_lans(datacenter_id=datacenter_id)

        self.assertEqual(len(lans), 4)
        self.assertEqual(lans['items'][0]['id'], lan_id)
        self.assertEqual(lans['items'][0]['properties']['name'], 'public Lan 4')

    def test_get_lan(self):
        lan = self.lan.get_lan(datacenter_id=datacenter_id, lan_id=lan_id)

        self.assertEqual(lan['properties']['name'], 'public Lan 4')
        self.assertTrue(lan['properties']['public'])

    def test_delete_lan(self):
        lan = self.lan.delete_lan(datacenter_id=datacenter_id, lan_id=lan_id)
        self.assertTrue(lan)

    def test_update_lan(self):
        lan = self.lan.update_lan(datacenter_id=datacenter_id,
                                  lan_id=lan_id,
                                  name='new lan 4 name',
                                  public=False)

        self.assertEqual(lan['properties']['name'], 'public Lan 4')
        self.assertTrue(lan['properties']['public'])

    def test_create_lan(self):
        i = LAN(
            name='public Lan 4',
            public=True)

        response = self.lan.create_lan(datacenter_id=datacenter_id, lan=i)

        self.assertEqual(response['properties']['name'], 'public Lan 4')
        self.assertTrue(response['properties']['public'])

    def test_create_complex_lan(self):
        nics = ['<NIC-ID-1>', '<NIC-ID-2>']

        i = LAN(
            name='public Lan 4',
            public=True,
            nics=nics)

        response = self.lan.create_lan(datacenter_id=datacenter_id, lan=i)

        self.assertEqual(response['properties']['name'], 'public Lan 4')
        self.assertTrue(response['properties']['public'])

    def test_get_lan_members(self):
        members = self.lan.get_lan_members(datacenter_id=datacenter_id,
                                           lan_id=lan_id)

        self.assertEqual(len(members), 4)
        self.assertEqual(members['items'][0]['id'], '<NIC-ID>')
        self.assertEqual(members['items'][0]['properties']['name'], 'nic1')
        self.assertEqual(members['items'][0]['properties']['mac'], 'AB:21:23:09:78:C2')

if __name__ == '__main__':
    unittest.main()
