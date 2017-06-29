import unittest

from helpers import configuration
from helpers.resources import resource
from profitbricks.client import ProfitBricksService
from profitbricks.errors import PBNotFoundError
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
            if (configuration.IMAGE_NAME in item['properties']['name'] and
                    item['properties']['location'] == configuration.LOCATION):
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
        assertRegex(self, image['id'], self.resource['uuid_match'])
        self.assertGreater(len(image['properties']['name']), 0)
        self.assertIsNone(image['properties']['description'])
        self.assertGreater(image['properties']['size'], 0)
        self.assertNotEquals(image['properties']['name'], "")
        self.assertIn(image['properties']['location'], self.resource['locations'])
        self.assertIn(image['properties']['licenceType'], self.resource['licence_type'])
        self.assertIn(image['properties']['imageType'], ['HDD', 'CDROM'])
        self.assertIsInstance(image['properties']['imageAliases'], list)
        self.assertIsInstance(image['properties']['cpuHotPlug'], bool)
        self.assertIsInstance(image['properties']['cpuHotUnplug'], bool)
        self.assertIsInstance(image['properties']['ramHotPlug'], bool)
        self.assertIsInstance(image['properties']['ramHotUnplug'], bool)
        self.assertIsInstance(image['properties']['nicHotPlug'], bool)
        self.assertIsInstance(image['properties']['nicHotUnplug'], bool)
        self.assertIsInstance(image['properties']['discVirtioHotPlug'], bool)
        self.assertIsInstance(image['properties']['discVirtioHotUnplug'], bool)
        self.assertIsInstance(image['properties']['discScsiHotPlug'], bool)
        self.assertIsInstance(image['properties']['discScsiHotUnplug'], bool)
        self.assertIsInstance(image['properties']['public'], bool)

    def test_get_failure(self):
        try:
            self.client.get_image('00000000-0000-0000-0000-000000000000')
        except PBNotFoundError as e:
            self.assertIn(self.resource['not_found_error'], e.content[0]['message'])

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
