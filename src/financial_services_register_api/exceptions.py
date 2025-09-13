__all__ = [
    'FinancialServicesRegisterApiClientException',
    'FinancialServicesRegisterApiException',
    'FinancialServicesRegisterApiRequestException',
    'FinancialServicesRegisterApiResponseException',
]


# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --

# -- Internal libraries --


class FinancialServicesRegisterApiException(Exception):
    """Base class for all API exceptions.
    """


class FinancialServicesRegisterApiRequestException(FinancialServicesRegisterApiException):
    """Base class all API request exceptions.
    """


class FinancialServicesRegisterApiResponseException(FinancialServicesRegisterApiException):
    """Base class all API response exceptions.
    """


class FinancialServicesRegisterApiClientException(FinancialServicesRegisterApiException):
    """Base class for an API client exceptions.
    """
