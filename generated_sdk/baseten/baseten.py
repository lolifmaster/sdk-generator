import requests
from types import *

class BaseTenClient:
    def __init__(self, api_key: str):
        self.base_url = "https://api.baseten.co"
        self.api_key = api_key

    def _make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"ApiKey {self.api_key}"
        kwargs["headers"] = headers
        return requests.request(method, url, **kwargs)

    def get_all_secrets(self) -> requests.Response:
        """Retrieve all secrets."""
        url = f"{self.base_url}/v1/secrets"
        return self._make_authenticated_request("GET", url)

    def upsert_new_secret(self, secret: UpsertSecretRequestV1) -> requests.Response:
        """Upsert a new secret."""
        url = f"{self.base_url}/v1/secrets"
        return self._make_authenticated_request("POST", url, json=secret)

    def get_all_models(self) -> requests.Response:
        """Retrieve all models."""
        url = f"{self.base_url}/v1/models"
        return self._make_authenticated_request("GET", url)

    def get_model_by_id(self, model_id: ModelId) -> requests.Response:
        """Retrieve a model by its ID."""
        url = f"{self.base_url}/v1/models/{model_id['name']}"
        return self._make_authenticated_request("GET", url)

    def get_all_deployments(self, model_id: ModelId) -> requests.Response:
        """Retrieve all deployments for a model."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments"
        return self._make_authenticated_request("GET", url)

    def get_development_details(self, model_id: ModelId) -> requests.Response:
        """Retrieve development deployment details for a model."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/development"
        return self._make_authenticated_request("GET", url)

    def get_production_details(self, model_id: ModelId) -> requests.Response:
        """Retrieve production deployment details for a model."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/production"
        return self._make_authenticated_request("GET", url)

    def get_deployment_details(self, model_id: ModelId, deployment_id: DeploymentId) -> requests.Response:
        """Retrieve deployment details for a specific deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/{deployment_id['name']}"
        return self._make_authenticated_request("GET", url)

    def update_development_autoscaling_settings(self, model_id: ModelId, settings: UpdateAutoscalingSettingsV1) -> requests.Response:
        """Update autoscaling settings for the development deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/development/autoscaling_settings"
        return self._make_authenticated_request("PATCH", url, json=settings)

    def update_production_autoscaling_settings(self, model_id: ModelId, settings: UpdateAutoscalingSettingsV1) -> requests.Response:
        """Update autoscaling settings for the production deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/production/autoscaling_settings"
        return self._make_authenticated_request("PATCH", url, json=settings)

    def update_deployment_autoscaling_settings(self, model_id: ModelId, deployment_id: DeploymentId, settings: UpdateAutoscalingSettingsV1) -> requests.Response:
        """Update autoscaling settings for a specific deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/{deployment_id['name']}/autoscaling_settings"
        return self._make_authenticated_request("PATCH", url, json=settings)

    def promote_development(self, model_id: ModelId, promote_request: PromoteRequestV1) -> requests.Response:
        """Promote the development deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/development/promote"
        return self._make_authenticated_request("POST", url, json=promote_request)

    def promote_deployment(self, model_id: ModelId, deployment_id: DeploymentId, promote_request: PromoteRequestV1) -> requests.Response:
        """Promote a specific deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/{deployment_id['name']}/promote"
        return self._make_authenticated_request("POST", url, json=promote_request)

    def activate_development_deployment(self, model_id: ModelId) -> requests.Response:
        """Activate the development deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/development/activate"
        return self._make_authenticated_request("POST", url)

    def activate_production(self, model_id: ModelId) -> requests.Response:
        """Activate the production deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/production/activate"
        return self._make_authenticated_request("POST", url)

    def activate_deployment_status(self, model_id: ModelId, deployment_id: DeploymentId) -> requests.Response:
        """Activate a specific deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/{deployment_id['name']}/activate"
        return self._make_authenticated_request("POST", url)

    def deactivate_development(self, model_id: ModelId) -> requests.Response:
        """Deactivate the development deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/development/deactivate"
        return self._make_authenticated_request("POST", url)

    def deactivate_production_deployment(self, model_id: ModelId) -> requests.Response:
        """Deactivate the production deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/production/deactivate"
        return self._make_authenticated_request("POST", url)

    def deactivate_deployment_status(self, model_id: ModelId, deployment_id: DeploymentId) -> requests.Response:
        """Deactivate a specific deployment."""
        url = f"{self.base_url}/v1/models/{model_id['name']}/deployments/{deployment_id['name']}/deactivate"
        return self._make_authenticated_request("POST", url)