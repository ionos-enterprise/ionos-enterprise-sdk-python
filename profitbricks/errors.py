# Copyright 2015-2017 ProfitBricks GmbH
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


class PBError(Exception):
    """Base error for this module."""
    def __init__(self, resp, content, uri=None):  # pylint: disable=super-init-not-called
        self.resp = resp
        self.content = content
        self.uri = uri


class PBNotAuthorizedError(PBError):
    """The authorization information provided is not correct"""


class PBNotFoundError(PBError):
    """The ProfitBricks entity was not found"""


class PBValidationError(PBError):
    """The HTTP data provided is not valid"""


class PBRateLimitExceededError(PBError):
    """The number of requests sent have exceeded the allowed API rate limit"""


class PBRequestError(Exception):
    """Base error for request failures"""
    def __init__(self, msg, request_id):  # pylint: disable=super-init-not-called
        self.msg = msg
        self.request_id = request_id


class PBFailedRequest(PBRequestError):
    """Raised when a provisioning request failed."""


class PBTimeoutError(PBRequestError):
    """Raised when a request does not finish in the given time span."""
