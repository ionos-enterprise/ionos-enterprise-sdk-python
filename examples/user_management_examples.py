import os

from profitbricks.client import ProfitBricksService, Group, User

# Instantiate ProfitBricks connection
client = ProfitBricksService(
    username=os.getenv('PROFITBRICKS_USERNAME'),
    password=os.getenv('PROFITBRICKS_PASSWORD'))

"""Create a group
"""
request = Group(
    name='demo-group',
    create_datacenter=True,
    create_snapshot=False,
    reserve_ip=True,
    access_activity_log=False)

group = client.create_group(request)

"""List groups
"""
groups = client.list_groups()

"""Create a user
"""
user_request = User(
    firstname='John',
    lastname='Doe',
    email='demo-user@example.com',
    password='SecretPassword123',
    administrator=True,
    force_sec_auth=False)

user = client.create_user(user_request)

"""List users
"""
users = client.list_users()

"""Add user to group
"""
# gu = client.add_group_user(group_id=group['id'], user_id=user['id'])
# print json.dumps(gu, indent=4)

"""List group users
"""
gus = client.list_group_users(group_id=group['id'])

"""Delete group
"""
response = client.delete_group(group['id'])

"""Delete user
"""
response = client.delete_user(user['id'])

"""List all resources
"""
# listing all resources under an admin user may take a while
resources = client.list_resources()

"""List ipblock resources
"""
ipblock_resources = client.list_resources(resource_type='ipblock')
