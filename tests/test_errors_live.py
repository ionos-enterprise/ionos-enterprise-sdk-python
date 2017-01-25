import unittest

from profitbricks.client import ProfitBricksService, Datacenter, Volume

from profitbricks.errors import PBError, PBNotAuthorizedError, PBNotFoundError, PBValidationError
from tests.helpers import configuration
from tests.helpers.resources import resource


class TestErrors(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)
        self.datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_pb_not_found(self):
        try:
            self.client.get_datacenter("fake_id")
        except PBError as err:
            self.assertTrue(isinstance(err, PBNotFoundError))

    def test_pb_unauthorized_error(self):
        try:
            self.client = ProfitBricksService(
                username=configuration.USERNAME + "1",
                password=configuration.PASSWORD,
                headers=configuration.HEADERS)
            self.client.list_datacenters()

        except PBError as err:
            self.assertTrue(isinstance(err, PBNotAuthorizedError))

    def test_pb_validation_error(self):
        try:
            i = Volume(
                name='Explicitly created volume',
                size=5,
                disk_type='HDD',
                image='fake_image_id',
                bus='VIRTIO')
            self.client.create_volume(datacenter_id=self.datacenter['id'], volume=i)
        except PBError as err:
            self.assertTrue(isinstance(err, PBValidationError))


if __name__ == '__main__':
    unittest.main()
