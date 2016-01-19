import unittest

from profitbricks.client import ProfitBricksService
from helpers import configuration
from helpers.resources import resource


class TestImage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME, password=configuration.PASSWORD)

        # Find an Ubuntu image for testing.
        for item in self.client.list_images()['items']:
            # if item['id'] == '2f98b678-6e7e-11e5-b680-52540066fee9': # Custom image used due to existing REST API public image bug
            if 'Ubuntu-15' in item['properties']['name'] and item['properties']['location'] == self.resource['location']:
                self.image = item

    def test_list_images(self):
        images = self.client.list_images()

        self.assertGreater(len(images), 0)
        self.assertEqual(images['items'][0]['type'], 'image')
        self.assertRegexpMatches(images['items'][0]['id'], self.resource['uuid_match'])

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
