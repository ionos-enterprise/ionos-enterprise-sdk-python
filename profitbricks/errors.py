class PBError(Exception):
    """Base error for this module."""
    def __init__(self, resp, content, uri=None):
        self.resp = resp
        self.content = content
        self.uri = uri


class PBNotAuthorizedError(PBError):
    """HTTP data was invalid or unexpected."""


class PBNotFoundError(PBError):
    """HTTP data was invalid or unexpected."""


class PBValidationError(PBError):
    """HTTP data was invalid or unexpected."""
