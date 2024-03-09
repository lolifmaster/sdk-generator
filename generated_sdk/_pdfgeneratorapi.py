import requests


class DocumentsClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def _make_request(self, method, path, params=None, data=None):
        url = self.base_url + path
        response = requests.request(method, url, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def _make_authenticated_request(self, method, path, params=None, data=None):
        headers = {"Authorization": "Bearer " + self.api_key}
        url = self.base_url + path
        response = requests.request(
            method, url, params=params, json=data, headers=headers
        )
        response.raise_for_status()
        return response.json()

    def merge_templates(self, name, format="pdf", output="base64", data=None):
        path = "/templates/output"
        params = {"name": name, "format": format, "output": output}
        return self._make_authenticated_request("POST", path, params=params, data=data)

    def merge_template(
        self, template_id, name, format="pdf", output="base64", data=None
    ):
        path = f"/templates/{template_id}/output"
        params = {"name": name, "format": format, "output": output}
        return self._make_authenticated_request("POST", path, params=params, data=data)

    def get_templates(self):
        path = "/templates"
        return self._make_authenticated_request("GET", path)

    def create_template(self, data):
        path = "/templates"
        return self._make_authenticated_request("POST", path, data=data)

    def delete_template(self, template_id):
        path = f"/templates/{template_id}"
        return self._make_authenticated_request("DELETE", path)

    def get_template(self, template_id):
        path = f"/templates/{template_id}"
        return self._make_authenticated_request("GET", path)

    def update_template(self, template_id, data):
        path = f"/templates/{template_id}"
        return self._make_authenticated_request("PUT", path, data=data)

    def copy_template(self, template_id, name=None):
        path = f"/templates/{template_id}/copy"
        params = {"name": name} if name else None
        return self._make_authenticated_request("POST", path, params=params)

    def get_editor_url(self, template_id, language=None, data=None):
        path = f"/templates/{template_id}/editor"
        params = {"language": language} if language else None
        return self._make_authenticated_request("POST", path, params=params, data=data)

    def delete_workspace(self, workspace_id):
        path = f"/workspaces/{workspace_id}"
        return self._make_authenticated_request("DELETE", path)

    def get_workspace(self, workspace_id):
        path = f"/workspaces/{workspace_id}"
        return self._make_authenticated_request("GET", path)


client = DocumentsClient("https://api.example.com", "your-api-key")
templates = client.get_templates()
