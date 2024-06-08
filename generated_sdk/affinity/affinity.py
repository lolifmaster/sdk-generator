import requests


class AffinityClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.affinity.co"

    def _make_authenticated_request(self, method, url, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")
        return response

    def get_current_user(self):
        """Retrieve the current user's information."""
        url = f"{self.base_url}/v2/auth/whoami"
        return self._make_authenticated_request("GET", url)

    def get_all_companies(self, query_params=None):
        """Retrieve all companies with optional query parameters."""
        url = f"{self.base_url}/v2/companies"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_company_fields_metadata(self, query_params=None):
        """Retrieve metadata on company fields."""
        url = f"{self.base_url}/v2/companies/fields"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_single_company(self, company_id, query_params=None):
        """Retrieve a single company by ID."""
        url = f"{self.base_url}/v2/companies/{company_id}"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_companies_lists_metadata(self, company_id, query_params=None):
        """Retrieve metadata on a company's lists."""
        url = f"{self.base_url}/v2/companies/{company_id}/lists"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_companies_list_entries(self, company_id, query_params=None):
        """Retrieve a company's list entries."""
        url = f"{self.base_url}/v2/companies/{company_id}/list-entries"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_all_lists_metadata(self, query_params=None):
        """Retrieve metadata on all lists."""
        url = f"{self.base_url}/v2/lists"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_all_list_entries(self, list_id, query_params=None):
        """Retrieve all list entries for a specific list."""
        url = f"{self.base_url}/v2/lists/{list_id}/list-entries"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_metadata_single(self, list_id):
        """Retrieve metadata for a single list."""
        url = f"{self.base_url}/v2/lists/{list_id}"
        return self._make_authenticated_request("GET", url)

    def get_lists_field_metadata(self, list_id, query_params=None):
        """Retrieve metadata on a single list's fields."""
        url = f"{self.base_url}/v2/lists/{list_id}/fields"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_saved_views_metadata(self, list_id, query_params=None):
        """Retrieve metadata on saved views for a list."""
        url = f"{self.base_url}/v2/lists/{list_id}/saved-views"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_saved_view_list_entries(self, list_id, view_id, query_params=None):
        """Retrieve all list entries for a specific saved view."""
        url = f"{self.base_url}/v2/lists/{list_id}/saved-views/{view_id}/list-entries"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_saved_view_metadata(self, list_id, view_id):
        """Retrieve metadata for a single saved view."""
        url = f"{self.base_url}/v2/lists/{list_id}/saved-views/{view_id}"
        return self._make_authenticated_request("GET", url)

    def get_all_opportunities(self, query_params=None):
        """Retrieve all opportunities with optional query parameters."""
        url = f"{self.base_url}/v2/opportunities"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_opportunity_basic_info(self, opportunity_id):
        """Retrieve basic information for a single opportunity."""
        url = f"{self.base_url}/v2/opportunities/{opportunity_id}"
        return self._make_authenticated_request("GET", url)

    def get_all_persons(self, query_params=None):
        """Retrieve all persons with optional query parameters."""
        url = f"{self.base_url}/v2/persons"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_persons_metadata(self, query_params=None):
        """Retrieve metadata on person fields."""
        url = f"{self.base_url}/v2/persons/fields"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_person_field_data(self, person_id, query_params=None):
        """Retrieve field data for a single person."""
        url = f"{self.base_url}/v2/persons/{person_id}"
        return self._make_authenticated_request("GET", url, params=query_params)

    def get_persons_lists_metadata(self, person_id, query_params=None):
        """Retrieve metadata on a person's lists."""
        url = f"{self.base_url}/v2/persons/{person_id}/lists"
        return self._make_authenticated_request("GET", url, params=query_params)

    def paginate_person_entries(self, person_id, query_params=None):
        """Retrieve a person's list entries with pagination."""
        url = f"{self.base_url}/v2/persons/{person_id}/list-entries"
        return self._make_authenticated_request("GET", url, params=query_params)
