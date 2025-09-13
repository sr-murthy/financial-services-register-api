from __future__ import annotations


__all__ = ['FinancialServicesRegisterApiClient',
           'FinancialServicesRegisterApiResponse',
           'FinancialServicesRegisterApiSession',]


# -- IMPORTS --

# -- Standard libraries --

from typing import Literal
from urllib.parse import urlencode

# -- 3rd party libraries --
import requests

from requests.models import Response

# -- Internal libraries --
from financial_services_register_api.constants import FINANCIAL_SERVICES_REGISTER_API_CONSTANTS as API_CONSTANTS
from financial_services_register_api.exceptions import (
    FinancialServicesRegisterApiRequestException,
    FinancialServicesRegisterApiResponseException,
)


class FinancialServicesRegisterApiSession(requests.Session):
    """A simple :py:class:`requests.Session`-based class for an API session.

    Examples
    --------
    >>> import os
    >>> session = FinancialServicesRegisterApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
    >>> type(session)
    <class 'api.FinancialServicesRegisterApiSession'>
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
            API developer portal:

            https://register.fca.org.uk/Developer/s/

        api_key : str
            The API key obtained from the registration profile on the API
            developer portal.

        Examples
        --------
        >>> import os
        >>> session = FinancialServicesRegisterApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
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
        """:py:class:`str`: The API username (signup email for the Financial Services Register).

        Returns
        -------
        str
            The API username.

        Examples
        --------
        >>> import os
        >>> session = FinancialServicesRegisterApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert session.api_username == os.environ['API_USERNAME']
        """
        return self._api_username

    @property
    def api_key(self) -> str:
        """:py:class:`str`: The API key (obtained from the API developer portal profile).

        Returns
        -------
        str
            The API key.

        Examples
        --------
        >>> import os
        >>> session = FinancialServicesRegisterApiSession(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert session.api_key == os.environ['API_KEY']
        """
        return self._api_key


class FinancialServicesRegisterApiResponse(requests.models.Response):
    """A simple :py:class:`requests.Response`-based wrapper for the API responses.

    Examples
    --------
    >>> import os
    >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
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
    def status(self) -> str:
        """:py:class:`str`: The status code of the API response.

        Returns
        -------
        str
            The status code of the API response.
        """
        return self.json().get('Status')

    @property
    def resultinfo(self) -> dict:
        """:py:class:`dict`: The pagination information in the API response.

        Returns
        -------
        dict
            The pagination information in the API response.
        """
        return self.json().get('ResultInfo')

    @property
    def message(self) -> str:
        """:py:class:`str`: The status message in the API response.

        Returns
        -------
        str
            The status message in the API response.
        """
        return self.json().get('Message')

    @property
    def data(self) -> dict | list[dict]:
        """:py:class:`dict` or :py:class:`list`: The data in the API response.

        Returns
        -------
        str
            The data in the API response - will usually be either a
            :py:class:`dict` or a :py:class:`list` of dicts.
        """
        return self.json().get('Data')


class FinancialServicesRegisterApiClient:
    """Client for the Financial Services Register API (V0.1).

    Consult the API documentation for further details.

    https://register.fca.org.uk/Developer/s/

    Examples
    --------
    >>> import os; from urllib.parse import urlencode
    >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
    >>> res = client.common_search('Hastings Direct', 'firm')
    >>> res
    <Response [200]>
    >>> assert res.data
    >>> assert res.status
    >>> assert res.message
    >>> assert res.resultinfo
    >>> client.search_frn("Hastings Insurance Services Limited")
    '311492'
    >>> res = client.search_frn('direct line')
    >>> assert isinstance(res, list)
    >>> assert (isinstance(rec, dict) for rec in res)
    >>> client.search_frn('direct line insurance plc')
    '202684'
    >>> assert client.get_firm('122702').data
    >>> assert client.get_individual('MXC29012').data
    >>> assert client.get_fund('635641').data
    """

    #: All instances must have this private attribute to store API session state
    _api_session: FinancialServicesRegisterApiSession

    def __init__(self, api_username: str, api_key: str) -> None:
        """Initialiser requiring the API username and key.

        Parameters
        ----------
        api_username : str
            The API username, which will be the email used to sign up on the
            developer portal:

            https://register.fca.org.uk/Developer/s/

        api_key : str
            The API key obtained from the registration profile on the developer
            portal.

        Examples
        --------
        >>> import os; from financial_services_register_api.constants import FINANCIAL_SERVICES_REGISTER_API_CONSTANTS as API_CONSTANTS
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert client.api_session.api_username == os.environ['API_USERNAME']
        >>> assert client.api_session.api_key == os.environ['API_KEY']
        >>> assert client.api_session.headers == {'ACCEPT': 'application/json', 'X-AUTH-EMAIL': os.environ['API_USERNAME'], 'X-AUTH-KEY': os.environ['API_KEY']}
        >>> assert client.api_version == API_CONSTANTS.API_VERSION.value
        """
        self._api_session = FinancialServicesRegisterApiSession(api_username, api_key)

    @property
    def api_session(self) -> FinancialServicesRegisterApiSession:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiSession`: The API session instance.

        Returns
        -------
        FinancialServicesRegisterApiSession
            The current :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiSession` object.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert isinstance(client.api_session, FinancialServicesRegisterApiSession)
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
        >>> import os; from financial_services_register_api.constants import FINANCIAL_SERVICES_REGISTER_API_CONSTANTS as API_CONSTANTS
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> assert client.api_version == API_CONSTANTS.API_VERSION.value
        """
        return API_CONSTANTS.API_VERSION.value

    def common_search(self, resource_name: str, resource_type: Literal['firm', 'individual', 'fund']) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the results of a search using the FS Register API common search API endpoint.

        Directly calls the API common search endpoint:
        ::

            /V0.1/Search?q=resource_name>&type=resource_type

        to perform a case-insensitive search in the FS Register on the given
        resource name (or name substring) and resource type (``"firm"``,
        ``"individual"``, ``"fund"``).

        Returns an :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse` object if the
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
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Raises
        ------
        FinancialServicesRegisterApiRequestException
            If there was a :py:class:`requests.RequestException` in making the original
            request.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.common_search('Hastings Direct', 'firm')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> assert res.status
        >>> assert res.message
        >>> assert res.resultinfo
        """
        search_str = urlencode({'q': resource_name, 'type': resource_type})
        url = f'{API_CONSTANTS.BASEURL.value}/Search?{search_str}'

        try:
            return FinancialServicesRegisterApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise FinancialServicesRegisterApiRequestException(e)

    def _search_ref_number(self, resource_name: str, resource_type: str, /) -> str | list[dict[str, str]]:
        """:py:class:`str` or :py:class:`list`: A private base handler for public search methods for unique firm, individual and product reference numbers.

        .. note::

           This is a private method and is **not** intended for direct use by
           end users.

        Uses the API common search endpoint:
        ::

            /V0.1/Search?q=resource_name&type=resource_type

        to perform a case-insensitive search for resources of type
        ``resource_type`` in the Financial Services Register on the given
        resource name substring.

        Returns a non-null string of the resource ref. number if there is
        a unique associated resource. Otherwise returns :py:class.

        If there are multiple resources matching the given resource name
        substring then a JSON array of the matching records is returned.


        Parameters
        ----------
        resource_name : str
            The resource name substring - need not be in any particular case.
            The name needs to be precise enough to guarantee a unique return
            value, otherwise multiple records exist and an exception is raised.

        resource_type : str
            The resource type, which should be one of ``'firm'``,
            ``'individual'``, or ``'fund'``.

        Returns
        -------
        str, list
            The unique resource reference number, if found. Otherwise
            a JSON array of matching records.

        Raises
        ------
        ValueError
            If the resource type is not of ``'firm'``, ``'individual'``, or
            ``'fund'``. 
        FinancialServicesRegisterApiRequestException
            If there was an API request exception.
        FinancialServicesRegisterApiResponseException
            If the API response does not conform to the expected structure, or
            no data was found for the given resource type and name.
        """
        if resource_type not in API_CONSTANTS.RESOURCE_TYPES.value:
            raise ValueError(
                'Resource type must be one of the strings ``"firm"``, '
                '``"fund"``, or ``"individual"``'
            )

        try:
            res = self.common_search(resource_name, resource_type)
        except FinancialServicesRegisterApiRequestException:
            raise

        if res.ok and res.data:
            if len(res.data) == 1:
                try:
                    return res.data[0]['Reference Number']
                except KeyError:
                    raise FinancialServicesRegisterApiResponseException(
                        'Unexpected response data structure from the API for '
                        f'{resource_type} search by name "{resource_name}"! '
                        'Please check the API developer documentation at '
                        f'{API_CONSTANTS.DEVELOPER_PORTAL.value}.'
                    )
            if len(res.data) > 1:
                return res.data
        elif not res.ok:
            raise FinancialServicesRegisterApiRequestException(
                f'API search request failed for an unknown reason: '
                f'{res.reason}. Please check the search parameters and try again.'
            )
        elif not res.data:
            raise FinancialServicesRegisterApiRequestException(
                'No data found in the API response. Please check the search '
                'parameters and try again.'
            )

    def search_frn(self, firm_name: str) -> str | list[dict[str, str]]:
        """:py:class:`str` or :py:class:`list`: Returns the unique firm reference number (FRN) of a given firm, if found, or else a JSON array of matching records.

        Calls the private method
        :py:meth:`~financial_services_register_api.FinancialServicesRegisterApiClient._search_ref_number` to do the
        search.

        Returns a non-null string of the FRN if there is a unique associated
        firm. Otherwise, a JSON array of all matching records is returned.

        Parameters
        ----------
        firm_name : str
            The firm name (case insensitive). The name needs to be precise
            enough to guarantee a unique return value, otherwise a JSON array
            of all matching records are returned.

        Returns
        -------
        str
            A string version of the firm reference number (FRN), if found, or
            a JSON array of all matching records.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_frn("Hastings Insurance Services Limited")
        '311492'
        >>> client.search_frn('hiscox insurance company limited')
        '113849'
        >>> res = client.search_frn('direct line')
        >>> assert isinstance(res, list)
        >>> assert all(isinstance(rec, dict) for rec in res)
        >>> client.search_frn('hiscox insurance company')
        '113849'
        >>> client.search_frn('nonexistent company')
        Traceback (most recent call last):
        ...
        financial_services_register_api.exceptions.FinancialServicesRegisterApiRequestException: No data found in the API response. Please check the search parameters and try again.
        """
        return self._search_ref_number(
            firm_name,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name']
        )


    def _get_resource_info(self, resource_ref_number: str, resource_type: str, modifiers: tuple[str] = None) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: A private, base handler for resource information API handlers.

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

        Returns an :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`.

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
        FinancialServicesRegisterApiRequestException
            If there was a request exception.

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the resource ref. number isn't found.
        """
        if resource_type not in API_CONSTANTS.RESOURCE_TYPES.value:
            raise ValueError(
                'Resource type must be one of the strings ``"firm"``, '
                '``"fund"``, or ``"individual"``'
            )

        resource_endpoint_base = (
            API_CONSTANTS.RESOURCE_TYPES.value[resource_type]['endpoint_base']
        )

        url = (
            f'{API_CONSTANTS.BASEURL.value}'
            '/'
            f'{resource_endpoint_base}'
            '/'
            f'{resource_ref_number}'
        )

        if modifiers:
            url += f'/{"/".join(modifiers)}'

        try:
            return FinancialServicesRegisterApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise FinancialServicesRegisterApiRequestException(e)

    def get_firm(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing firm details, given its firm reference number (FRN)

        Handler for the top-level firm details API endpoint:
        ::

            /V0.1/Firm/{FRN}

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm('122702')
        >>> res
        <Response [200]>
        >>> assert res.data[0]['Organisation Name'] == 'Barclays Bank Plc'
        >>> res = client.get_firm('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name']
        )

    def get_firm_names(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the alternative or secondary trading name details of a firm, given its firm reference number (FRN).

        Handler for the firm names API endpoint:
        ::

            /V0.1/Firm/{FRN}/Names

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_names('122702')
        >>> res
        <Response [200]>
        >>> assert res.data[0]['Current Names']
        >>> assert res.data[1]['Previous Names']
        >>> res = client.get_firm_names('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Names',)
        )

    def get_firm_addresses(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the address details of a firm, given its firm reference number (FRN).

        Handler for the firm address details API endpoint:
        ::

            /V0.1/Firm/{FRN}/Address

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_addresses('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_addresses('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Address',))

    def get_firm_controlled_functions(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the controlled functions associated with a firm ,given its firm reference number (FRN).

        Handler for the firm controlled functions API endpoint:
        ::

            /V0.1/Firm/{FRN}/CF

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_controlled_functions('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_controlled_functions('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('CF',)
        )

    def get_firm_individuals(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the individuals associated with a firm, given its firm reference number (FRN).

        Handler for the firm individuals API endpoint:
        ::

            /V0.1/Firm/{FRN}/Individuals

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_individuals('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_individuals('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Individuals',)
        )

    def get_firm_permissions(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the permissions associated with a firm, given its firm reference number (FRN).

        Handler for the firm permissions API endpoint:
        ::

            /V0.1/Firm/{FRN}/Permissions

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_permissions('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_permissions('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Permissions',)
        )

    def get_firm_requirements(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the requirements associated with a firm, given its firm reference number (FRN).

        Handler for the firm requirements API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_requirements('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_requirements('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Requirements',)
        )

    def get_firm_requirement_investment_types(self, frn: str, req_ref: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing any investment types listed for a specific requirement associated with a firm, given its firm reference number (FRN).

        Handler for the firm requirement investment types API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements/<ReqRef>/InvestmentTypes

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        req_ref : str
            The requirement reference number as a string.

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_requirement_investment_types('122702', 'OR-0262545')
        >>> assert res.data
        >>> res = client.get_firm_requirement_investment_types('1234567890', 'OR-0262545')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Requirements', req_ref, 'InvestmentTypes')
        )

    def get_firm_regulators(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the regulators associated with a firm, given its firm reference number (FRN).

        Handler for the firm regulators API endpoint:
        ::

            /V0.1/Firm/{FRN}/Regulators

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_regulators('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_regulators('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Regulators',)
        )

    def get_firm_passports(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the passports associated with a firm, given its firm reference number (FRN).

        Handler for the firm passports API endpoint:
        ::

            /V0.1/Firm/{FRN}/Passports

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_passports('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_passports('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Passports',)
        )

    def get_firm_passport_permissions(self, frn: str, country: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing country-specific passport permissions for a firm and a country, given its firm reference number (FRN) and country name.

        Handler for the firm passport permissions API endpoint:
        ::

            /V0.1/Firm/{FRN}/Requirements/{Country}/Permission

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        country : str
            The country name.

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_passport_permissions('122702', 'Gibraltar')
        >>> assert res.data
        >>> res = client.get_firm_passport_permissions('1234567890', 'Gibraltar')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Passports', country, 'Permission')
        )

    def get_firm_waivers(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing any waivers applying to a firm, given its firm reference number (FRN).

        Handler for the firm waivers API endpoint:
        ::

            /V0.1/Firm/{FRN}/Waivers

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_waivers('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_waivers('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Waivers',)
        )

    def get_firm_exclusions(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing any exclusions applying to a firm, given its firm reference number (FRN).

        Handler for the firm exclusions API endpoint:
        ::

            /V0.1/Firm/{FRN}/Exclusions

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_exclusions('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_exclusions('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('Exclusions',)
        )

    def get_firm_disciplinary_history(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing the disciplinary history of a firm, given its firm reference number (FRN).

        Handler for the firm disciplinary history API endpoint:
        ::

            /V0.1/Firm/{FRN}/DisciplinaryHistory

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_disciplinary_history('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_firm_disciplinary_history('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('DisciplinaryHistory',)
        )

    def get_firm_appointed_representatives(self, frn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`: Returns a response containing information on the appointed representatives of a firm, given its firm reference number (FRN).

        Handler for the firm appointed representatives API endpoint:
        ::

            /V0.1/Firm/{FRN}/AR

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        frn : str
            The firm reference number (FRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the FRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_firm_appointed_representatives('122702')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> assert any([res.data['PreviousAppointedRepresentatives'], res.data['CurrentAppointedRepresentatives']])
        >>> res = client.get_firm_appointed_representatives('1234567890')
        >>> assert not any([res.data['PreviousAppointedRepresentatives'], res.data['CurrentAppointedRepresentatives']])
        """
        return self._get_resource_info(
            frn,
            API_CONSTANTS.RESOURCE_TYPES.value['firm']['type_name'],
            modifiers=('AR',)
        )

    def search_irn(self, individual_name: str) -> str | list[dict[str, str]]:
        """:py:class:`str` or :py:class:`list`: Returns the unique individual reference number (IRN) of a given individual, if found, or else a JSON array of matching records.

        Calls the private method
        :py:meth:`~financial_services_register_api.FinancialServicesRegisterApiClient._search_ref_number`
        to do the search.

        Returns a non-null string of the IRN if there is a unique associated
        individual. Otherwise, a JSON array of all matching records is
        returned.

        Parameters
        ----------
        firm_name : str
            The individual name (case insensitive). The name needs to be precise
            enough to guarantee a unique return value, otherwise a JSON array
            of all matching records are returned.

        Returns
        -------
        str
            A string version of the individual reference number (IRN), if found, or
            a JSON array of all matching records.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_irn('Mark Carney')
        'MXC29012'
        >>> client.search_irn('mark Carney')
        'MXC29012'
        >>> res = client.search_irn('Mark C')
        >>> assert isinstance(res, list)
        >>> assert all(isinstance(rec, dict) for rec in res)
        >>> client.search_irn('nonexistent individual')
        Traceback (most recent call last):
        ...
        financial_services_register_api.exceptions.FinancialServicesRegisterApiRequestException: No data found in the API response. Please check the search parameters and try again.
        """
        return self._search_ref_number(
            individual_name,
            API_CONSTANTS.RESOURCE_TYPES.value['individual']['type_name']
        )

    def get_individual(self, irn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse` : Returns a response containing individual details, given their individual reference number (IRN)

        Handler for top-level individual details API endpoint:
        ::

            /V0.1/Individuals/{IRN}

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the IRN is found, otherwise with no data.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_individual('MXC29012')
        >>> res
        <Response [200]>
        >>> assert res.data[0]['Details']['Full Name'] == 'Mark Carney'
        >>> res = client.get_individual('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            irn,
            API_CONSTANTS.RESOURCE_TYPES.value['individual']['type_name']
        )

    def get_individual_controlled_functions(self, irn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse` : Returns a response containing the controlled functions associated with an individual, given their individual reference number (FRN).

        Handler for the individual controlled functions API endpoint:
        ::

            /V0.1/Firm/{IRN}/CF

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the IRN is found, otherwise with no data.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapepr of the API response object - there may be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_individual_controlled_functions('MXC29012')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_individual_controlled_functions('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            irn,
            API_CONSTANTS.RESOURCE_TYPES.value['individual']['type_name'],
            modifiers=('CF',)
        )

    def get_individual_disciplinary_history(self, irn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse` : Returns a response containing the disciplinary history of an individual, given their individual reference number (FRN).

        Handler for the individual disciplinary history API endpoint:
        ::

            /V0.1/Firm/{IRN}/DisciplinaryHistory

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the IRN is found, otherwise with no data.

        Parameters
        ----------
        irn : str
            The individual reference number (IRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the IRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_irn('Leigh Mackey')
        'LXM01328'
        >>> res = client.get_individual_disciplinary_history('LXM01328')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_individual_disciplinary_history('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            irn,
            API_CONSTANTS.RESOURCE_TYPES.value['individual']['type_name'],
            modifiers=('DisciplinaryHistory',)
        )

    def search_prn(self, fund_name: str) -> str | list[dict[str, str]]:
        """:py:class:`str` or :py:class:`list`: Returns the unique product reference number (PRN) of a given fund, if found, or else a JSON array of matching records.

        Calls the private method
        :py:meth:`~financial_services_register_api.FinancialServicesRegisterApiClient._search_ref_number`
        to do the search.

        Returns a non-null string of the PRN if there is a unique associated
        fund. Otherwise, a JSON array of all matching records is returned.

        Parameters
        ----------
        firm_name : str
            The fund name (case insensitive). The name needs to be precise
            enough to guarantee a unique return value, otherwise a JSON array
            of all matching records are returned.

        Returns
        -------
        str
            A string version of the product reference number (PRN), if found, or
            a JSON array of all matching records.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> client.search_prn('Northern Trust High Dividend ESG World Equity Feeder Fund')
        '913937'
        >>> res = client.search_prn('Northern Trust')
        >>> assert isinstance(res, list)
        >>> assert all(isinstance(rec, dict) for rec in res)
        >>> client.search_prn('nonexistent fund')
        Traceback (most recent call last):
        ...
        financial_services_register_api.exceptions.FinancialServicesRegisterApiRequestException: No data found in the API response. Please check the search parameters and try again.
        """
        return self._search_ref_number(
            fund_name,
            API_CONSTANTS.RESOURCE_TYPES.value['fund']['type_name']
        )

    def get_fund(self, prn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse` : Returns a response containing fund (or collective investment scheme (CIS)) details, given its product reference number (PRN)

        Handler for top-level fund details API endpoint:
        ::

            /V0.1/CIS/{PRN}

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the PRN is found, otherwise with no data.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund('185045')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_fund('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            prn,
            API_CONSTANTS.RESOURCE_TYPES.value['fund']['type_name']
        )

    def get_fund_names(self, prn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse` : Returns a response containing the alternative or secondary trading name details of a fund (or collective investment scheme (CIS)), given its product reference number (PRN).

        Handler for top-level fund names API endpoint:
        ::

            /V0.1/CIS/{PRN}/Names

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the PRN is found, otherwise with no data.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund_names('185045')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_fund_names('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            prn,
            API_CONSTANTS.RESOURCE_TYPES.value['fund']['type_name'],
            modifiers=('Names',)
        )

    def get_fund_subfunds(self, prn: str) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse` : Returns a response containing the subfund details of a fund (or collective investment scheme (CIS)), given its product reference number (PRN).

        Handler for top-level subfund details API endpoint:
        ::

            /V0.1/CIS/{PRN}/Subfund

        Returns a :py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse`, with data
        if the FRN is found, otherwise with no data.

        Parameters
        ----------
        prn : str
            The product reference number (PRN).

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the PRN isn't found.

        Examples
        --------
        >>> import os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_fund_subfunds('185045')
        >>> res
        <Response [200]>
        >>> assert res.data
        >>> res = client.get_fund_subfunds('1234567890')
        >>> assert not res.data
        """
        return self._get_resource_info(
            prn,
            API_CONSTANTS.RESOURCE_TYPES.value['fund']['type_name'],
            modifiers=('Subfund',)
        )

    def get_regulated_markets(self) -> FinancialServicesRegisterApiResponse:
        """:py:class:`~financial_services_register_api.api.FinancialServicesRegisterApiResponse` : Returns a response containing details of all current regulated markets, as defined in UK and EU / EEA financial services legislation.

        For further information consult the API documentation:

        https://register.fca.org.uk/Developer/s/

        or the FCA glossary:

        https://www.handbook.fca.org.uk/handbook/glossary/G978.html?date=2007-01-20

        Returns
        -------
        FinancialServicesRegisterApiResponse
            Wrapper of the API response object - there may be no data in
            the response if the common search query produces no results.

        Examples
        --------
        >>> import json, os
        >>> client = FinancialServicesRegisterApiClient(os.environ['API_USERNAME'], os.environ['API_KEY'])
        >>> res = client.get_regulated_markets()
        >>> print(json.dumps(res.data, indent=True))
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
            f'{API_CONSTANTS.BASEURL.value}'
            '/'
            'CommonSearch'
            '?'
            f'{urlencode({"q": "RM"})}'
        )

        return FinancialServicesRegisterApiResponse(
            self.api_session.get(url)
        )

if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     export API_USERNAME=<API username> && export API_KEY=<API key> && PYTHONPATH=src python -m doctest -v src/financial_services_register_api/api.py && unset API_USERNAME && unset API_KEY
    #
    import doctest
    doctest.testmod()
