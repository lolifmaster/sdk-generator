import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def merge_templates(self, docname, format='pdf', output='base64', data=None):
        url = f"{self.base_url}/mergeTemplates"
        params = {
            'name': docname,
            'format': format,
            'output': output
        }
        response = requests.post(url, params=params, json=data)
        return response.json()

    def get_templates(self):
        url = f"{self.base_url}/getTemplates"
        response = requests.get(url)
        return response.json()

    # Add more functions for other endpoints as needed


# Example usage
client = APIClient("https://api.example.com")
templates = client.get_templates()
print(templates)

# For mergeTemplates endpoint
data = {
    "BatchData": {
        "items": [
            {
                "Data": "example data"
            }
        ]
    }
}
response = client.merge_templates(docname="example_doc", data=data)
print(response)
