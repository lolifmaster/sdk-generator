import requests
from typing import Optional, Dict


class FlickrClient:
    def __init__(self, api_key: str, oauth_token: str):
        """
        Initializes the FlickrClient with the necessary authentication details.
        """
        self.base_url = "https://api.flickr.com/services"
        self.api_key = api_key
        self.oauth_token = oauth_token

    def _make_authenticated_request(
        self, method: str, path: str, params: Optional[Dict] = None
    ) -> requests.Response:
        """
        Makes an authenticated request to the Flickr API.
        """
        url = self.base_url + path
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.oauth_token,
        }
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, data=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        else:
            return response

    def get_access_token(self) -> requests.Response:
        """
        Retrieves an access token.
        """
        path = "/oauth/access_token"
        return self._make_authenticated_request("GET", path)

    def get_favorites_context(
        self, photo_id: str, user_id: Optional[str] = None
    ) -> requests.Response:
        """
        Retrieves the context for a favorite photo.
        """
        path = "/restmethodflickr.favorites.getContext"
        params = {"api_key": self.api_key, "photo_id": photo_id, "user_id": user_id}
        return self._make_authenticated_request("GET", path, params)

    def upload_photo(self, photo_path: str) -> requests.Response:
        """
        Uploads a photo.
        """
        path = "/upload"
        with open(photo_path, "rb") as photo:
            params = {"photo": photo}
            return self._make_authenticated_request("POST", path, params)
