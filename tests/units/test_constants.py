# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --

# -- Internal libraries --
from financial_services_register_api.constants import FINANCIAL_SERVICES_REGISTER_API_CONSTANTS as API_CONSTANTS


class TestFinancialServicesRegisterApiConstants:

	def test_fsr_api_constants(self):
		assert API_CONSTANTS.API_VERSION.value == 'V0.1'
		assert API_CONSTANTS.BASEURL.value == 'https://register.fca.org.uk/services/V0.1'
		assert API_CONSTANTS.RESOURCE_TYPES.value == {
			'firm': {'type_name': 'firm', 'endpoint_base': 'Firm'},
			'fund': {'type_name': 'fund', 'endpoint_base': 'CIS'},
			'individual': {'type_name': 'individual', 'endpoint_base': 'Individuals'}
		}
