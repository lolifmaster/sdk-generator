
import unittest
from unittest.mock import patch
from your_module import EdenAI, AskYourDataProjectRequest, AddFileRequest, AddTextRequest, AddUrlRequest, AskLLMRequest, PatchedAskYodaProjectUpdateRequest, UniversalTranslatorCreatetRequest, PatchedUniversalTranslatorCreatetRequest, UniversalTranslatorCallRequest, DocParserCreateRequest, PatchedDocParserUpdateRequest, DocParserCallParametersRequest

class TestEdenAI(unittest.TestCase):
    @patch('requests.request')
    def test_make_request(self, mock_request):
        mock_request.return_value.status_code = 200
        client = EdenAI('http://test.com', 'test_key')
        response = client._make_request('GET', '/test')
        self.assertEqual(response.status_code, 200)

    @patch('requests.request')
    def test_make_authenticated_request(self, mock_request):
        mock_request.return_value.status_code = 200
        client = EdenAI('http://test.com', 'test_key')
        response = client._make_authenticated_request('GET', '/test')
        self.assertEqual(response.status_code, 200)

    @patch('requests.request')
    def test_list_projects(self, mock_request):
        mock_request.return_value.status_code = 200
        client = EdenAI('http://test.com', 'test_key')
        response = client.list_projects()
        self.assertEqual(response.status_code, 200)

    # Continue with similar tests for each method in the EdenAI class

if __name__ == '__main__':
    unittest.main()
