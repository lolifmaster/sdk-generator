import requests


class AffinityAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def _make_authenticated_request(self, method: str, path: str, params: dict = None):
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, headers=headers, params=params)
        return response

    def Auth_getCurrentUser(self):
        return self._make_authenticated_request("GET", "/v2/auth/whoami")

    def Companies_getAll(
        self,
        cursor: str = None,
        limit: int = 100,
        ids: list[int] = None,
        fieldIds: list[str] = None,
        fieldTypes: list[str] = None,
    ):
        params = {
            "cursor": cursor,
            "limit": limit,
            "ids": ids,
            "fieldIds": fieldIds,
            "fieldTypes": fieldTypes,
        }
        return self._make_authenticated_request("GET", "/v2/companies", params=params)

    def Companies_getFieldMetadata(self, cursor: str = None, limit: int = 100):
        params = {"cursor": cursor, "limit": limit}
        return self._make_authenticated_request(
            "GET", "/v2/companies/fields", params=params
        )

    def Companies_getSingleCompany(
        self, id: int, fieldIds: list[str] = None, fieldTypes: list[str] = None
    ):
        params = {"fieldIds": fieldIds, "fieldTypes": fieldTypes}
        path = f"/v2/companies/{id}"
        return self._make_authenticated_request("GET", path, params=params)

    def Companies_getListsMetadata(self, id: int, cursor: str = None, limit: int = 100):
        params = {"cursor": cursor, "limit": limit}
        path = f"/v2/companies/{id}/lists"
        return self._make_authenticated_request("GET", path, params=params)

    def Companies_getListEntries(self, id: int, cursor: str = None, limit: int = 100):
        params = {"cursor": cursor, "limit": limit}
        path = f"/v2/companies/{id}/list-entries"
        return self._make_authenticated_request("GET", path, params=params)

    def Lists_getMetadata(self, cursor: str = None, limit: int = 100):
        params = {"cursor": cursor, "limit": limit}
        return self._make_authenticated_request("GET", "/v2/lists", params=params)

    def Lists_getAllListEntries(
        self,
        listId: int,
        cursor: str = None,
        limit: int = 100,
        fieldIds: list[str] = None,
        fieldTypes: list[str] = None,
    ):
        params = {
            "cursor": cursor,
            "limit": limit,
            "fieldIds": fieldIds,
            "fieldTypes": fieldTypes,
        }
        path = f"/v2/lists/{listId}/list-entries"
        return self._make_authenticated_request("GET", path, params=params)

    def Lists_getMetadataSingle(self, listId: int):
        path = f"/v2/lists/{listId}"
        return self._make_authenticated_request("GET", path)

    def Lists_getFieldMetadata(self, listId: int, cursor: str = None, limit: int = 100):
        params = {"cursor": cursor, "limit": limit}
        path = f"/v2/lists/{listId}/fields"
        return self._make_authenticated_request("GET", path, params=params)

    def Lists_listSavedViewsMetadata(
        self, listId: int, cursor: str = None, limit: int = 100
    ):
        params = {"cursor": cursor, "limit": limit}
        path = f"/v2/lists/{listId}/saved-views"
        return self._make_authenticated_request("GET", path, params=params)

    def Lists_getSavedViewListEntries(
        self, listId: int, viewId: int, cursor: str = None, limit: int = 100
    ):
        params = {"cursor": cursor, "limit": limit}
        path = f"/v2/lists/{listId}/saved-views/{viewId}/list-entries"
        return self._make_authenticated_request("GET", path, params=params)

    def Lists_getSavedViewMetadata(self, listId: int, viewId: int):
        path = f"/v2/lists/{listId}/saved-views/{viewId}"
        return self._make_authenticated_request("GET", path)

    def Opportunities_getAll(
        self, cursor: str = None, limit: int = 100, ids: list[int] = None
    ):
        params = {"cursor": cursor, "limit": limit, "ids": ids}
        return self._make_authenticated_request(
            "GET", "/v2/opportunities", params=params
        )

    def Opportunities_getBasicInfo(self, id: int):
        path = f"/v2/opportunities/{id}"
        return self._make_authenticated_request("GET", path)

    def Persons_getAll(
        self,
        cursor: str = None,
        limit: int = 100,
        ids: list[int] = None,
        fieldIds: list[str] = None,
        fieldTypes: list[str] = None,
    ):
        params = {
            "cursor": cursor,
            "limit": limit,
            "ids": ids,
            "fieldIds": fieldIds,
            "fieldTypes": fieldTypes,
        }
        return self._make_authenticated_request("GET", "/v2/persons", params=params)

    def Persons_getMetadata(self, cursor: str = None, limit: int = 100):
        params = {"cursor": cursor, "limit": limit}
        return self._make_authenticated_request(
            "GET", "/v2/persons/fields", params=params
        )

    def Persons_getPersonFieldData(
        self, id: int, fieldIds: list[str] = None, fieldTypes: list[str] = None
    ):
        params = {"fieldIds": fieldIds, "fieldTypes": fieldTypes}
        path = f"/v2/persons/{id}"
        return self._make_authenticated_request("GET", path, params=params)

    def Persons_getListsMetadata(self, id: int, cursor: str = None, limit: int = 100):
        params = {"cursor": cursor, "limit": limit}
        path = f"/v2/persons/{id}/lists"
        return self._make_authenticated_request("GET", path, params=params)

    def Persons_paginateEntries(self, id: int, cursor: str = None, limit: int = 100):
        params = {"cursor": cursor, "limit": limit}
        path = f"/v2/persons/{id}/list-entries"
        return self._make_authenticated_request("GET", path, params=params)
