
class PathNotExists(Exception):
    """Raised when a inexistent path is given."""


class HandlerNotImplement(Exception):
    """Raised when a handler does not implement the appropiate method."""


class WrongProjectStructure(Exception):
    """Raised when the structure of the project is bad defined."""
