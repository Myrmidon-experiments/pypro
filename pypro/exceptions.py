
class PathNotExists(Exception):
    """Raised when a inexistent path is given."""


class HandlerNotImplement(Exception):
    """Raised when a handler does not implement the appropiate method."""


class SchemeConfigWrong(Exception):
    """Raised when any config on the scheme file is bad defined."""
