
import requests
from types import *


class ApaleoInventorySDK:
    def __init__(self, base_url='https://api.apaleo.com'):
        self.base_url = base_url

    def _make_authenticated_request(self, method, url, headers=None, params=None, json=None):
        # Replace with your authentication logic
        # Example assumes OAuth2 token
        headers = headers or {}
        headers['Authorization'] = 'Bearer YOUR_ACCESS_TOKEN_HERE'
        response = requests.request(method, url, headers=headers, params=params, json=json)
        return response

    def Property_listGet(self, status: list[str] = None, includeArchived: bool = None, countryCode: list[str] = None,
                         pageNumber: int = 1, pageSize: int = None, expand: list[str] = None) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/properties"
        headers = {}
        params = {
            'status': status,
            'includeArchived': includeArchived,
            'countryCode': countryCode,
            'pageNumber': pageNumber,
            'pageSize': pageSize,
            'expand': expand
        }
        return self._make_authenticated_request('GET', url, headers=headers, params=params)

    def Property_create(self, Idempotency_Key: str, data: dict) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/properties"
        headers = {'Idempotency-Key': Idempotency_Key}
        return self._make_authenticated_request('POST', url, headers=headers, json=data)

    def Property_getTotalCount(self) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/properties/count"
        return self._make_authenticated_request('GET', url)

    def Property_getById(self, id: str, languages: list[str] = None, expand: list[str] = None) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/properties/{id}"
        params = {
            'languages': languages,
            'expand': expand
        }
        return self._make_authenticated_request('GET', url, params=params)

    def Property_modifyDetails(self, id: str, data: dict) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/properties/{id}"
        return self._make_authenticated_request('PATCH', url, json=data)

    def PropertyActions_cloneProperty(self, id: str, Idempotency_Key: str = None) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/property-actions/{id}/clone"
        headers = {}
        if Idempotency_Key:
            headers['Idempotency-Key'] = Idempotency_Key
        return self._make_authenticated_request('POST', url, headers=headers)

    def PropertyActions_archiveProperty(self, id: str) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/property-actions/{id}/archive"
        return self._make_authenticated_request('PUT', url)

    def PropertyActions_moveToLive(self, id: str) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/property-actions/{id}/set-live"
        return self._make_authenticated_request('PUT', url)

    def PropertyActions_resetPropertyData(self, id: str) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/property-actions/{id}/reset"
        return self._make_authenticated_request('PUT', url)

    def Types_supportedCountriesList(self) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/types/countries"
        return self._make_authenticated_request('GET', url)

    def Unit_updateProperties(self, id: str, data: dict) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/units/{id}"
        return self._make_authenticated_request('PATCH', url, json=data)

    def Unit_getById(self, id: str, languages: list[str] = None, expand: list[str] = None) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/units/{id}"
        params = {
            'languages': languages,
            'expand': expand
        }
        return self._make_authenticated_request('GET', url, params=params)

    def Unit_deleteById(self, id: str) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/units/{id}"
        return self._make_authenticated_request('DELETE', url)

    def Unit_updateUnitsAttributes(self, unitIds: list[str], data: dict) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/units"
        params = {
            'unitIds': unitIds
        }
        return self._make_authenticated_request('PATCH', url, params=params)

    def Unit_listUnits(self, propertyId: str = None, unitGroupId: str = None, unitGroupIds: list[str] = None,
                       unitAttributeIds: list[str] = None, isOccupied: bool = None, maintenanceType: str = None,
                       condition: str = None, textSearch: str = None, pageNumber: int = 1, pageSize: int = None,
                       expand: list[str] = None) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/units"
        params = {
            'propertyId': propertyId,
            'unitGroupId': unitGroupId,
            'unitGroupIds': unitGroupIds,
            'unitAttributeIds': unitAttributeIds,
            'isOccupied': isOccupied,
            'maintenanceType': maintenanceType,
            'condition': condition,
            'textSearch': textSearch,
            'pageNumber': pageNumber,
            'pageSize': pageSize,
            'expand': expand
        }
        return self._make_authenticated_request('GET', url, params=params)

    def Unit_create(self, Idempotency_Key: str, data: CreateUnitModel) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/units"
        headers = {'Idempotency-Key': Idempotency_Key}
        return self._make_authenticated_request('POST', url, headers=headers, json=data)

    def Unit_getCount(self, propertyId: str = None, unitGroupId: str = None, unitGroupIds: list[str] = None,
                      unitAttributeIds: list[str] = None, isOccupied: bool = None, maintenanceType: str = None,
                      condition: str = None, textSearch: str = None) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/units/count"
        params = {
            'propertyId': propertyId,
            'unitGroupId': unitGroupId,
            'unitGroupIds': unitGroupIds,
            'unitAttributeIds': unitAttributeIds,
            'isOccupied': isOccupied,
            'maintenanceType': maintenanceType,
            'condition': condition,
            'textSearch': textSearch
        }
        return self._make_authenticated_request('GET', url, params=params)

    def Unit_bulkCreateUnits(self, Idempotency_Key: str, data: BulkCreateUnitsModel) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/units/bulk"
        headers = {'Idempotency-Key': Idempotency_Key}
        return self._make_authenticated_request('POST', url, headers=headers, json=data)

    def UnitAttribute_getById(self, id: str) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/unit-attributes/{id}"
        return self._make_authenticated_request('GET', url)

    def UnitAttribute_modifyDescription(self, id: str, data: dict) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/unit-attributes/{id}"
        return self._make_authenticated_request('PATCH', url, json=data)

    def UnitAttribute_deleteById(self, id: str) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/unit-attributes/{id}"
        return self._make_authenticated_request('DELETE', url)

    def UnitAttribute_listAttributes(self, pageNumber: int = 1, pageSize: int = None) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/unit-attributes"
        params = {
            'pageNumber': pageNumber,
            'pageSize': pageSize
        }
        return self._make_authenticated_request('GET', url, params=params)

    def UnitAttribute_createNewAttribute(self, Idempotency_Key: str, data: CreateUnitAttributeDefinitionModel) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/unit-attributes"
        headers = {'Idempotency-Key': Idempotency_Key}
        return self._make_authenticated_request('POST', url, headers=headers, json=data)

    def UnitGroup_createNewGroup(self, Idempotency_Key: str, data: CreateUnitGroupModel) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/unit-groups"
        headers = {'Idempotency-Key': Idempotency_Key}
        return self._make_authenticated_request('POST', url, headers=headers, json=data)

    def UnitGroup_getAll(self, propertyId: str = None, unitGroupTypes: list[str] = None, pageNumber: int = 1,
                         pageSize: int = None, expand: list[str] = None) -> requests.Response:
        url = f"{self.base_url}/inventory/v1/unit-groups"
        params = {
            'propertyId': propertyId,
            'unitGroupTypes': unitGroupTypes,
            'pageNumber': pageNumber,
            'pageSize': pageSize
        }