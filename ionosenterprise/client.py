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

import getpass
import logging
import os
import sys
import re
import time
import requests
import six

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

try:
    import keyring
    HAS_KEYRING = True
except ImportError:
    HAS_KEYRING = False

from ionosenterprise import (
    API_HOST, __version__
)

from ionosenterprise.errors import (
    ICNotAuthorizedError,
    ICNotFoundError,
    ICValidationError,
    ICRateLimitExceededError,
    ICError,
    ICFailedRequest,
    ICTimeoutError,
)

from .utils import ask

from .requests import IonosEnterpriseRequests

from .items import * # NOQA

_LIBRARY_NAME = "ionosenterprise-sdk-python"


# IonosEnterprise Object Classes
class IonosEnterpriseService(IonosEnterpriseRequests):
    """
        IonosEnterpriseClient Base Class
    """

    def __init__(self, username=None, password=None, host_base=API_HOST,
                 host_cert=None, ssl_verify=True, headers=None, client_user_agent=None,
                 use_config=True, use_keyring=HAS_KEYRING, config_filename=None):
        if headers is None:
            headers = dict()
        self._config = None
        self._config_filename = None
        self.keyring_identificator = '%s (%s)' % (re.sub(r"/v\d+$", '', host_base), _LIBRARY_NAME)
        self.host_base = host_base
        self.host_cert = host_cert
        self.verify = ssl_verify
        self.headers = headers
        self.username = self._get_username(username, use_config, config_filename)
        self.password = self._get_password(password, use_config, config_filename, use_keyring)
        self.user_agent = '{}/{}'.format(_LIBRARY_NAME, __version__)
        if client_user_agent:
            self.user_agent = client_user_agent + ' ' + self.user_agent

    def _read_config(self, filename=None):
        """
        Read the user configuration
        """
        if filename:
            self._config_filename = filename
        else:
            try:
                import appdirs
            except ImportError:
                raise Exception("Missing dependency for determining config path. Please install "
                                "the 'appdirs' Python module.")
            self._config_filename = appdirs.user_config_dir(_LIBRARY_NAME, "IonosEnterprise") + ".ini"
        if not self._config:
            self._config = configparser.ConfigParser()
            self._config.optionxform = str
            self._config.read(self._config_filename)

    def _save_config(self, filename=None):
        """
        Save the given user configuration.
        """
        if filename is None:
            filename = self._config_filename
        parent_path = os.path.dirname(filename)
        if not os.path.isdir(parent_path):
            os.makedirs(parent_path)
        with open(filename, "w") as configfile:
            self._config.write(configfile)

    def _get_username(self, username=None, use_config=True, config_filename=None):
        """Determine the username

        If a username is given, this name is used. Otherwise the configuration
        file will be consulted if `use_config` is set to True. The user is asked
        for the username if the username is not available. Then the username is
        stored in the configuration file.

        :param      username: Username (used directly if given)
        :type       username: ``str``

        :param      use_config: Whether to read username from configuration file
        :type       use_config: ``bool``

        :param      config_filename: Path to the configuration file
        :type       config_filename: ``str``

        """
        if not username and use_config:
            if self._config is None:
                self._read_config(config_filename)
            username = self._config.get("credentials", "username", fallback=None)

        if not username:
            username = input("Please enter your username: ").strip()
            while not username:
                username = input("No username specified. Please enter your username: ").strip()
            if 'credendials' not in self._config:
                self._config.add_section('credentials')
            self._config.set("credentials", "username", username)
            self._save_config()

        return username

    def _get_password(self, password, use_config=True, config_filename=None,
                      use_keyring=HAS_KEYRING):
        """
        Determine the user password

        If the password is given, this password is used. Otherwise
        this function will try to get the password from the user's keyring
        if `use_keyring` is set to True.

        :param      username: Username (used directly if given)
        :type       username: ``str``

        :param      use_config: Whether to read username from configuration file
        :type       use_config: ``bool``

        :param      config_filename: Path to the configuration file
        :type       config_filename: ``str``

        """
        if not password and use_config:
            if self._config is None:
                self._read_config(config_filename)
            password = self._config.get("credentials", "password", fallback=None)

        if not password and use_keyring:
            logger = logging.getLogger(__name__)
            question = ("Please enter your password for {} on {}: "
                        .format(self.username, self.host_base))
            if HAS_KEYRING:
                password = keyring.get_password(self.keyring_identificator, self.username)
                if password is None:
                    password = getpass.getpass(question)
                    try:
                        keyring.set_password(self.keyring_identificator, self.username, password)
                    except keyring.errors.PasswordSetError as error:
                        logger.warning("Storing password in keyring '%s' failed: %s",
                                       self.keyring_identificator, error)
            else:
                logger.warning("Install the 'keyring' Python module to store your password "
                               "securely in your keyring!")
                password = self._config.get("credentials", "password", fallback=None)
                if password is None:
                    password = getpass.getpass(question)
                    store_plaintext_passwords = self._config.get(
                        "preferences", "store-plaintext-passwords", fallback=None)
                    if store_plaintext_passwords != "no":
                        question = ("Do you want to store your password in plain text in " +
                                    self._config_filename())
                        answer = ask(question, ["yes", "no", "never"], "no")
                        if answer == "yes":
                            self._config.set("credentials", "password", password)
                            self._save_config()
                        elif answer == "never":
                            if "preferences" not in self._config:
                                self._config.add_section("preferences")
                            self._config.set("preferences", "store-plaintext-passwords", "no")
                            self._save_config()

        return password

    def wait_for(
        self, fn_check, fn_request, timeout=3600, initial_wait=5,
        scaleup=10, console_print=None
    ):
        """
        Poll resource request status until resource is provisioned.

        :param      fn_check: Function used to check the response
        :type       fn_check: ``function``

        :param      fn_request: Function used to perform the request
        :type       fn_request: ``function``

        :param      timeout: Maximum waiting time in seconds. None means infinite waiting time.
        :type       timeout: ``int``

        :param      initial_wait: Initial polling interval in seconds.
        :type       initial_wait: ``int``

        :param      scaleup: Double polling interval every scaleup steps, which will be doubled.
        :type       scaleup: ``int``

        """
        logger = logging.getLogger(__name__)
        wait_period = initial_wait
        next_increase = time.time() + wait_period * scaleup
        if timeout:
            timeout = time.time() + timeout
        while True:
            if console_print is not None:
                sys.stdout.write(console_print)
                sys.stdout.flush()

            resp = fn_request()
            check_response = fn_check(resp)

            if check_response:
                break

            current_time = time.time()
            if timeout and current_time > timeout:
                raise ICTimeoutError('Timed out waiting for request {0}.'.format(
                    resp['requestId']), resp['requestId'])

            if current_time > next_increase:
                wait_period *= 2
                next_increase = time.time() + wait_period * scaleup
                scaleup *= 2

            logger.info("Sleeping for %i seconds...", wait_period)
            time.sleep(wait_period)

        if console_print is not None:
            print('')

        return resp

    def wait_for_completion(self, response, timeout=3600, initial_wait=5, scaleup=10):
        """
        Poll resource request status until resource is provisioned.

        :param      response: A response dict, which needs to have a 'requestId' item.
        :type       response: ``dict``

        :param      timeout: Maximum waiting time in seconds. None means infinite waiting time.
        :type       timeout: ``int``

        :param      initial_wait: Initial polling interval in seconds.
        :type       initial_wait: ``int``

        :param      scaleup: Double polling interval every scaleup steps, which will be doubled.
        :type       scaleup: ``int``

        """
        if not response:
            return
        logger = logging.getLogger(__name__)
        wait_period = initial_wait
        next_increase = time.time() + wait_period * scaleup
        if timeout:
            timeout = time.time() + timeout
        while True:
            request = self.get_request(request_id=response['requestId'], status=True)

            if request['metadata']['status'] == 'DONE':
                break
            elif request['metadata']['status'] == 'FAILED':
                raise ICFailedRequest(
                    'Request {0} failed to complete: {1}'.format(
                        response['requestId'], request['metadata']['message']),
                    response['requestId']
                )

            current_time = time.time()
            if timeout and current_time > timeout:
                raise ICTimeoutError('Timed out waiting for request {0}.'.format(
                    response['requestId']), response['requestId'])

            if current_time > next_increase:
                wait_period *= 2
                next_increase = time.time() + wait_period * scaleup
                scaleup *= 2

            logger.info("Request %s is in state '%s'. Sleeping for %i seconds...",
                        response['requestId'], request['metadata']['status'], wait_period)
            time.sleep(wait_period)

    def _wrapped_request(self, method, url,
                         params=None,
                         data=None,
                         headers=None,
                         cookies=None,
                         files=None,
                         auth=None,
                         timeout=None,
                         allow_redirects=True,
                         proxies=None,
                         hooks=None,
                         stream=None):

        headers.update(self.headers)
        session = requests.Session()
        return session.request(method, url, params, data, headers, cookies,
                               files, auth, timeout, allow_redirects, proxies,
                               hooks, stream, self.verify, self.host_cert)

    def _perform_request(self, url, method='GET', data=None, headers=None):
        if headers is None:
            headers = dict()

        auth = (self.username, self.password)

        url = self._build_url(url)
        headers.update({'User-Agent': self.user_agent})
        if method == 'POST' or method == 'PUT':
            response = self._wrapped_request(method, url, auth=auth, data=data,
                                             headers=headers)
            headers.update({'Content-Type': 'application/json'})
        elif method == 'POST-ACTION-JSON' or method == 'POST-ACTION':
            headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
            response = self._wrapped_request('POST', url, auth=auth, data=data,
                                             headers=headers)
            if response.status_code == 202 and method == 'POST-ACTION':
                return True
            elif response.status_code == 401:
                raise response.raise_for_status()
        elif method == 'PATCH':
            headers.update({'Content-Type': 'application/json'})
            response = self._wrapped_request(method, url, auth=auth, data=data,
                                             headers=headers)
        else:
            headers.update({'Content-Type': 'application/json'})
            response = self._wrapped_request(method, url, auth=auth, params=data,
                                             headers=headers)

        try:
            if not response.ok:
                err = response.json()
                code = err['httpStatus']
                msg = err['messages']
                if response.status_code == 401:
                    raise ICNotAuthorizedError(code, msg, url)
                if response.status_code == 404:
                    raise ICNotFoundError(code, msg, url)
                if response.status_code == 422:
                    raise ICValidationError(code, msg, url)
                if response.status_code == 429:
                    raise ICRateLimitExceededError(code, msg, url)
                else:
                    raise ICError(code, msg, url)

        except ValueError:
            raise Exception('Failed to parse the response', response.text)

        if method == 'DELETE':
            # response content is empty for DELETE
            # set json_response to dict to return the request ID
            json_response = dict()
        else:
            json_response = response.json()

        if 'location' in response.headers:
            json_response['requestId'] = self._request_id(response.headers)

        return json_response

    @staticmethod
    def _request_id(headers):
        # The request URL has currently the format:
        # {host_base}/requests/{request ID}/status
        # Thus search for a UUID.
        match = re.search('/requests/([-A-Fa-f0-9]+)/', headers['location'])
        if match:
            return match.group(1)
        else:
            raise Exception("Failed to extract request ID from response "
                            "header 'location': '{location}'".format(location=headers['location']))

    def _build_url(self, uri):
        url = self.host_base + uri
        return url

    @staticmethod
    def _b(s, encoding='utf-8'):
        """
        Returns the given string as a string of bytes. That means in
        Python2 as a str object, and in Python3 as a bytes object.
        Raises a TypeError, if it cannot be converted.
        """
        if six.PY2:
            # This is Python2
            if isinstance(s, str):
                return s
            elif isinstance(s, unicode):  # noqa, pylint: disable=undefined-variable
                return s.encode(encoding)
        else:
            # And this is Python3
            if isinstance(s, bytes):
                return s
            elif isinstance(s, str):
                return s.encode(encoding)

        raise TypeError("Invalid argument %r for _b()" % (s,))

    @staticmethod
    def _underscore_to_camelcase(value):
        """
        Convert Python snake case back to mixed case.
        """
        def camelcase():
            yield str.lower
            while True:
                yield str.capitalize

        c = camelcase()
        return "".join(next(c)(x) if x else '_' for x in value.split("_"))
