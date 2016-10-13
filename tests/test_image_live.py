import unittest

from helpers import configuration
from helpers.resources import resource
from profitbricks.client import ProfitBricksService
from six import assertRegex


class TestImage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Find an Ubuntu image for testing.
        for item in self.client.list_images()['items']:
            if configuration.IMAGE_NAME in item['properties']['name'] and item['properties'][
                'location'] == configuration.LOCATION:
                self.image = item

    def test_list_images(self):
        images = self.client.list_images()

        assertRegex(self, images['items'][0]['id'], self.resource['uuid_match'])
        self.assertGreater(len(images), 0)
        self.assertEqual(images['items'][0]['type'], 'image')
        self.assertTrue(self, len(images['items']) > 0)

    def test_get_image(self):
        image = self.client.get_image(self.image['id'])

        self.assertEqual(image['type'], 'image')
        self.assertEqual(image['id'], self.image['id'])
        self.assertIn(image['properties']['imageType'], ['HDD', 'CDROM'])

        # A custom image would need to be uploaded and referenced to perform the
        # following tests. Skipping for now.

        # def test_delete_image(self):
        #     image = self.client.delete_image(image_id)
        #     self.assertTrue(image)

        # def test_update_image(self):
        #     image = self.client.update_image(
        #         image_id,
        #         name='New name')
        #    self.assertEqual(image['properties']['name'], 'New name')


if __name__ == '__main__':
    unittest.main()
