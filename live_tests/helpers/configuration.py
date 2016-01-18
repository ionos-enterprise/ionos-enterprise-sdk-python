import os
import sys

LOCATION = os.getenv('PROFITBRICKS_LOCATION', 'us/lasdev')

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
