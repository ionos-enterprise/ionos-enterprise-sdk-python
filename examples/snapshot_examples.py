"""List Snapshots
"""
from profitbricks.client import ProfitBricksService

client = ProfitBricksService(
    username='username', password='password')

snapshots = client.list_snapshots()

for s in snapshots['items']:
    print s['properties']['name']

"""Get Snapshot
"""
from profitbricks.client import ProfitBricksService

snapshot_id = '7df81087-5835-41c6-a10b-3e098593bba4'
# datacenter_id = '700e1cab-99b2-4c30-ba8c-1d273ddba022'

client = ProfitBricksService(
    username='username', password='password')

snapshot = client.get_snapshot(
    snapshot_id=snapshot_id)

"""Remove Snapshot
"""

from profitbricks.client import ProfitBricksService

snapshot_id = '7df81087-5835-41c6-a10b-3e098593bba4'

client = ProfitBricksService(
    username='username', password='password')

snapshot = client.delete_snapshot(
    snapshot_id=snapshot_id)