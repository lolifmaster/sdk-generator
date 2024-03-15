import requests


class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _make_request(self, method, endpoint, params=None, data=None):
        url = self.base_url + endpoint
        response = requests.request(method, url, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def _make_authenticated_request(self, method, endpoint, params=None, data=None):
        url = self.base_url + endpoint
        response = requests.request(
            method, url, headers=self.headers, params=params, json=data
        )
        response.raise_for_status()
        return response.json()

    def merge_templates(self, name, format, output):
        endpoint = "/templates/output"
        params = {"name": name, "format": format, "output": output}
        return self._make_authenticated_request("POST", endpoint, params=params)

    def merge_template(self, template_id, name, format, output):
        endpoint = f"/templates/{template_id}/output"
        params = {"name": name, "format": format, "output": output}
        return self._make_authenticated_request("POST", endpoint, params=params)

    def get_templates(self):
        endpoint = "/templates"
        return self._make_authenticated_request("GET", endpoint)

    def create_template(self, template_definition):
        endpoint = "/templates"
        return self._make_authenticated_request(
            "POST", endpoint, data=template_definition
        )

    def delete_template(self, template_id):
        endpoint = f"/templates/{template_id}"
        return self._make_authenticated_request("DELETE", endpoint)

    def get_template(self, template_id):
        endpoint = f"/templates/{template_id}"
        return self._make_authenticated_request("GET", endpoint)

    def update_template(self, template_id, template_definition):
        endpoint = f"/templates/{template_id}"
        return self._make_authenticated_request(
            "PUT", endpoint, data=template_definition
        )

    def copy_template(self, template_id, name=None):
        endpoint = f"/templates/{template_id}/copy"
        params = {"name": name} if name else None
        return self._make_authenticated_request("POST", endpoint, params=params)

    def get_editor_url(self, template_id, language=None):
        endpoint = f"/templates/{template_id}/editor"
        params = {"language": language} if language else None
        return self._make_authenticated_request("GET", endpoint, params=params)

    def delete_workspace(self, workspace_id):
        endpoint = f"/workspaces/{workspace_id}"
        return self._make_authenticated_request("DELETE", endpoint)

    def get_workspace(self, workspace_id):
        endpoint = f"/workspaces/{workspace_id}"
        return self._make_authenticated_request("GET", endpoint)
