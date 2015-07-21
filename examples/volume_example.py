"""Create volume
"""

from profitbricks.client import ProfitBricksService, Volume

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = ProfitBricksService(
    username='username', password='password')

i = Volume(
    name='Explicitly created volume',
    size=56,
    image='<IMAGE/SNAPSHOT-ID>',
    bus='VIRTIO')

response = client.create_volume(
    datacenter_id=datacenter_id, volume=i)

"""Create snapshot
"""

from profitbricks.client import ProfitBricksService

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'

client = ProfitBricksService(
    username='username', password='password')

volume = client.create_snapshot(
    datacenter_id=datacenter_id,
    volume_id=volume_id,
    snapshot_name='<URLENCODED_SNAPSHOT_NAME>',
    snapshot_description='<URLENCODED_SNAPSHOT_DESCRIPTION>')

"""Restore Snapshot
"""
from profitbricks.client import ProfitBricksService

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'
snapshot_id = '7df81087-5835-41c6-a10b-3e098593bba4'


client = ProfitBricksService(
    username='username', password='password')

response = client.restore_snapshot(
    datacenter_id=datacenter_id,
    volume_id=volume_id,
    snapshot_id=snapshot_id)

"""Update Volume
"""

from profitbricks.client import ProfitBricksService

datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'
volume_id = '700e1cab-99b2-4c30-ba8c-1d273ddba025'

client = ProfitBricksService(
    username='username', password='password')

volume = client.update_volume(
    datacenter_id=datacenter_id,
    volume_id=volume_id,
    size=100,
    name='Resized storage to 100 GB')
