__all__ = ['FSRegisterApiException',
           'FSRegisterApiRequestException',
           'FSRegisterApiResponseException',]


# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --

# -- Internal libraries --


class FSRegisterApiException(Exception):
    """
    Base class all FS Register API exceptions.
    """
    ...


class FSRegisterApiRequestException(FSRegisterApiException):
    """
    Base class all FS Register API request exceptions.
    """
    ...


class FSRegisterApiResponseException(FSRegisterApiException):
    """
    Base class all FS Register API response exceptions.
    """
    ...
