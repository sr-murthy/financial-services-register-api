__all__ = ['FINANCIAL_SERVICES_REGISTER_API_CONSTANTS',]


# -- IMPORTS --

# -- Standard libraries --
from enum import Enum

# -- 3rd party libraries --

# -- Internal libraries --


class FINANCIAL_SERVICES_REGISTER_API_CONSTANTS(Enum):
    """An enum to store FS Register API-level constants.

    Examples
    --------
    >>> FINANCIAL_SERVICES_REGISTER_API_CONSTANTS.API_VERSION.value
    'V0.1'
    >>> FINANCIAL_SERVICES_REGISTER_API_CONSTANTS.BASEURL.value
    'https://register.fca.org.uk/services/V0.1'
    >>> FINANCIAL_SERVICES_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value
    {'firm': {'type_name': 'firm', 'endpoint_base': 'Firm'}, 'fund': {'type_name': 'fund', 'endpoint_base': 'CIS'}, 'individual': {'type_name': 'individual', 'endpoint_base': 'Individuals'}}
    """

    API_VERSION = 'V0.1'
    BASEURL = f'https://register.fca.org.uk/services/{API_VERSION}'
    DEVELOPER_PORTAL = 'https://register.fca.org.uk/Developer/s/'
    RESOURCE_TYPES = {
        'firm': {'type_name': 'firm', 'endpoint_base': 'Firm'},
        'fund': {'type_name': 'fund', 'endpoint_base': 'CIS'},
        'individual': {'type_name': 'individual', 'endpoint_base': 'Individuals'}
    }
