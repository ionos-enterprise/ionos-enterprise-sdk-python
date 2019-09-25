# Copyright 2015-2017 ProfitBricks GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from profitbricks.client import ProfitBricksService

from helpers import configuration


class TestContractResources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

    def test_list_contract_resources(self):
        contracts = self.client.list_contracts()

        self.assertEqual(contracts['type'], 'contract')
        self.assertIsInstance(contracts['properties']['contractNumber'], int)


if __name__ == '__main__':
    unittest.main()
