import requests


class DocumentServiceSDK:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def merge_templates(self, docname, format="pdf", output="base64", batch_data=None):
        path = "/templates/output"
        params = {"name": docname, "format": format, "output": output}
        return self._make_request("POST", path, params=params, json=batch_data)

    def merge_template(self, template_id, docname, format="pdf", output="base64", data=None):
        path = f"/templates/{template_id}/output"
        params = {"name": docname, "format": format, "output": output}
        return self._make_request("POST", path, params=params, json=data)

    def get_templates(self):
        path = "/templates"
        return self._make_request("GET", path)

    def get_specifications(self):
        return self._make_request("GET", '')


# Example Usage
if __name__ == "__main__":
    # Instantiate the SDK with the base URL of your API
    api_base_url = "https://us1.pdfgeneratorapi.com/api/v3"
    sdk = DocumentServiceSDK(api_base_url)

    # Get the specification
    try:
        spec = sdk.get_specifications()
        print(spec)
    except requests.exceptions.RequestException as e:
        print(e)
