from ionoscloud.exceptions import ApiException, ApiTimeout, ApiFailedRequest
from ionosenterprise.errors import (
    ICNotAuthorizedError,
    ICNotFoundError,
    ICValidationError,
    ICRateLimitExceededError,
    ICError,
    ICFailedRequest,
    ICTimeoutError
)
import json
import functools
import re
import inspect

class IonosCoreProxy:

    custom_methods = {
        'start_server': 'POST-ACTION',
        'stop_server': 'POST-ACTION',
        'reboot_server': 'POST-ACTION',
        'restore_snapshot': 'POST-ACTION',
        'create_snapshot': 'POST-ACTION-JSON'
    }

    @staticmethod
    def get_default_args(func):
        signature = inspect.signature(func)
        return {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }

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

    @staticmethod
    def process_response(f):
        @functools.wraps(f)
        def func(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                return IonosCoreProxy.handle_response_operations(f, response)
            except Exception as e:
                raise IonosCoreProxy.cast_exception(e)
        return func

    @staticmethod
    def cast_exceptions(f):
        @functools.wraps(f)
        def func(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if type(e) == ApiException:
                    code = e.status
                    msg = json.loads(e.body)
                    url = e.url
                    if code == 401:
                        raise ICNotAuthorizedError(code, msg, url)
                    elif code == 404:
                        raise ICNotFoundError(code, msg, url)
                    elif code == 422:
                        raise ICValidationError(code, msg, url)
                    elif code == 429:
                        raise ICRateLimitExceededError(code, msg, url)
                    else:
                        raise ICError(code, msg, url)
                elif type(e) == ApiTimeout:
                    raise ICTimeoutError(e.message, e.request_id)
                elif type(e) == ApiFailedRequest:
                    raise ICFailedRequest(e.message, e.request_id)
                raise e
        return func

    @staticmethod
    def _underscore_to_camelcase(f):
        def underscore_to_camelcase(value):
            def camelcase():
                yield str.lower
                while True:
                    yield str.capitalize
            c = camelcase()
            return "".join(next(c)(x) if x else '_' for x in value.split("_"))
        def myprint(d):
            for k in list(d):
                v = d[k]
                del d[k]
                d[underscore_to_camelcase(k)] = v
                if isinstance(v, dict):
                    myprint(v)


        @functools.wraps(f)
        def func(*args, **kwargs):
            x = f(*args, **kwargs)
            myprint(x)
            return x
        return func

    @staticmethod
    def handle_response_operations(func, response):
        return_data = response[0]
        status_code = response[1]
        response_headers = response[2]

        if func.__name__ in IonosCoreProxy.custom_methods and IonosCoreProxy.custom_methods[func.__name__] in ['POST-ACTION-JSON', 'POST-ACTION']:
            if status_code == 202 and func.__name__ in IonosCoreProxy.custom_methods and IonosCoreProxy.custom_methods[func.__name__] == 'POST-ACTION':
                return True

        if 'location' in response_headers:
            if return_data == '':
                return_data = {}
            elif type(return_data) != dict:
                return_data = return_data.to_dict()
            return_data['requestId'] = IonosCoreProxy._request_id(response_headers)

        return return_data



    @staticmethod
    def cast_exception(e):
        if type(e).__name__ == ApiException.__name__:

            code = e.status
            msg = json.loads(e.body)
            url = e.url

            if 'messages' in msg:
                msg = msg['messages']

            if code == 401:
                raise ICNotAuthorizedError(code, msg, url)
            if code == 404:
                raise ICNotFoundError(code, msg, url)
            if code == 422:
                raise ICValidationError(code, msg, url)
            if code == 429:
                raise ICRateLimitExceededError(code, msg, url)
            else:
                raise ICError(code, msg, url)
        raise e