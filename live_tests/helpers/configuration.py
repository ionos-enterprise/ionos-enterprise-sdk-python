import os
import sys

# Default settings for testing.
LOCATION = os.getenv('PROFITBRICKS_LOCATION', 'us/lasdev')

# Import environment variables for credentials.
try:
    os.environ['PROFITBRICKS_USERNAME']
    USERNAME = os.getenv('PROFITBRICKS_USERNAME')
except KeyError:
    raise Exception('Please set the environment variable PROFITBRICKS_USERNAME')

try:
    os.environ['PROFITBRICKS_PASSWORD']
    PASSWORD = os.getenv('PROFITBRICKS_PASSWORD')
except KeyError:
    raise Exception('Please set the environment variable PROFITBRICKS_PASSWORD')
