import requests
from types import (
    FlightsCalculateAttributesBenefitsRequest,
    FlightsCalculateFareAttributesRequest,
    TravelersCreateProfileRequest,
    MembershipsCreateFrequentFlyerProgramMembershipRequest,
)


class MilefyClient:
    def __init__(self, api_key: str, base_url: str = "https://milefy-api.30k.com"):
        self.api_key = api_key
        self.base_url = base_url

    def _make_authenticated_request(self, method: str, url: str, **kwargs):
        headers = kwargs.get("headers", {}).copy()
        headers["Authorization"] = f"Bearer {self.api_key}"
        kwargs["headers"] = headers
        return requests.request(method, url, **kwargs)

    def get_frequent_flyer_programs(self, authentication: str = None):
        """Get the list of frequent flyer programs."""
        url = f"{self.base_url}/programs"
        params = {}
        if authentication:
            params["authentication"] = authentication
        return self._make_authenticated_request("GET", url, params=params)

    def get_frequent_flyer_program(self, code: str = None):
        """Get a specific frequent flyer program by code."""
        url = (
            f"{self.base_url}/programs/{code}" if code else f"{self.base_url}/programs"
        )
        return self._make_authenticated_request("GET", url)

    def get_status_benefit_type_collection(self):
        """Get the collection of status benefit types."""
        url = f"{self.base_url}/benefits"
        return self._make_authenticated_request("GET", url)

    def get_status_benefit_type(self, code: str):
        """Get a specific status benefit type by code."""
        url = f"{self.base_url}/benefits/{code}"
        return self._make_authenticated_request("GET", url)

    def get_fare_attribute_type_collection(self):
        """Get the collection of fare attribute types."""
        url = f"{self.base_url}/attributes"
        return self._make_authenticated_request("GET", url)

    def get_fare_attribute_type(self, code: str):
        """Get a specific fare attribute type by code."""
        url = f"{self.base_url}/attributes/{code}"
        return self._make_authenticated_request("GET", url)

    def calculate_attributes_benefits(
        self,
        request: FlightsCalculateAttributesBenefitsRequest,
        traveler: str,
        scope: str = None,
        sourceClientId: str = None,
    ):
        """Calculate attributes and benefits for a traveler."""
        url = f"{self.base_url}/calculate"
        params = {"traveler": traveler}
        if scope:
            params["scope"] = scope
        if sourceClientId:
            params["sourceClientId"] = sourceClientId
        return self._make_authenticated_request(
            "POST", url, json=request, params=params
        )

    def calculate_fare_attributes(
        self, request: FlightsCalculateFareAttributesRequest, scope: str = "attributes"
    ):
        """Calculate fare attributes for a traveler."""
        url = f"{self.base_url}/fare-attributes"
        params = {"scope": scope}
        return self._make_authenticated_request(
            "POST", url, json=request, params=params
        )

    def create_traveler(self, request: TravelersCreateProfileRequest):
        """Create a new traveler profile."""
        url = f"{self.base_url}/travelers"
        return self._make_authenticated_request("POST", url, json=request)

    def get_traveler_collection(self, offset: int = None, limit: int = None):
        """Get a collection of traveler profiles."""
        url = f"{self.base_url}/travelers"
        params = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        return self._make_authenticated_request("GET", url, params=params)

    def get_traveler(self, travelerId: str):
        """Get a specific traveler profile by ID."""
        url = f"{self.base_url}/travelers/{travelerId}"
        return self._make_authenticated_request("GET", url)

    def update_traveler(self, travelerId: str, request: TravelersCreateProfileRequest):
        """Update a traveler profile by ID."""
        url = f"{self.base_url}/travelers/{travelerId}"
        return self._make_authenticated_request("PUT", url, json=request)

    def remove_traveler(self, travelerId: str):
        """Remove a traveler profile by ID."""
        url = f"{self.base_url}/travelers/{travelerId}"
        return self._make_authenticated_request("DELETE", url)

    def create_frequent_flyer_program_membership(
        self,
        travelerId: str,
        request: MembershipsCreateFrequentFlyerProgramMembershipRequest,
    ):
        """Create a new frequent flyer program membership for a traveler."""
        url = f"{self.base_url}/travelers/{travelerId}/memberships"
        return self._make_authenticated_request("POST", url, json=request)

    def get_membership_collection(self, travelerId: str):
        """Get a collection of frequent flyer program memberships for a traveler."""
        url = f"{self.base_url}/travelers/{travelerId}/memberships"
        return self._make_authenticated_request("GET", url)

    def get_membership_by_code(self, travelerId: str, programCode: str):
        """Get a specific frequent flyer program membership by program code."""
        url = f"{self.base_url}/travelers/{travelerId}/memberships/{programCode}"
        return self._make_authenticated_request("GET", url)

    def edit_traveler_membership(
        self,
        travelerId: str,
        programCode: str,
        request: MembershipsCreateFrequentFlyerProgramMembershipRequest,
    ):
        """Edit a frequent flyer program membership for a traveler."""
        url = f"{self.base_url}/travelers/{travelerId}/memberships/{programCode}"
        return self._make_authenticated_request("PUT", url, json=request)

    def delete_membership(self, travelerId: str, programCode: str):
        """Delete a frequent flyer program membership by program code."""
        url = f"{self.base_url}/travelers/{travelerId}/memberships/{programCode}"
        return self._make_authenticated_request("DELETE", url)
