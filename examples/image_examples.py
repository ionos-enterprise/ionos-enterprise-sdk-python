"""List Images
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

images = client.list_images()

print(images)

"""
Update Image

Valid image parameters are:

* name (str)
* description (str)
* licence_type (one of 'LINUX', 'WINDOWS' or 'UNKNOWN')
* cpu_hot_plug (bool)
* ram_hot_plug (bool)
* nic_hot_plug (bool)
* nic_hot_unplug (bool)
* disc_virtio_hot_plug (bool)
* disc_virtio_hot_unplug (bool)
* disc_scsi_hot_plug (bool)
* disc_scsi_hot_unplug (bool)

"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'
image = client.update_image(
    image_id,
    name='New name',
    description="Centos 7 with NGnix",
    licence_type='LINUX',
    cpu_hot_plug=True,
    ram_hot_plug=True,
    nic_hot_plug=True,
    nic_hot_unplug=True,
    disc_virtio_hot_plug=True,
    disc_virtio_hot_unplug=True)

"""Delete Image
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

image_id = '7df81087-5835-41c6-a10b-3e098593bbd2'

image = client.delete_image(image_id)
