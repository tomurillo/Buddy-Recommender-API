class ResourceAlreadyExistsException(Exception):
    """
    This exception shall be raised when a resource which should not exist already exists
    """


class UserDoesNotExistException(Exception):
    """
    This exception shall be raised when data about a non-existing user is requested
    """


class ItemDoesNotExistException(Exception):
    """
    This exception shall be raised when data about a non-existing item is requested
    """