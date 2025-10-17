# -- IMPORTS --

# -- Standard libraries --
import os
import unittest.mock as mock

from urllib.parse import urlencode

# -- 3rd party libraries --
import pytest
import requests

# -- Internal libraries --
import financial_services_register_api.api

from financial_services_register_api.api import FinancialServicesRegisterApiSession, FinancialServicesRegisterApiClient
from financial_services_register_api.constants import FINANCIAL_SERVICES_REGISTER_API_CONSTANTS as API_CONSTANTS
from financial_services_register_api.exceptions import FinancialServicesRegisterApiRequestException, FinancialServicesRegisterApiResponseException


class _TestFinancialServicesRegisterApi:

    _api_username = os.environ['API_USERNAME']
    _api_key = os.environ['API_KEY']


class TestFinancialServicesRegisterApiSession(_TestFinancialServicesRegisterApi):

    def test_fs_register_api_session(self):
        test_session = FinancialServicesRegisterApiSession(self._api_username, self._api_key)

        assert test_session.api_username == self._api_username
        assert test_session.api_key == self._api_key
        assert test_session.headers == {
            'ACCEPT': 'application/json',
            'X-AUTH-EMAIL': self._api_username,
            'X-AUTH-KEY': self._api_key
        }


class TestFinancialServicesRegisterApiClient(_TestFinancialServicesRegisterApi):

    def test_financial_services_register_api_client____init__(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        assert test_client.api_session.api_username == self._api_username
        assert test_client.api_session.api_key == self._api_key
        assert test_client.api_session.headers == {
            'ACCEPT': 'application/json',
            'X-AUTH-EMAIL': self._api_username,
            'X-AUTH-KEY': self._api_key
        }
        assert test_client.api_version == API_CONSTANTS.API_VERSION.value

    def test_financial_services_register_api_client__common_search__api_request_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with mock.patch('financial_services_register_api.api.FinancialServicesRegisterApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FinancialServicesRegisterApiRequestException):
                test_client.common_search('exceptional resource', 'firm')

    def test_financial_services_register_api_client__common_search__no_api_request_exception(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        recv_response = test_client.common_search('hastings direct', 'firm')
        assert recv_response.ok
        assert recv_response.data
        assert len(recv_response.data)
        assert recv_response.status == 'FSR-API-04-01-00'
        assert recv_response.message == 'Ok. Search successful'
        assert recv_response.resultinfo

        recv_response = test_client.common_search('non existent firm', 'firm')
        assert recv_response.ok
        assert not recv_response.data
        assert recv_response.status == 'FSR-API-04-01-11'
        assert recv_response.message == 'No search result found'
        assert not recv_response.resultinfo

        recv_response = test_client.common_search('mark carney', 'individual')
        assert recv_response.ok
        assert recv_response.data
        assert len(recv_response.data)
        assert recv_response.status == 'FSR-API-04-01-00'
        assert recv_response.message == 'Ok. Search successful'
        assert recv_response.resultinfo

        recv_response = test_client.common_search('non existent individual', 'individual')
        assert recv_response.ok
        assert not recv_response.data
        assert recv_response.status == 'FSR-API-04-01-11'
        assert recv_response.message == 'No search result found'
        assert not recv_response.resultinfo

        recv_response = test_client.common_search('jupiter asia pacific income', 'fund')
        assert recv_response.ok
        assert recv_response.data
        assert len(recv_response.data)
        assert recv_response.status == 'FSR-API-04-01-00'
        assert recv_response.message == 'Ok. Search successful'
        assert recv_response.resultinfo

        recv_response = test_client.common_search('non existent fund', 'fund')
        assert recv_response.ok
        assert not recv_response.data
        assert recv_response.status == 'FSR-API-04-01-11'
        assert recv_response.message == 'No search result found'
        assert not recv_response.resultinfo

    def test_financial_services_register_api_client___search_ref_number__resource_type_incorrect__value_error_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with pytest.raises(ValueError):
            test_client._search_ref_number('resource_name', 'incorrect_resource_type')

    def test_financial_services_register_api_client___search_ref_number__exceptional_request__api_request_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with mock.patch('financial_services_register_api.api.FinancialServicesRegisterApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FinancialServicesRegisterApiRequestException):
                test_client._search_ref_number('exceptional search', 'firm')
                test_client._search_ref_number('exceptional search', 'individual')
                test_client._search_ref_number('exceptional search', 'fund')

    def test_financial_services_register_api_client___search_ref_number__response_not_ok__api_request_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with mock.patch('financial_services_register_api.api.FinancialServicesRegisterApiClient.common_search', return_value=mock.MagicMock(ok=False)):
            with pytest.raises(FinancialServicesRegisterApiRequestException):
                test_client._search_ref_number('exceptional search', 'firm')
                test_client._search_ref_number('exceptional search', 'individual')
                test_client._search_ref_number('exceptional search', 'fund')

    def test_financial_services_register_api_client___search_ref_number__no_fs_register_data_in_response__api_request_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with mock.patch('financial_services_register_api.api.FinancialServicesRegisterApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value=dict())
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FinancialServicesRegisterApiRequestException):
                test_client._search_ref_number('bad search', 'firm')
                test_client._search_ref_number('bad search', 'individual')
                test_client._search_ref_number('bad search', 'fund')

    def test_financial_services_register_api_client___search_ref_number__fs_register_data_with_key_error__api_request_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with mock.patch('financial_services_register_api.api.FinancialServicesRegisterApiSession.get') as mock_api_session_get:
            mock_response = mock.create_autospec(requests.Response)
            mock_response.json = mock.MagicMock(name='json', return_value={'Data': [{'not a Reference Number': None}]})
            mock_api_session_get.return_value = mock_response

            with pytest.raises(FinancialServicesRegisterApiResponseException):
                test_client._search_ref_number('bad response', 'firm')
                test_client._search_ref_number('bad response', 'individual')
                test_client._search_ref_number('bad response', 'fund')

    def test_financial_services_register_api_client___search_ref_number__incorrectly_specified_resource__no_fs_register_data__api_response_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a failed FRN search for an incorrectly specified firm
        with pytest.raises(FinancialServicesRegisterApiRequestException):
            test_client._search_ref_number('nonexistent123 insurance company', 'firm')

        # Covers the case of a failed IRN search for an incorrectly specified individual
        with pytest.raises(FinancialServicesRegisterApiRequestException):
            test_client._search_ref_number('a nonexistent individual', 'individual')

        # Covers the case of a failed PRN search for an incorrectly specified firm
        with pytest.raises(FinancialServicesRegisterApiRequestException):
            test_client._search_ref_number('a nonexistent fund', 'fund')

    def test_financial_services_register_api_client___search_ref_number__inadequately_specified_resource__nonunique_fs_register_data__api_response_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of an FRN search based on an inadequately specified firm
        # that produces multiple results
        recv_recs = test_client._search_ref_number('direct line', 'firm')
        assert isinstance(recv_recs, list)
        assert all(isinstance(rec, dict) for rec in recv_recs)

        # Covers the case of an IRN search based on an inadequately specified individual
        # that produces multiple results
        recv_recs = test_client._search_ref_number('john smith', 'individual')
        assert isinstance(recv_recs, list)
        assert all(isinstance(rec, dict) for rec in recv_recs)

        # Covers the case of an PRN search based on an inadequately specified firm
        # that produces multiple results
        recv_recs = test_client._search_ref_number('jupiter', 'fund')
        assert isinstance(recv_recs, list)
        assert all(isinstance(rec, dict) for rec in recv_recs)

    def test_financial_services_register_api_client___search_ref_number__correctly_and_adequately_specced_resource__unique_fs_register_data__response_returned_ok(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a successful FRN search for an existing firm
        recv_frn = test_client._search_ref_number('hiscox insurance company', 'firm')
        assert isinstance(recv_frn, str)
        assert recv_frn

        # Covers the case of a successful IRN search for an existing individual
        recv_irn = test_client._search_ref_number('mark carney', 'individual')
        assert isinstance(recv_irn, str)
        assert recv_irn

        # Covers the case of a successful PRN search for an existing fund
        recv_prn = test_client._search_ref_number('jupiter asia pacific income', 'fund')
        assert isinstance(recv_prn, str)
        assert recv_prn

    def test_financial_services_register_api_client___search_frn__correctly_and_adequately_specced_firm__unique_fs_register_data__response_returned_ok(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a successful FRN search for existing, unique firms
        recv_frn = test_client.search_frn('hiscox insurance company')
        assert isinstance(recv_frn, str)
        assert recv_frn

        recv_frn = test_client.search_frn('hastings insurance services limited')
        assert isinstance(recv_frn, str)
        assert recv_frn

        recv_frn = test_client.search_frn('citibank europe luxembourg')
        assert isinstance(recv_frn, str)
        assert recv_frn

    def test_financial_services_register_api_client___search_frn__inadequately_specced_firm__json_array_of_matching_records__response_returned_ok(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a successful FRN search for existing, unique firms
        recv_recs = test_client._search_ref_number('hsbc', 'firm')
        assert isinstance(recv_recs, list)
        assert all(isinstance(rec, dict) for rec in recv_recs)

        recv_recs = test_client._search_ref_number('northern', 'firm')
        assert isinstance(recv_recs, list)
        assert all(isinstance(rec, dict) for rec in recv_recs)

    def test_financial_services_register_api_client___get_resource_info__invalid_resource_type__no_modifiers__value_error_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with pytest.raises(ValueError):
            test_client._get_resource_info('test_ref_number', 'invalid resource type')

    def test_financial_services_register_api_client___get_resource_info__invalid_resource_type__modifiers__value_error_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with pytest.raises(ValueError):
            test_client._get_resource_info('test_ref_number', 'invalid resource type', modifiers=('test_modifier1', 'test_modifier2',))

    def test_financial_services_register_api_client___get_resource_info__no_modifiers__request_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with mock.patch('financial_services_register_api.api.FinancialServicesRegisterApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FinancialServicesRegisterApiRequestException):
                test_client._get_resource_info('test_frn', 'firm')
                test_client._get_resource_info('test_prn', 'fund')
                test_client._get_resource_info('test_irn', 'individual')

    def test_financial_services_register_api_client___get_resource_info__modifiers__request_exception_raised(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        with mock.patch('financial_services_register_api.api.FinancialServicesRegisterApiSession.get') as mock_api_session_get:
            mock_api_session_get.side_effect = requests.RequestException('test RequestException')

            with pytest.raises(FinancialServicesRegisterApiRequestException):
                test_client._get_resource_info('test_frn', 'firm', modifiers=('test_modifier1', 'test_modifier2',))
                test_client._get_resource_info('test_prn', 'fund', modifiers=('test_modifier1', 'test_modifier2',))
                test_client._get_resource_info('test_irn', 'individual', modifiers=('test_modifier1', 'test_modifier2',))

    def test_financial_services_register_api_client___get_resource_info__firm(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited with the FRN 113849
        recv_response = test_client._get_resource_info('113849', 'firm')
        assert recv_response.ok
        assert recv_response.data
        assert recv_response.data[0]['Organisation Name'] == 'Hiscox Insurance Company Limited'

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client._get_resource_info('1234567890', 'firm')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the secondary or
        # alternative business or trading names used by Hiscox Insurance
        # Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Names',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the secondary or alternative business
        # or trading names of a non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Names',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the listed business
        # address of Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Address',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the listed business address of a non-
        # existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Address',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the controlled functions
        # (CF) of Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('CF',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the controlled functions (CF) of a
        # non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('CF',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the individuals
        # associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Individuals',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the individuals associated with a
        # existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Individuals',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the activities and
        # permissions associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Permissions',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the activities and permissions
        # associated with a non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Permissions',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the requirements
        # associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Requirements',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the requirements associated with a
        # non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Requirements',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the investment types
        # associated with a specific requirement associated with Hiscox Insurance
        # Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Requirements', 'OR-0131728', 'InvestmentTypes',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the regulators
        # listed for Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Regulators',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the regulators listed for a
        # non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Regulators',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the passports
        # associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Passports',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the passports associated with a
        # non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Passports',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the passports
        # for a specific country, Gibraltar, associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Passports', 'Gibraltar', 'Permission',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the passports for a specific country
        # associated with a non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Passports', 'Gibraltar', 'Permission',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for any waivers
        # associated with Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('Waivers',))
        try:
            assert recv_response.ok
            assert recv_response.data
        except AssertionError:
            ...

        # Covers the case of a request for any waivers associated with a
        # non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Waivers',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for any exclusions
        # applying to Barclays Bank plc (FRN 122702)
        recv_response = test_client._get_resource_info('122702', 'firm', modifiers=('Exclusions',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for any exclusions applying to a
        # non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('Exclusions',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the disciplinary history
        # of Barclays Bank plc (FRN 122702)
        recv_response = test_client._get_resource_info('122702', 'firm', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the disciplinary history of a
        # non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the appointed representatives of
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client._get_resource_info('113849', 'firm', modifiers=('AR',))
        assert recv_response.ok
        assert (
            recv_response.data['PreviousAppointedRepresentatives'] or 
            recv_response.data['CurrentAppointedRepresentatives']
        )

        # Covers the case of a request for the appointed representatives
        # of a non-existent firm
        recv_response = test_client._get_resource_info('1234567890', 'firm', modifiers=('AR',))
        assert recv_response.ok
        assert not recv_response.data['PreviousAppointedRepresentatives']
        assert not recv_response.data['CurrentAppointedRepresentatives']

    def test_financial_services_register_api_client___get_resource_info__fund(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing fund which is
        # 'Jupiter Asia Pacific Income Fund (IRL)' with the PRN 1006826
        recv_response = test_client._get_resource_info('1006826', 'fund')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent fund given by
        # a non-existent PRN 1234567890
        recv_response = test_client._get_resource_info('1234567890', 'fund')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the subfund details of an
        # existing fund with PRN 185045
        recv_response = test_client._get_resource_info('185045', 'fund', modifiers=('Subfund',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the non-existent subfund details of an
        # existing fund with PRN 1006826
        recv_response = test_client._get_resource_info('1006826', 'fund', modifiers=('Subfund',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the non-existent subfund details
        # of a non-existent fund
        recv_response = test_client._get_resource_info('1234567890', 'fund', modifiers=('Subfund',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the alternative or secondary trading
        # names of an existing fund with PRN 185045
        recv_response = test_client._get_resource_info('185045', 'fund', modifiers=('Names',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the non-existent alternative or
        # secondary trading names of an existing fund with PRN 1006826
        recv_response = test_client._get_resource_info('1006826', 'fund', modifiers=('Names',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the non-existent alternative or
        # secondary trading names of a non-existing fund with a non-existent
        # PRN 1234567890
        recv_response = test_client._get_resource_info('1234567890', 'fund', modifiers=('Names',))
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client___get_resource_info__individual(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing individual
        # 'Mark Carney'(IRN 'MXC29012')
        recv_response = test_client._get_resource_info('MXC29012', 'individual')
        assert recv_response.ok
        assert recv_response.data
        assert recv_response.data[0]['Details']['Full Name'] == 'Mark Carney'

        # Covers the case of a request for an non-existent individual
        recv_response = test_client._get_resource_info('1234567890', 'individual')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the controlled functions
        # associated with an existing individual, 'Mark Carney'
        recv_response = test_client._get_resource_info('MXC29012', 'individual', modifiers=('CF',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the controlled functions associated
        # with a non-existent individual
        recv_response = test_client._get_resource_info('1234567890', 'individual', modifiers=('CF',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the disciplinary history
        # of an individual, 'Leigh Mackey' (IRN 'LXM01328')
        recv_response = test_client._get_resource_info('LXM01328', 'individual', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of an unrequest for the disciplinary history
        # of an individual, 'Mark Carney' (IRN 'MXC29012')
        recv_response = test_client._get_resource_info('MXC29012', 'individual', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the disciplinary history of a non-
        # existent individual
        recv_response = test_client._get_resource_info('1234567890', 'individual', modifiers=('DisciplinaryHistory',))
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the firm details of
        # an existing firm, Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm('113849')
        assert recv_response.ok
        assert recv_response.data
        assert recv_response.data[0]['Organisation Name'] == 'Hiscox Insurance Company Limited'

        # Covers the case of a request for the firm details of
        # an existing firm, Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_names(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_names('113849')
        assert recv_response.ok
        assert recv_response.data
        assert recv_response.data[0]['Current Names'][0]['Name'] == 'Hiscox'
        assert recv_response.data[1]['Previous Names']

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_names('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_addresses(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_addresses('113849')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_addresses('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_controlled_functions(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_controlled_functions('113849')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_controlled_functions('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_individuals(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_individuals('113849')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_individuals('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_permissions(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_permissions('113849')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_permissions('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_requirements(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_requirements('113849')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_requirements('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_requirement_investment_types(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Barclays Bank Plc (FRN 122702)
        recv_response = test_client.get_firm_requirement_investment_types('122702', 'OR-0262545')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of an unrequest for an existing firm which is
        # Barclays Bank Plc (FRN 122702)
        recv_response = test_client.get_firm_requirement_investment_types('122702', 'OR-1234567890')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_requirement_investment_types('1234567890', 'OR-0262545')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_regulators(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_regulators('113849')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_regulators('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_passports(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_passports('113849')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_passports('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_passport_permissions(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_passport_permissions('113849', 'Gibraltar')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a unrequest for an existing firm which is
        # Hiscox Insurance Comnpany Limited (FRN 113849)
        recv_response = test_client.get_firm_passport_permissions('113849', 'Germany')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_passport_permissions('1234567890', 'Gibraltar')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_waivers(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_waivers('113849')
        try:
            assert recv_response.ok
            assert recv_response.data
        except AssertionError:
            ...

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_waivers('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_exclusions(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Barclays Bank Plc (FRN 122702)
        recv_response = test_client.get_firm_exclusions('122702')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of an unrequest for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_exclusions('113849')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_exclusions('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_disciplinary_history(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Barclays Bank Plc (FRN 122702)
        recv_response = test_client.get_firm_disciplinary_history('122702')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of an unrequest for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_disciplinary_history('113849')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_disciplinary_history('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_firm_appointed_representatives(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing firm which is
        # Hiscox Insurance Company Limited (FRN 113849)
        recv_response = test_client.get_firm_appointed_representatives('113849')
        assert recv_response.ok
        assert recv_response.data
        assert any([
            recv_response.data['PreviousAppointedRepresentatives'],
            recv_response.data['CurrentAppointedRepresentatives']
        ])

        # Covers the case of a request for an non-existent firm given by
        # a non-existent FRN 1234567890
        recv_response = test_client.get_firm_appointed_representatives('1234567890')
        assert recv_response.ok
        assert not any([
            recv_response.data['PreviousAppointedRepresentatives'],
            recv_response.data['CurrentAppointedRepresentatives']
        ])

    def test_financial_services_register_api_client___search_irn__correctly_and_adequately_specced_individual__unique_fs_register_data__response_returned_ok(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a successful IRN search for existing, unique individuals
        recv_irn = test_client.search_irn('mark carney')
        assert isinstance(recv_irn, str)
        assert recv_irn

        recv_irn = test_client.search_irn('lynne elizabeth atkinson')
        assert isinstance(recv_irn, str)
        assert recv_irn

        recv_irn = test_client.search_irn('margaretha jensen')
        assert isinstance(recv_irn, str)
        assert recv_irn

    def test_financial_services_register_api_client___search_irn__inadequately_specced_individual__json_array_of_matching_records__response_returned_ok(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a successful IRN search for existing, unique individuals
        recv_recs = test_client.search_irn('john smith')
        assert isinstance(recv_recs, list)
        assert (isinstance(rec, dict) for rec in recv_recs)

    def test_financial_services_register_api_client__get_individual(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the details of an
        # existing individual, 'Mark Carney' (IRN 'MXC29012')
        recv_response = test_client.get_individual('MXC29012')
        assert recv_response.ok
        assert recv_response.data
        assert recv_response.data[0]['Details']['Full Name'] == 'Mark Carney'

        # Covers the case of a request for the details of a non-existent individual
        recv_response = test_client.get_individual('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_individual_controlled_functions(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing individual -
        # 'Mark Carney' (IRN 'MXC29012')
        recv_response = test_client.get_individual_controlled_functions('MXC29012')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent individual given by
        # a non-existent IRN '1234567890'
        recv_response = test_client.get_individual_controlled_functions('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_individual_disciplinary_history(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for an existing individual with -
        # disciplinary history, 'Leigh Mackey' (IRN 'LXM01328')
        recv_response = test_client.get_individual_disciplinary_history('LXM01328')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for an non-existent individual given by
        # a non-existent IRN '1234567890'
        recv_response = test_client.get_individual_disciplinary_history('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client___search_prn__correctly_and_adequately_specced_fund__unique_fs_register_data__response_returned_ok(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a successful PRN search for existing, unique funds
        recv_prn = test_client.search_prn('jupiter asia pacific income')
        assert isinstance(recv_prn, str)
        assert recv_prn

        recv_prn = test_client.search_prn('abrdn sterling short term government bond')
        assert isinstance(recv_prn, str)
        assert recv_prn

        recv_prn = test_client.search_prn('northern trust high dividend esg world equity feeder')
        assert isinstance(recv_prn, str)
        assert recv_prn

    def test_financial_services_register_api_client___search_prn__inadequately_specced_fund__json_array_of_matching_records__response_returned_ok(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a successful PRN search for existing, unique funds
        recv_recs = test_client.search_prn('jupiter')
        assert isinstance(recv_recs, list)
        assert all(isinstance(rec, dict) for rec in recv_recs)

    def test_financial_services_register_api_client__get_fund(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the details of an
        # existing fund, 'Jupiter Asia Pacific Income Fund (IRL)' (PRN '635641')
        try:
            recv_response = test_client.get_fund('635641')
            assert recv_response.ok
            assert recv_response.data
        except AssertionError:
            pass

        # Covers the case of a request for the details of a non-existent fund
        recv_response = test_client.get_fund('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_fund_names(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the alternate/secondary names
        # details of existing fund with PRN 185045
        recv_response = test_client.get_fund_names('185045')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the alternate/secondary name
        # details of an existing fund with PRN 1006826
        recv_response = test_client.get_fund_names('1006826')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the alternate/secondary name
        # details of a non-existent fund
        recv_response = test_client.get_fund_names('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_fund_subfunds(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the case of a request for the subfund details of an
        # existing fund with PRN 185045
        recv_response = test_client.get_fund_subfunds('185045')
        assert recv_response.ok
        assert recv_response.data

        # Covers the case of a request for the subfund details of an
        # existing fund with PRN 1006826
        recv_response = test_client.get_fund_subfunds('1006826')
        assert recv_response.ok
        assert not recv_response.data

        # Covers the case of a request for the subfund details of a
        # non-existent fund
        recv_response = test_client.get_fund_subfunds('1234567890')
        assert recv_response.ok
        assert not recv_response.data

    def test_financial_services_register_api_client__get_regulated_markets(self):
        test_client = FinancialServicesRegisterApiClient(self._api_username, self._api_key)

        # Covers the regulated markets API endpoint, which ATM returns a
        # list of markets regulated by UK and/or EU/EEA financial legislation.
        #
        # We don't bother to check the exact list of markets returned by the
        # endpoint, as this may change - it is enough to check that the endpoint
        # should provide some data.
        recv_response = test_client.get_regulated_markets()
        assert recv_response.ok
        assert recv_response.data
