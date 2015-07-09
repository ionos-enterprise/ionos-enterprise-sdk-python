import unittest

from profitbricks.client import ProfitBricksService, IPBlock

ipblock_id = '854467eb-a0d3-4651-ac83-754e2faedba4'


class TestIPBlock(unittest.TestCase):
    def setUp(self):
        self.ipblock = ProfitBricksService(
            username='username', password='password')

    def test_list_ipblocks(self):
        ipblocks = self.ipblock.list_ipblocks()

        self.assertEqual(len(ipblocks), 4)
        self.assertEqual(ipblocks['items'][0]['id'], ipblock_id)
        self.assertEqual(
            ipblocks['items'][0]['properties']['size'], 5)
        self.assertEqual(
            ipblocks['items'][0]['properties']['location'], 'de/fra')

    def test_get_ipblock(self):
        ipblock = self.ipblock.get_ipblock(ipblock_id)

        self.assertEqual(ipblock['id'], ipblock_id)
        self.assertEqual(ipblock['properties']['size'], 5)
        self.assertEqual(
            ipblock['properties']['location'], 'de/fra')

    def test_delete_ipblock(self):
        ipblock = self.ipblock.delete_ipblock(ipblock_id)
        self.assertTrue(ipblock)

    def test_reserve_ipblock(self):
        i = IPBlock(location='de/fra', size=5)

        ipblock = self.ipblock.reserve_ipblock(i)

        self.assertEqual(ipblock['id'], ipblock_id)
        self.assertEqual(ipblock['properties']['size'], 5)
        self.assertEqual(
            ipblock['properties']['location'], 'de/fra')

if __name__ == '__main__':
    unittest.main()
