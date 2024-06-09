import requests
from types import *


class ClientSDK:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    def _make_authenticated_request(
        self, method: str, endpoint: str, params: dict = None, json: dict = None
    ):
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.request(
            method, url, headers=headers, params=params, json=json
        )
        return response

    def get_activity(self, limit: int = 50, offset: int = 0):
        params = {"limit": limit, "offset": offset}
        return self._make_authenticated_request("GET", "/activity", params=params)

    def list_vaults(self, filter: str = None):
        params = {"filter": filter} if filter else {}
        return self._make_authenticated_request("GET", "/vaults", params=params)

    def get_vault_details(self, vaultUuid: str):
        return self._make_authenticated_request("GET", f"/vaults/{vaultUuid}")

    def get_all_items(self, vaultUuid: str, filter: str = None):
        params = {"filter": filter} if filter else {}
        return self._make_authenticated_request(
            "GET", f"/vaults/{vaultUuid}/items", params=params
        )

    def create_new_item(self, vaultUuid: str, item: FullItem):
        return self._make_authenticated_request(
            "POST", f"/vaults/{vaultUuid}/items", json=item
        )

    def get_item_details_by_id(self, vaultUuid: str, itemUuid: str):
        return self._make_authenticated_request(
            "GET", f"/vaults/{vaultUuid}/items/{itemUuid}"
        )

    def update_item_details(self, vaultUuid: str, itemUuid: str, item: FullItem):
        return self._make_authenticated_request(
            "PUT", f"/vaults/{vaultUuid}/items/{itemUuid}", json=item
        )

    def delete_item_by_id(self, vaultUuid: str, itemUuid: str):
        return self._make_authenticated_request(
            "DELETE", f"/vaults/{vaultUuid}/items/{itemUuid}"
        )

    def update_subset_attributes(self, vaultUuid: str, itemUuid: str, patch: Patch):
        return self._make_authenticated_request(
            "PATCH", f"/vaults/{vaultUuid}/items/{itemUuid}", json=patch
        )

    def get_all_files_inside_item(
        self, vaultUuid: str, itemUuid: str, inline_files: bool = None
    ):
        params = {"inline_files": inline_files} if inline_files is not None else {}
        return self._make_authenticated_request(
            "GET", f"/vaults/{vaultUuid}/items/{itemUuid}/files", params=params
        )

    def get_file_details(
        self, vaultUuid: str, itemUuid: str, fileUuid: str, inline_files: bool = None
    ):
        params = {"inline_files": inline_files} if inline_files is not None else {}
        return self._make_authenticated_request(
            "GET",
            f"/vaults/{vaultUuid}/items/{itemUuid}/files/{fileUuid}",
            params=params,
        )

    def get_file_content(self, vaultUuid: str, itemUuid: str, fileUuid: str):
        return self._make_authenticated_request(
            "GET", f"/vaults/{vaultUuid}/items/{itemUuid}/files/{fileUuid}/content"
        )

    def check_liveness(self):
        return self._make_authenticated_request("GET", "/heartbeat")
