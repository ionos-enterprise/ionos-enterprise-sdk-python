class PBError(Exception):
    """Base error for this module."""
    def __init__(self, resp, content, uri=None):
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
