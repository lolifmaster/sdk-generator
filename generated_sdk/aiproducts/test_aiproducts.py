import unittest
from unittest.mock import patch, Mock
from aiproducts import EdenAiClient


class TestEdenAiClient(unittest.TestCase):
    def setUp(self):
        self.client = EdenAiClient("test_api_key")

    @patch("requests.request")
    def test_list_projects(self, mock_request):
        mock_request.return_value = Mock(status_code=200)
        response = self.client.list_projects("test_project_type")
        self.assertEqual(response.status_code, 200)
        mock_request.assert_called_once_with(
            "GET",
            "https://api.edenai.run/v2/aiproducts/",
            headers={"Authorization": "Bearer test_api_key"},
            params={"project_type": "test_project_type"},
        )

    @patch("requests.request")
    def test_retrieve_project(self, mock_request):
        mock_request.return_value = Mock(status_code=200)
        response = self.client.retrieve_project("test_project_id")
        self.assertEqual(response.status_code, 200)
        mock_request.assert_called_once_with(
            "GET",
            "https://api.edenai.run/v2/aiproducts/test_project_id",
            headers={"Authorization": "Bearer test_api_key"},
        )

    # Continue writing tests for the rest of the methods in a similar way


if __name__ == "__main__":
    unittest.main()
