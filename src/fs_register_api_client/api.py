from __future__ import annotations


__all__ = ['FSRegisterApiClient',
           'FSRegisterApiResponse',
           'FSRegisterApiSession',]


# -- IMPORTS --

# -- Standard libraries --
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from typing import Literal
from urllib.parse import urlencode

# -- 3rd party libraries --
import requests

from requests.models import Response

# -- Internal libraries --
from fs_register_api_client.constants import FS_REGISTER_API_CONSTANTS
from fs_register_api_client.exceptions import (
    FSRegisterApiRequestException,
    FSRegisterApiResponseException,
)


class FSRegisterApiSession(requests.Session):
    """A simple :py:class:`requests.Session`-based class for an FS Register API session.

    Examples
    --------
    >>> import os
    >>> session = FSRegisterApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
    >>> type(session)
    <class 'api.FSRegisterApiSession'>
    >>> assert session.api_username == os.environ['API_USERNAME']
    >>> assert session.api_key == os.environ['API_KEY']
    >>> assert session.headers == {'ACCEPT': 'application/json', 'X-AUTH-EMAIL': os.environ['API_USERNAME'], 'X-AUTH-KEY': os.environ['API_KEY']}
    """

    _api_username: str
    _api_key: str

    def __init__(self, api_username: str, api_key: str) -> None:
        """Initialiser requiring the API username and key.

        Parameters
        ----------
        api_username : str
            The API username which will be the email used to sign up on the
            FS Register developer portal:

            https://register.fca.org.uk/Developer/s/

        api_key : str
            The API key obtained from the registration profile on the FS
            Register API developer portal.

        Examples
        --------
        >>> import os
        >>> session = FSRegisterApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert session.api_username == os.environ['API_USERNAME']
        >>> assert session.api_key == os.environ['API_KEY']
        >>> assert session.headers == {'ACCEPT': 'application/json', 'X-AUTH-EMAIL': os.environ['API_USERNAME'], 'X-AUTH-KEY': os.environ['API_KEY']}
        """
        super().__init__()

        self._api_username = api_username
        self._api_key = api_key
        self.headers = {
            'ACCEPT': 'application/json',
            'X-AUTH-EMAIL': self._api_username,
            'X-AUTH-KEY': self._api_key
        }

    @property
    def api_username(self) -> str:
        """:py:class:`str`: The API username (FS Register signup email).

        Returns
        -------
        str
            The API username.

        Examples
        --------
        >>> import os
        >>> session = FSRegisterApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert session.api_username == os.environ['API_USERNAME']
        """
        return self._api_username

    @property
    def api_key(self) -> str:
        """:py:class:`str`: The API key (obtained from the registration profile).

        Returns
        -------
        str
            The API key.

        Examples
        --------
        >>> import os
        >>> session = FSRegisterApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert session.api_key == os.environ['API_KEY']
        """
        return self._api_key


class FSRegisterApiResponse(requests.models.Response):
    """A simple :py:class:`requests.Response`-based wrapper for FS Register API responses.

    Examples
    --------
    >>> import os
    >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
    >>> res = client.common_search('Hastings Direct', 'firm')
    >>> res
    <Response [200]>
    """

    __attrs__ = Response.__attrs__

    def __init__(self, response: requests.Response) -> None:
        """Initialiser requiring a :py:class:`requests.Response` object.

        Parameters
        ----------
        response : requests.Response
            The response from the original request.
        """    
        self.__dict__.update(**response.__dict__)

    @property
    def fs_register_status(self) -> str:
        """:py:class:`str`: The FS Register status code of the response.

        Returns
        -------
        str
            The FS Register status code from the original request.
        """
        return self.json().get('Status')

    @property
    def fs_register_resultinfo(self) -> dict:
        """:py:class:`dict`: The FS Register pagination information on the response from the original request.

        Returns
        -------
        dict
            The FS Register pagination information on the response from the original request.
        """
        return self.json().get('ResultInfo')

    @property
    def fs_register_message(self) -> str:
        """:py:class:`str`: The FS Register status message in the response.

        Returns
        -------
        str
            The FS Register status message from the original request.
        """
        return self.json().get('Message')

    @property
    def fs_register_data(self) -> dict | list[dict]:
        """:py:class:`dict` or :py:class:`list`: The FS Register data in the response.

        Returns
        -------
        str
            The FS Register data from the original request - will either be a
            :py:class:`dict` or a :py:class:`list` of dicts.
        """
        return self.json().get('Data')


