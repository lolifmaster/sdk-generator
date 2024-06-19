import requests
from types import *


class ApaleoInventorySDK:
    def __init__(self, access_token: str, base_url: str = "https://api.apaleo.com"):
        self.access_token = access_token
        self.base_url = base_url

    def _make_authenticated_request(
        self, method: str, url: str, **kwargs
    ) -> requests.Response:
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        return requests.request(method, url, **kwargs)

    def list_properties(self, query_params: Dict = None) -> requests.Response:
        """Fetch a list of properties with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/properties"
        return self._make_authenticated_request("GET", url, params=query_params)

    def create_property(
        self, property_data: CreatePropertyModel, idempotency_key: str = None
    ) -> requests.Response:
        """Create a new property with the provided data."""
        url = f"{self.base_url}/inventory/v1/properties"
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._make_authenticated_request(
            "POST", url, json=property_data, headers=headers
        )

    def get_total_property_count(self) -> requests.Response:
        """Get the total count of properties."""
        url = f"{self.base_url}/inventory/v1/properties/$count"
        return self._make_authenticated_request("GET", url)

    def get_property_by_id(
        self, property_id: str, query_params: Dict = None
    ) -> requests.Response:
        """Fetch a property by its ID with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/properties/{property_id}"
        return self._make_authenticated_request("GET", url, params=query_params)

    def modify_property_details(
        self, property_id: str, property_data: PropertyModifyDetailsRequest
    ) -> requests.Response:
        """Modify the details of a property with the provided data."""
        url = f"{self.base_url}/inventory/v1/properties/{property_id}"
        return self._make_authenticated_request("PATCH", url, json=property_data)

    def clone_property(
        self,
        property_id: str,
        property_data: CreatePropertyModel,
        idempotency_key: str = None,
    ) -> requests.Response:
        """Clone a property with the provided data."""
        url = f"{self.base_url}/inventory/v1/property-actions/{property_id}/clone"
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._make_authenticated_request(
            "POST", url, json=property_data, headers=headers
        )

    def archive_property(self, property_id: str) -> requests.Response:
        """Archive a property by its ID."""
        url = f"{self.base_url}/inventory/v1/property-actions/{property_id}/archive"
        return self._make_authenticated_request("PUT", url)

    def move_property_to_live(self, property_id: str) -> requests.Response:
        """Move a property to live status by its ID."""
        url = f"{self.base_url}/inventory/v1/property-actions/{property_id}/set-live"
        return self._make_authenticated_request("PUT", url)

    def reset_property_data(self, property_id: str) -> requests.Response:
        """Reset the data of a property by its ID."""
        url = f"{self.base_url}/inventory/v1/property-actions/{property_id}/reset"
        return self._make_authenticated_request("PUT", url)

    def get_supported_countries_list(self) -> requests.Response:
        """Fetch a list of supported countries."""
        url = f"{self.base_url}/inventory/v1/types/countries"
        return self._make_authenticated_request("GET", url)

    def update_unit_properties(
        self, unit_id: str, property_data: PropertyModifyDetailsRequest
    ) -> requests.Response:
        """Update the properties of a unit by its ID with the provided data."""
        url = f"{self.base_url}/inventory/v1/units/{unit_id}"
        return self._make_authenticated_request("PATCH", url, json=property_data)

    def get_unit_by_id(
        self, unit_id: str, query_params: Dict = None
    ) -> requests.Response:
        """Fetch a unit by its ID with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/units/{unit_id}"
        return self._make_authenticated_request("GET", url, params=query_params)

    def delete_unit_by_id(self, unit_id: str) -> requests.Response:
        """Delete a unit by its ID."""
        url = f"{self.base_url}/inventory/v1/units/{unit_id}"
        return self._make_authenticated_request("DELETE", url)

    def update_units_attributes(
        self, query_params: Dict, property_data: PropertyModifyDetailsRequest
    ) -> requests.Response:
        """Update the attributes of multiple units with the provided data and query parameters."""
        url = f"{self.base_url}/inventory/v1/units"
        return self._make_authenticated_request(
            "PATCH", url, params=query_params, json=property_data
        )

    def list_units(self, query_params: Dict = None) -> requests.Response:
        """Fetch a list of units with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/units"
        return self._make_authenticated_request("GET", url, params=query_params)

    def create_unit(
        self, unit_data: CreateUnitModel, idempotency_key: str = None
    ) -> requests.Response:
        """Create a new unit with the provided data."""
        url = f"{self.base_url}/inventory/v1/units"
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._make_authenticated_request("POST", url, json=unit_data)

    def get_unit_count(self, query_params: Dict = None) -> requests.Response:
        """Get the total count of units with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/units/$count"
        return self._make_authenticated_request("GET", url, params=query_params)

    def bulk_create_units(
        self, bulk_unit_data: BulkCreateUnitsModel, idempotency_key: str = None
    ) -> requests.Response:
        """Bulk create units with the provided data."""
        url = f"{self.base_url}/inventory/v1/units/bulk"
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._make_authenticated_request("POST", url, json=bulk_unit_data)

    def get_unit_attribute_by_id(self, attribute_id: str) -> requests.Response:
        """Fetch a unit attribute by its ID."""
        url = f"{self.base_url}/inventory/v1/unit-attributes/{attribute_id}"
        return self._make_authenticated_request("GET", url)

    def modify_unit_attribute_description(
        self, attribute_id: str, property_data: PropertyModifyDetailsRequest
    ) -> requests.Response:
        """Modify the description of a unit attribute with the provided data."""
        url = f"{self.base_url}/inventory/v1/unit-attributes/{attribute_id}"
        return self._make_authenticated_request("PATCH", url, json=property_data)

    def delete_unit_attribute_by_id(self, attribute_id: str) -> requests.Response:
        """Delete a unit attribute by its ID."""
        url = f"{self.base_url}/inventory/v1/unit-attributes/{attribute_id}"
        return self._make_authenticated_request("DELETE", url)

    def list_unit_attributes(self, query_params: Dict = None) -> requests.Response:
        """Fetch a list of unit attributes with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/unit-attributes"
        return self._make_authenticated_request("GET", url, params=query_params)

    def create_new_unit_attribute(
        self,
        attribute_data: CreateUnitAttributeDefinitionModel,
        idempotency_key: str = None,
    ) -> requests.Response:
        """Create a new unit attribute with the provided data."""
        url = f"{self.base_url}/inventory/v1/unit-attributes"
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._make_authenticated_request("POST", url, json=attribute_data)

    def create_new_unit_group(
        self, unit_group_data: CreateUnitGroupModel, idempotency_key: str = None
    ) -> requests.Response:
        """Create a new unit group with the provided data."""
        url = f"{self.base_url}/inventory/v1/unit-groups"
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._make_authenticated_request("POST", url, json=unit_group_data)

    def get_all_unit_groups(self, query_params: Dict = None) -> requests.Response:
        """Fetch a list of all unit groups with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/unit-groups"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_unit_group_count(self, query_params: Dict = None) -> requests.Response:
        """Get the total count of unit groups with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/unit-groups/$count"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_unit_group_by_id(
        self, unit_group_id: str, query_params: Dict = None
    ) -> requests.Response:
        """Fetch a unit group by its ID with optional query parameters."""
        url = f"{self.base_url}/inventory/v1/unit-groups/{unit_group_id}"
        return self._make_authenticated_request("GET", url, params=query_params)

    def update_unit_group(
        self, unit_group_id: str, unit_group_data: ReplaceUnitGroupModel
    ) -> requests.Response:
        """Update a unit group by its ID with the provided data."""
        url = f"{self.base_url}/inventory/v1/unit-groups/{unit_group_id}"
        return self._make_authenticated_request("PUT", url, json=unit_group_data)

    def delete_unit_group_by_id(self, unit_group_id: str) -> requests.Response:
        """Delete a unit group by its ID."""
        url = f"{self.base_url}/inventory/v1/unit-groups/{unit_group_id}"
        return self._make_authenticated_request("DELETE", url)
