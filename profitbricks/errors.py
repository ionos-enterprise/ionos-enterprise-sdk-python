class PBError(Exception):
    """Base error for this module."""
    def __init__(self, resp, content, uri=None):
        self.resp = resp
        self.content = content
        self.uri = uri


class PBNotAuthorizedError(PBError):
    """The authorization infromation provided were not correct"""


class PBNotFoundError(PBError):
    """The ProfitBricks entity was not found"""


class PBValidationError(PBError):
    """HTTP data provided is not valid"""


class PBRateLimitExceededError(PBError):
    """The amount of requests sent have exceeded the API allowed limit"""
