import json
import requests
from pprint import pprint
from typing import TypedDict, Union


class Credentials(TypedDict):
    email: str
    password: str


class APIClient:
    def __init__(self, credentials: Credentials):
        if 'email' not in credentials or 'password' not in credentials:
            raise ValueError("Credentials must contain 'email' and 'password' keys.")

        self.base_url: str = 'http://127.0.0.1:8000'
        self.credentials: dict[str, str] = credentials
        self.access_token: str = self._get_access_token()

    def _get_access_token(self) -> str:
        url: str = f"{self.base_url}/api/token/"

        headers: dict[str, str] = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        response: requests.Response = requests.post(url, data=json.dumps(self.credentials), headers=headers)
        response.raise_for_status()
        return response.json().get('access', '')

    def _make_request(
            self,
            method: str,
            path: str,
            params: dict[str, Union[str, None]] = None,
            data: dict[str, Union[str, None]] = None,
            headers: dict[str, str] = None
    ):
        url: str = f"{self.base_url}{path}"

        full_headers: dict[str, str] = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        if headers:
            full_headers.update(headers)

        if method == 'get':
            response: requests.Response = requests.get(url, params=params, headers=full_headers)
        elif method == 'post':
            response: requests.Response = requests.post(url, data=json.dumps(data), headers=full_headers)
        elif method == 'delete':
            response: requests.Response = requests.delete(url, headers=full_headers)
        elif method == 'patch':
            response: requests.Response = requests.patch(url, data=json.dumps(data), headers=full_headers)
        elif method == 'put':
            response: requests.Response = requests.put(url, data=json.dumps(data), headers=full_headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()

    def _make_authenticated_request(
            self,
            method: str,
            path: str,
            params: dict[str, Union[str, None]] = None,
            data: dict[str, Union[str, None]] = None
    ):
        headers: dict[str, str] = {
            'Authorization': f'Bearer {self.access_token}',
        }

        return self._make_request(method, path, params=params, data=data, headers=headers)

    # Cart Endpoints
    def cart_list(self):
        return self._make_request('get', '/api/cart/')

    def cart_read(self, cart_id: str):
        return self._make_request('get', f'/api/cart/{cart_id}/')

    # Categories Endpoints
    def categories_list(self):
        return self._make_request('get', '/api/categories/')

    def categories_read(self, category_id: str):
        return self._make_request('get', f'/api/categories/{category_id}/')

    # Order Endpoints
    def order_list(self, cursor: str = None):
        params: dict[str, Union[str, None]] = {'cursor': cursor} if cursor else {}
        return self._make_authenticated_request('get', '/api/orders/', params=params)

    def order_create(self):
        return self._make_authenticated_request('post', '/api/orders/')

    def order_delete(self, order_id: str):
        return self._make_authenticated_request('delete', f'/api/orders/{order_id}/')

    def order_read(self, order_id: str):
        return self._make_authenticated_request('get', f'/api/orders/{order_id}/')

    def order_partial_update(
            self,
            order_id: str,
            data: dict[str, Union[str, None]]
    ):
        return self._make_authenticated_request('patch', f'/api/orders/{order_id}/', data=data)

    def order_update(
            self,
            order_id: str,
            data: dict[str, Union[str, None]]
    ):
        return self._make_authenticated_request('put', f'/api/orders/{order_id}/', data=data)

    # Products Endpoints
    def products_list(
            self,
            cursor: str = None,
            search: str = None
    ):
        params: dict[str, Union[str, None]] = {'cursor': cursor, 'search': search} if cursor or search else {}
        return self._make_authenticated_request('get', '/api/products/', params=params)

    def products_read(
            self,
            product_id: str,
            search: str = None
    ):
        params: dict[str, Union[str, None]] = {'search': search} if search else {}
        return self._make_request('get', f'/api/products/{product_id}/', params=params)

    # Token Endpoint
    def token_create(
            self,
            credentials: Credentials
    ):
        return self._make_request('post', '/api/token/', data=credentials)


# Example Usage:
if __name__ == "__main__":
    api_client = APIClient({'email': 'a@a.com', 'password': 'bedeltoxD'})
    # Make API requests
    products_list_response = api_client.products_list()
    pprint(products_list_response)
