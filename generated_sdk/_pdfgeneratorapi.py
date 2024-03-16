import requests
from typing import Optional, Literal, TypedDict


class DocumentAPI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def _make_request(self, method: str, endpoint: str, params: dict = None, data: dict = None):
        url = self.base_url + endpoint
        response = requests.request(method, url, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def _make_authenticated_request(self, method: str, endpoint: str, params: dict = None, data: dict = None):
        headers = {'Authorization': 'Bearer ' + self.api_key}
        url = self.base_url + endpoint
        response = requests.request(method, url, params=params, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def merge_templates(self, doc_name: str, name: str, format: Literal['pdf', 'html', 'zip', 'xlsx'],
                        output: Literal['base64', 'url']):
        endpoint = '/templates/output'
        params = {'doc_name': doc_name, 'name': name, 'format': format, 'output': output}
        return self._make_authenticated_request('POST', endpoint, params=params)

    def merge_template(self, templateId: int, doc_name: str, name: str, format: Literal['pdf', 'html', 'zip', 'xlsx'],
                       output: Literal['base64', 'url']):
        endpoint = f'/templates/{templateId}/output'
        params = {'doc_name': doc_name, 'name': name, 'format': format, 'output': output}
        return self._make_authenticated_request('POST', endpoint, params=params)

    def get_templates(self):
        endpoint = '/templates'
        return self._make_authenticated_request('GET', endpoint)

    def create_template(self, template_definition_new: dict):
        endpoint = '/templates'
        return self._make_authenticated_request('POST', endpoint, data=template_definition_new)

    def delete_template(self, templateId: int):
        endpoint = f'/templates/{templateId}'
        return self._make_authenticated_request('DELETE', endpoint)

    def get_template(self, templateId: int):
        endpoint = f'/templates/{templateId}'
        return self._make_authenticated_request('GET', endpoint)

    def update_template(self, templateId: int, template_definition_new: dict):
        endpoint = f'/templates/{templateId}'
        return self._make_authenticated_request('PUT', endpoint, data=template_definition_new)

    def copy_template(self, templateId: int, name: Optional[str] = None):
        endpoint = f'/templates/{templateId}/copy'
        params = {'name': name} if name else None
        return self._make_authenticated_request('POST', endpoint, params=params)

    def get_editor_url(self, templateId: int, language: Optional[Literal['en', 'et', 'cs', 'sk', 'ru']] = None):
        endpoint = f'/templates/{templateId}/editor'
        params = {'language': language} if language else None
        return self._make_authenticated_request('GET', endpoint, params=params)

    def delete_workspace(self, workspaceId: str):
        endpoint = f'/workspaces/{workspaceId}'
        return self._make_authenticated_request('DELETE', endpoint)

    def get_workspace(self, workspaceId: str):
        endpoint = f'/workspaces/{workspaceId}'
        return self._make_authenticated_request('GET', endpoint)
