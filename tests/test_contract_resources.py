import unittest

from helpers import configuration
from profitbricks.client import ProfitBricksService


class TestContractResources(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

    def test_list_contract_resources(self):
        contracts = self.client.list_contracts()

        self.assertEqual(contracts['type'], 'contract')
        self.assertIsInstance(contracts['properties']['contractNumber'], int)


if __name__ == '__main__':
    unittest.main()
