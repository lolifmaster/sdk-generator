import requests


class DocumentsClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    def _make_request(self, method, path, params=None, data=None):
        url = self.base_url + path
        response = requests.request(method, url, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def _make_authenticated_request(self, method, path, params=None, data=None):
        url = self.base_url + path
        response = requests.request(method, url, params=params, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def merge_templates(self, name, format, output):
        path = '/templates/output'
        params = {'name': name, 'format': format, 'output': output}
        return self._make_authenticated_request('POST', path, params=params)

    def merge_template(self, template_id, name, format, output):
        path = f'/templates/{template_id}/output'
        params = {'name': name, 'format': format, 'output': output}
        return self._make_authenticated_request('POST', path, params=params)

    def get_templates(self):
        path = '/templates'
        return self._make_authenticated_request('GET', path)

    def create_template(self, template_definition):
        path = '/templates'
        return self._make_authenticated_request('POST', path, data=template_definition)

    def delete_template(self, template_id):
        path = f'/templates/{template_id}'
        return self._make_authenticated_request('DELETE', path)

    def get_template(self, template_id):
        path = f'/templates/{template_id}'
        return self._make_authenticated_request('GET', path)

    def update_template(self, template_id, template_definition):
        path = f'/templates/{template_id}'
        return self._make_authenticated_request('PUT', path, data=template_definition)

    def copy_template(self, template_id, name=None):
        path = f'/templates/{template_id}/copy'
        params = {'name': name} if name else None
        return self._make_authenticated_request('POST', path, params=params)

    def get_editor_url(self, template_id, language=None):
        path = f'/templates/{template_id}/editor'
        params = {'language': language} if language else None
        return self._make_authenticated_request('GET', path, params=params)

    def delete_workspace(self, workspace_id):
        path = f'/workspaces/{workspace_id}'
        return self._make_authenticated_request('DELETE', path)

    def get_workspace(self, workspace_id):
        path = f'/workspaces/{workspace_id}'
        return self._make_authenticated_request('GET', path)


client = DocumentsClient('https://us1.pdfgeneratorapi.com/api/v3',
                         'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI2ZDdiOWJhNjhmM2FjODJiZDMzOWY3N2I3ZjI0Y2U1ZjU2MzhiNDk5MmI5ZjY3ODBlZjExOWFhOWZiYzUwMDQ4Iiwic3ViIjoiY2hhcmVmMjAwMkBnbWFpbC5jb20iLCJleHAiOjE3MDk4OTk2NzZ9.8Wab2Ur269Rapue0IkYojHMo_jWB3ZJJGsDaldwjJ5A')

try:
    spec = client.get_templates()
    print(spec)
except requests.exceptions.RequestException as e:
    print(e)
