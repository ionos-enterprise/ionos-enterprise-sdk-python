import os

# Default settings for testing.
LOCATION = os.getenv('PROFITBRICKS_LOCATION', 'us/las')
# Custom HTTP headers
# Connection: close - prevents resource warnings in Python 3.4
HEADERS = {'Connection': 'close'}

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
