import unittest

from profitbricks.client import ProfitBricksService


class TestImage(unittest.TestCase):
    def setUp(self):
        self.image = ProfitBricksService(
            username='username', password='password')

    def test_list_images(self):
        images = self.image.list_images()

        self.assertEqual(len(images), 4)
        self.assertEqual(
            images['items'][0]['id'], '7df81087-5835-41c6-a10b-3e098593bbd2')

    def test_get_image(self):
        image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'
        image = self.image.get_image(image_id)

        self.assertEqual(image['properties']['name'], 'Ubuntu 14.04')

    def test_delete_image(self):
        image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'

        image = self.image.delete_image(image_id)
        self.assertTrue(image)

    def test_update_image(self):
        image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'
        image = self.image.update_image(
            image_id,
            name='New name')

        self.assertEqual(image['properties']['name'], 'New name')

if __name__ == '__main__':
    unittest.main()
