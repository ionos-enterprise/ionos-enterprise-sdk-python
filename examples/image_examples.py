"""List Images
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

images = client.list_images()

print(images)

"""Update Image
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'
image = client.update_image(
    image_id,
    name='New name')

"""Delete Image
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'

image = client.delete_image(image_id)
