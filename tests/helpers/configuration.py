# Copyright 2015-2017 IONOS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

# Default settings for testing.
LOCATION = os.getenv('IONOS_LOCATION', 'us/las')
IMAGE_NAME = 'Ubuntu-16'  # Note: Partial image name and case sensitive

# Custom HTTP headers
# Connection: close - prevents resource warnings in Python 3.4
HEADERS = {'Connection': 'close'}

# Import environment variables for credentials.
try:
    USERNAME = os.environ['IONOS_USERNAME']
except KeyError:
    raise Exception('Please set the environment variable IONOS_USERNAME')

try:
    PASSWORD = os.environ['IONOS_PASSWORD']
except KeyError:
    raise Exception('Please set the environment variable IONOS_PASSWORD')