class FSRegisterApiClient:
    """Client for the FS Register API (V0.1).

    Consult the API documentation for further details.

    https://register.fca.org.uk/Developer/s/

    Examples
    --------
    >>> import os; from urllib.parse import urlencode
    >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
    >>> res = client.common_search('Hastings Direct', 'firm')
    >>> res
    <Response [200]>
    >>> assert res.fs_register_data
    >>> assert res.fs_register_status
    >>> assert res.fs_register_message
    >>> assert res.fs_register_resultinfo
    >>> client.search_frn("Hastings Insurance Services Limited")
    '311492'
    >>> client.search_frn('direct line')
    Traceback (most recent call last):
    ...
    fs_register_api_client.exceptions.FSRegisterApiResponseException: Multiple firms returned. The firm name needs to be more precise. If you are unsure of the results please use the common search endpoint.
    >>> client.search_frn('direct line insurance plc')
    '202684'
    >>> assert client.get_firm('122702').fs_register_data
    >>> assert client.get_individual('MXC29012').fs_register_data
    >>> assert client.get_fund('635641').fs_register_data
    """

    #: All instances must have this private attribute to store API session state
    _api_session: FSRegisterApiSession

    def __init__(self, api_username: str, api_key: str) -> None:
        """Initialiser requiring the API username and key.

        Parameters
        ----------
        api_username : str
            The API username which will be the email used to sign up on the
            FS Register developer portal:

            https://register.fca.org.uk/Developer/s/

        api_key : str
            The API key obtained from the registration profile on the FS
            Register API developer portal.

        Examples
        --------
        >>> import os; from fs_register_api_client.constants import FS_REGISTER_API_CONSTANTS
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert client.api_session.api_username == os.environ['API_USERNAME']
        >>> assert client.api_session.api_key == os.environ['API_KEY']
        >>> assert client.api_session.headers == {'ACCEPT': 'application/json', 'X-AUTH-EMAIL': os.environ['API_USERNAME'], 'X-AUTH-KEY': os.environ['API_KEY']}
        >>> assert client.api_version == FS_REGISTER_API_CONSTANTS.API_VERSION.value
        """
        self._api_session = FSRegisterApiSession(api_username, api_key)

    @property
    def api_session(self) -> FSRegisterApiSession:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiSession`: The API session instance.

        Returns
        -------
        FSRegisterApiSession
            The current :py:class:`~fs_register_api_client.api.FSRegisterApiSession` object.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert isinstance(client.api_session, FSRegisterApiSession)
        """
        return self._api_session

    @property
    def api_version(self) -> str:
        """:py:class:`str`: The API version being used by the client.

        Returns
        -------
        str
            The API version being used by the client.

        Examples
        --------
        >>> import os; from fs_register_api_client.constants import FS_REGISTER_API_CONSTANTS
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert client.api_version == FS_REGISTER_API_CONSTANTS.API_VERSION.value
        """
        return FS_REGISTER_API_CONSTANTS.API_VERSION.value

    def common_search(self, resource_name: str, resource_type: Literal['firm', 'individual', 'fund']) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the results of a search using the FS Register API common search API endpoint.

        Directly calls the API common search endpoint:
        ::

            /V0.1/Search?q=resource_name>&type=resource_type

        to perform a case-insensitive search in the FS Register on the given
        resource name (or name substring) and resource type (``"firm"``,
        ``"individual"``, ``"fund"``).

        Returns an :py:class:`~fs_register_api_client.api.FSRegisterApiResponse` object if the
        API call completes without exceptions or errors.

        Parameters
        ----------
        resource_name : str
            The name (or name substring) of a resource to search for in the
            FS Register, e.g. ``"ABC Company"``, ``"John Smith"``,
            ``"International Super Fund"``.

        resource_type : str
            The resource type to search for - according to the API this must
            be one of the following strings: ``"firm"``, ``"individual"``, or
            ``"fund"``.

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Raises
        ------
        FSRegisterApiRequestException
            If there was a :py:class:`requests.RequestException` in making the original
            request.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.common_search('Hastings Direct', 'firm')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> assert res.fs_register_status
        >>> assert res.fs_register_message
        >>> assert res.fs_register_resultinfo
        """
        search_str = urlencode({'q': resource_name, 'type': resource_type})
        url = f'{FS_REGISTER_API_CONSTANTS.BASEURL.value}/Search?{search_str}'

        try:
            return FSRegisterApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise FSRegisterApiRequestException(e)

    def _search_ref_number(self, resource_name: str, resource_type: str) -> str:
        """:py:class:`str`: A private base handler for public methods for searching for unique firm, individual and product reference numbers.

        .. note::

           This is a private method and is **not** intended for direct use by
           end users.

        Uses the API common search endpoint:
        ::

            /V0.1/Search?q=resource_name&type=resource_type

        to perform a case-insensitive search for resources of type
        ``resource_type`` in the FS Register on the given resource name
        substring.

        Returns a non-null string of the resource ref. number if there is
        a unique associated resource.


        Parameters
        ----------
        resource_name : str
            The resource name substring - need not be in any particular case.
            The name needs to be precise enough to guarantee a unique return
            value, otherwise multiple records exist and an exception is raised.

        Raises
        ------
        ValueError
            If the resource type is not of ``'firm'``, ``'individual'``, or
            ``'fund'``. 
        FSRegisterApiRequestException
            If there was a request exception from calling the common search
            handler.
        FsrApiException
            If there was an error in the API response or in processing the response.

        Returns
        -------
        str
            The unique resource reference number, if found.
        """
        if resource_type not in FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value:
            raise ValueError(
                'Resource type must be one of the strings ``"firm"``, '
                '``"fund"``, or ``"individual"``'
            )

        try:
            res = self.common_search(resource_name, resource_type)
        except FSRegisterApiRequestException:
            raise

        if res.ok and res.fs_register_data:
            if len(res.fs_register_data) > 1:
                raise FSRegisterApiResponseException(
                    f'Multiple {resource_type}s returned. The {resource_type} '
                     'name needs to be more precise. If you are unsure of the '
                     'results please use the common search endpoint.'
                )

            try:
                return res.fs_register_data[0]['Reference Number']
            except (KeyError, IndexError):
                raise FSRegisterApiResponseException(
                    'Unexpected response data structure from the FS Register '
                    f'API for general {resource_type} search by name! Please '
                    'check the FS Register API developer documentation at '
                    'https://register.fca.org.uk/Developer/s/.'
                )
        elif not res.fs_register_data:
            raise FSRegisterApiResponseException(
                'No data found in FS Register API response. Please check the search '
                'parameters and try again.'
            )
        else:
            raise FSRegisterApiResponseException(
                f'FS Register API search request failed for some other reason: '
                f'{res.reason}.'
            )

    def search_frn(self, firm_name: str) -> str:
        """:py:class:`str`: Returns the unique firm reference number (FRN) of a given firm, if found.

        Calls the private method
        :py:meth:`~fs_register_api_client.FSRegisterApiClient._search_ref_number` to do the
        search.

        Returns a non-null string of the FRN if there is a unique associated
        firm.

        Parameters
        ----------
        firm_name : str
            The firm name - need not be in any particular case. The name
            needs to be precise enough to guarantee a unique return value,
            otherwise multiple records exist and an exception is raised.

        Returns
        -------
        str
            A string version of the firm reference number (FRN), if found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_frn("Hastings Insurance Services Limited")
        '311492'
        >>> client.search_frn('hiscox insurance company limited')
        '113849'
        >>> client.search_frn('direct line')
        Traceback (most recent call last):
        ...
        fs_register_api_client.exceptions.FSRegisterApiResponseException: Multiple firms returned. The firm name needs to be more precise. If you are unsure of the results please use the common search endpoint.
        >>> client.search_frn('direct line insurance')
        Traceback (most recent call last):
        ...
        fs_register_api_client.exceptions.FSRegisterApiResponseException: Multiple firms returned. The firm name needs to be more precise. If you are unsure of the results please use the common search endpoint.
        >>> client.search_frn('direct line insurance plc')
        '202684'
        >>> client.search_frn('Hiscxo Insurance Company')
        Traceback (most recent call last):
        ...
        fs_register_api_client.exceptions.FSRegisterApiResponseException: No data found in FS Register API response. Please check the search parameters and try again.
        >>> client.search_frn('hiscox insurance company')
        '113849'
        """
        return self._search_ref_number(
            firm_name,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name']
        )


    def _get_resource_info(self, resource_ref_number: str, resource_type: str, modifiers: tuple[str] = None) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: A private, base handler for resource information API handlers.

        Is the base handler for the following resource informational API endpoints (in alphabetical order):
        ::

            /V0.1/CIS/{PRN}
            /V0.1/CIS/{PRN}/Names
            /V0.1/CIS/{PRN}/Subfund
            /V0.1/Firm/{FRN}
            /V0.1/Firm/{FRN}/Address
            /V0.1/Firm/{FRN}/AR
            /V0.1/Firm/{FRN}/CF
            /V0.1/Firm/{FRN}/DisciplinaryHistory
            /V0.1/Firm/{FRN}/Exclusions
            /V0.1/Firm/{FRN}/Individuals
            /V0.1/Firm/{FRN}/Names
            /V0.1/Firm/{FRN}/Passports
            /V0.1/Firm/{FRN}/Passports/{Country}/Permission
            /V0.1/Firm/{FRN}/Permissions
            /V0.1/Firm/{FRN}/Regulators
            /V0.1/Firm/{FRN}/Requirements
            /V0.1/Firm/{FRN}/Requirements/{ReqRef}/InvestmentTypes
            /V0.1/Firm/{FRN}/Waiver
            /V0.1/Individuals/{IRN}
            /V0.1/Individuals/{IRN}/CF
            /V0.1/Individuals/{IRN}/DisciplinaryHistory

        where ``{FRN}``, ``{IRN}``, and ``{PRN}`` denote unique firm reference
        numbers (FRN), individual reference numbers (IRN), and product
        reference numbers (PRN).

        The ``resource_ref_number`` must be a valid unique resource identifier
        and ``resource_type`` should be a valid resource type, as given by one
        of the strings ``'firm'``, ``'individual'``, or ``'fund'``.
            
        .. note::

           This is a private method and is **not** intended for direct use by
           end users.

        Returns an :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`.

        The optional modifiers, given as a tuple of strings, should represent a
        valid ordered combination of actions and/or properties related to the
        given resource as identified by the resource ref. number.

        The modifier strings should **NOT** contain any leading or trailing
        forward slashes (``"/"``) as this can lead to badly formed URLs
        and to responses with no data - in any case, any leading or trailing
        forward slashes are stripped before the request.

        Parameters
        ----------
        resource_ref_number : str
            The resource reference number.

        resource_type : str
            The resource type - should be one of the strings ``'firm'``,
            ``'individual'``, or ``'fund'``.

        modifiers : tuple, default=None
            Optional tuple of strings indicating a valid ordered combination of
            resource and/or action modifiers for the resource in question.
            Should **NOT** have leading or trailing forward slashes (``"/"``).

        Raises
        ------
        FSRegisterApiRequestException
            If there was a request exception.

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the resource ref. number isn't found.
        """
        if resource_type not in FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value:
            raise ValueError(
                'Resource type must be one of the strings ``"firm"``, '
                '``"fund"``, or ``"individual"``'
            )

        resource_endpoint_base = (
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value[resource_type]['endpoint_base']
        )

        url = (
            f'{FS_REGISTER_API_CONSTANTS.BASEURL.value}'
            '/'
            f'{resource_endpoint_base}'
            '/'
            f'{resource_ref_number}'
        )

        if modifiers:
            url += f'/{"/".join(modifiers)}'

        try:
            return FSRegisterApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise FSRegisterApiRequestException(e)

    def get_firm(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing firm details, given its firm reference number (FRN)

        Handler for the top-level firm details API endpoint:
        ::

            /V0.1/Firm/{FRN}

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data[0]['Organisation Name'] == 'Barclays Bank Plc'
        >>> res = client.get_firm('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name']
        )

    def get_firm_names(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the alternative or secondary trading name details of a firm, given its firm reference number (FRN).

        Handler for the firm names API endpoint:
        ::

            /V0.1/Firm/{FRN}/Names

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_names('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data[0]['Current Names']
        >>> assert res.fs_register_data[1]['Previous Names']
        >>> res = client.get_firm_names('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Names',)
        )

    def get_firm_addresses(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the address details of a firm, given its firm reference number (FRN).

        Handler for the firm address details API endpoint:
        ::

            /V0.1/Firm/{FRN}/Address

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_addresses('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_addresses('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Address',))

    def get_firm_controlled_functions(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the controlled functions associated with a firm ,given its firm reference number (FRN).

        Handler for the firm controlled functions API endpoint:
        ::

            /V0.1/Firm/{FRN}/CF

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_controlled_functions('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_controlled_functions('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('CF',)
        )

    def get_firm_individuals(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the individuals associated with a firm, given its firm reference number (FRN).

        Handler for the firm individuals API endpoint:
        ::

            /V0.1/Firm/{FRN}/Individuals

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_individuals('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_individuals('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Individuals',)
        )

    def get_firm_permissions(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the permissions associated with a firm, given its firm reference number (FRN).

        Handler for the firm permissions API endpoint:
        ::

            /V0.1/Firm/{FRN}/Permissions

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_permissions('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_permissions('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Permissions',)
        )

    def get_firm_requirements(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the requirements associated with a firm, given its firm reference number (FRN).

        Handler for the firm requirements API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_requirements('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_requirements('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Requirements',)
        )

    def get_firm_requirement_investment_types(self, frn: str, req_ref: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing any investment types listed for a specific requirement associated with a firm, given its firm reference number (FRN).

        Handler for the firm requirement investment types API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements/<ReqRef>/InvestmentTypes

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        req_ref : str
            The requirement reference number as a string.

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_requirement_investment_types('122702', 'OR-0262545')
        >>> assert res.fs_register_data
        >>> res = client.get_firm_requirement_investment_types('1234567890', 'OR-0262545')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Requirements', req_ref, 'InvestmentTypes')
        )

    def get_firm_regulators(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the regulators associated with a firm, given its firm reference number (FRN).

        Handler for the firm regulators API endpoint:
        ::

            /V0.1/Firm/{FRN}/Regulators

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_regulators('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_regulators('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Regulators',)
        )

    def get_firm_passports(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the passports associated with a firm, given its firm reference number (FRN).

        Handler for the firm passports API endpoint:
        ::

            /V0.1/Firm/{FRN}/Passports

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_passports('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_passports('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Passports',)
        )

    def get_firm_passport_permissions(self, frn: str, country: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing country-specific passport permissions for a firm and a country, given its firm reference number (FRN) and country name.

        Handler for the firm passport permissions API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements/{Country}/Permission

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        country : str
            The country name.

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_passport_permissions('122702', 'Gibraltar')
        >>> assert res.fs_register_data
        >>> res = client.get_firm_passport_permissions('1234567890', 'Gibraltar')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Passports', country, 'Permission')
        )

    def get_firm_waivers(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing any waivers applying to a firm, given its firm reference number (FRN).

        Handler for the firm waivers API endpoint:
        ::

            /V0.1/Firm/{FRN}/Waivers

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_waivers('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_waivers('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Waivers',)
        )

    def get_firm_exclusions(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing any exclusions applying to a firm, given its firm reference number (FRN).

        Handler for the firm exclusions API endpoint:
        ::

            /V0.1/Firm/{FRN}/Exclusions

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_exclusions('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_exclusions('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Exclusions',)
        )

    def get_firm_disciplinary_history(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing the disciplinary history of a firm, given its firm reference number (FRN).

        Handler for the firm disciplinary history API endpoint:
        ::

            /V0.1/Firm/{FRN}/DisciplinaryHistory

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_disciplinary_history('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_firm_disciplinary_history('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('DisciplinaryHistory',)
        )

    def get_firm_appointed_representatives(self, frn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse`: Returns a response containing information on the appointed representatives of a firm, given its firm reference number (FRN).

        Handler for the firm appointed representatives API endpoint:
        ::

            /V0.1/Firm/{FRN}/AR

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_appointed_representatives('122702')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> assert any([res.fs_register_data['PreviousAppointedRepresentatives'], res.fs_register_data['CurrentAppointedRepresentatives']])
        >>> res = client.get_firm_appointed_representatives('1234567890')
        >>> assert not any([res.fs_register_data['PreviousAppointedRepresentatives'], res.fs_register_data['CurrentAppointedRepresentatives']])
        """
        return self._get_resource_info(
            frn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('AR',)
        )

    def search_irn(self, individual_name: str) -> str:
        """:py:class:`str`: Returns the unique individual reference number (IRN) of a given individual, if found.

        Uses the API common search endpoint:
        ::

            /V0.1/Search?q=<individual name>&type=individual

        to perform a case-insensitive individual-type search in the FS Register on the
        given name.

        Returns a non-null string of the IRN if there is a unique associated
        individual.

        Parameters
        ----------
        individual_name : str
            The individual name - need not be in any particular case. The name
            needs to be precise enough to guarantee a unique return value,
            otherwise multiple records exist and an exception is raised.

        Raises
        ------
        FSRegisterApiRequestException
            If there was a request exception from calling the common search
            handler.

        FsrApiException
            If there was an error in the API response or in processing the response.

        Returns
        -------
        str
            A string version of the individual reference number (IRN), if
            found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_irn('Mark Carney')
        'MXC29012'
        >>> client.search_irn('mark Carney')
        'MXC29012'
        >>> client.search_irn('Mark C')
        Traceback (most recent call last):
        ...
        fs_register_api_client.exceptions.FSRegisterApiResponseException: Multiple individuals returned. The individual name needs to be more precise. If you are unsure of the results please use the common search endpoint.
        >>> client.search_irn('A Nonexistent Person')
        Traceback (most recent call last):
        ...
        fs_register_api_client.exceptions.FSRegisterApiResponseException: No data found in FS Register API response. Please check the search parameters and try again.
        """
        return self._search_ref_number(
            individual_name,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['individual']['type_name']
        )

    def get_individual(self, irn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse` : Returns a response containing individual details, given their individual reference number (IRN)

        Handler for top-level individual details API endpoint:
        ::

            /V0.1/Individuals/{IRN}

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the IRN is found, otherwise with no data.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_individual('MXC29012')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data[0]['Details']['Full Name'] == 'Mark Carney'
        >>> res = client.get_individual('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            irn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['individual']['type_name']
        )

    def get_individual_controlled_functions(self, irn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse` : Returns a response containing the controlled functions associated with an individual, given their individual reference number (FRN).

        Handler for the individual controlled functions API endpoint:
        ::

            /V0.1/Firm/{IRN}/CF

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the IRN is found, otherwise with no data.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapepr of the API response object - there may be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_individual_controlled_functions('MXC29012')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_individual_controlled_functions('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            irn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['individual']['type_name'],
            modifiers=('CF',)
        )

    def get_individual_disciplinary_history(self, irn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse` : Returns a response containing the disciplinary history of an individual, given their individual reference number (FRN).

        Handler for the individual disciplinary history API endpoint:
        ::

            /V0.1/Firm/{IRN}/DisciplinaryHistory

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the IRN is found, otherwise with no data.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_irn('Leigh Mackey')
        'LXM01328'
        >>> res = client.get_individual_disciplinary_history('LXM01328')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_individual_disciplinary_history('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            irn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['individual']['type_name'],
            modifiers=('DisciplinaryHistory',)
        )

    def search_prn(self, fund_name: str) -> str:
        """:py:class:`str` : Returns the unique product reference number (PRN) of a given fund or collective investment scheme (CIS), including subfunds, if it exists.

        Uses the API common search endpoint:
        ::

            /V0.1/Search?q=<fund name>&type=fund

        to perform a case-insensitive fund-type search in the FS Register on
        the given name.

        Returns a non-null string of the PRN if there is a unique associated
        fund.

        Parameters
        ----------
        fund_name : str
            The fund name - need not be in any particular case. The name needs
            to be precise enough to guarantee a unique return value, otherwise
            multiple records exist and an exception is raised.

        Raises
        ------
        FSRegisterApiRequestException
            If there was a request exception from calling the common search
            handler.

        FSRegisterApiResponseException
            If there was an error in the API response or in processing the
            response.

        Returns
        -------
        str
            A string version of the product reference number (PRN), if found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_prn('Northern Trust')
        Traceback (most recent call last):
        ...
        fs_register_api_client.exceptions.FSRegisterApiResponseException: Multiple funds returned. The fund name needs to be more precise. If you are unsure of the results please use the common search endpoint.
        >>> client.search_prn('Northern Trust High Dividend ESG World Equity')
        Traceback (most recent call last):
        ...
        fs_register_api_client.exceptions.FSRegisterApiResponseException: Multiple funds returned. The fund name needs to be more precise. If you are unsure of the results please use the common search endpoint.
        >>> client.search_prn('Northern Trust High Dividend ESG World Equity Feeder Fund')
        '913937'
        >>> client.search_prn('A nonexistent fund')
        Traceback (most recent call last):
        ...
        fs_register_api_client.exceptions.FSRegisterApiResponseException: No data found in FS Register API response. Please check the search parameters and try again.
        """
        return self._search_ref_number(
            fund_name,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['fund']['type_name']
        )

    def get_fund(self, prn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse` : Returns a response containing fund (or collective investment scheme (CIS)) details, given its product reference number (PRN)

        Handler for top-level fund details API endpoint:
        ::

            /V0.1/CIS/{PRN}

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the PRN is found, otherwise with no data.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund('185045')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_fund('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            prn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['fund']['type_name']
        )

    def get_fund_names(self, prn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse` : Returns a response containing the alternative or secondary trading name details of a fund (or collective investment scheme (CIS)), given its product reference number (PRN).

        Handler for top-level fund names API endpoint:
        ::

            /V0.1/CIS/{PRN}/Names

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the PRN is found, otherwise with no data.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund_names('185045')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_fund_names('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            prn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['fund']['type_name'],
            modifiers=('Names',)
        )

    def get_fund_subfunds(self, prn: str) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse` : Returns a response containing the subfund details of a fund (or collective investment scheme (CIS)), given its product reference number (PRN).

        Handler for top-level subfund details API endpoint:
        ::

            /V0.1/CIS/{PRN}/Subfund

        Returns a :py:class:`~fs_register_api_client.api.FSRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund_subfunds('185045')
        >>> res
        <Response [200]>
        >>> assert res.fs_register_data
        >>> res = client.get_fund_subfunds('1234567890')
        >>> assert not res.fs_register_data
        """
        return self._get_resource_info(
            prn,
            FS_REGISTER_API_CONSTANTS.RESOURCE_TYPES.value['fund']['type_name'],
            modifiers=('Subfund',)
        )

    def get_regulated_markets(self) -> FSRegisterApiResponse:
        """:py:class:`~fs_register_api_client.api.FSRegisterApiResponse` : Returns a response containing details of all current regulated markets, as defined in UK and EU / EEA financial services legislation.

        For further information consult the API documentation:

        https://register.fca.org.uk/Developer/s/

        or the FCA glossary:

        https://www.handbook.fca.org.uk/handbook/glossary/G978.html?date=2007-01-20

        Returns
        -------
        FSRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the common search query produces no results.

        Examples
        --------
        >>> import json, os
        >>> client = FSRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_regulated_markets()
        >>> print(json.dumps(res.fs_register_data, indent=True))
        [
         {
          "Name": "The London Metal Exchange",
          "TradingName": "",
          "Type of business or Individual": "Exchange - RM",
          "Reference Number": "",
          "Status": "",
          "FirmURL": "https://register.fca.org.uk/services/V0.1/Firm/"
         },
         {
          "Name": "ICE Futures Europe",
          "TradingName": "",
          "Type of business or Individual": "Exchange - RM",
          "Reference Number": "",
          "Status": "",
          "FirmURL": "https://register.fca.org.uk/services/V0.1/Firm/"
         },
         {
          "Name": "London Stock Exchange",
          "TradingName": "",
          "Type of business or Individual": "Exchange - RM",
          "Reference Number": "",
          "Status": "",
          "FirmURL": "https://register.fca.org.uk/services/V0.1/Firm/"
         },
         {
          "Name": "Aquis Stock Exchange Limited",
          "TradingName": "ICAP Securities & Derivatives Exchange Limited",
          "Type of business or Individual": "Exchange - RM",
          "Reference Number": "",
          "Status": "",
          "FirmURL": "https://register.fca.org.uk/services/V0.1/Firm/"
         },
         {
          "Name": "Cboe Europe Equities Regulated Market",
          "TradingName": "",
          "Type of business or Individual": "Exchange - RM",
          "Reference Number": "",
          "Status": "",
          "FirmURL": "https://register.fca.org.uk/services/V0.1/Firm/"
         }
        ]
        """
        url = (
            f'{FS_REGISTER_API_CONSTANTS.BASEURL.value}'
            '/'
            'CommonSearch'
            '?'
            f'{urlencode({"q": "RM"})}'
        )

        return FSRegisterApiResponse(
            self.api_session.get(url)
        )

if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     export API_USERNAME=<API username> && export API_KEY=<API key> && python -m doctest -v src/fs_register_api_client/api.py && unset API_USERNAME && unset API_KEY
    #
    import doctest
    doctest.testmod()
