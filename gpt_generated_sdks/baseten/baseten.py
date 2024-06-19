import requests
from types import (
    UpsertSecretRequestV1,
    UpdateAutoscalingSettingsV1,
    PromoteRequestV1,
    PathParameter,
)


class BaseTenApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def getAllSecrets(self):
        url = f"{self.base_url}/v1/secrets"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def upsertNewSecret(self, body: UpsertSecretRequestV1):
        url = f"{self.base_url}/v1/secrets"
        response = requests.post(url, json=body.__dict__, headers=self.headers)
        return response.json()

    def getAllModels(self):
        url = f"{self.base_url}/v1/models"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def getModelById(self, model_id: PathParameter):
        url = f"{self.base_url}/v1/models/{model_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def getAllDeployments(self, model_id: PathParameter):
        url = f"{self.base_url}/v1/models/{model_id}/deployments"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def getDevelopmentDetails(self, model_id: PathParameter):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/development"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def getProductionDetails(self, model_id: PathParameter):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/production"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def getDeploymentDetails(
        self, model_id: PathParameter, deployment_id: PathParameter
    ):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/{deployment_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def updateDevelopmentSetting(
        self, model_id: PathParameter, body: UpdateAutoscalingSettingsV1
    ):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/development/autoscaling_settings"
        response = requests.patch(url, json=body.__dict__, headers=self.headers)
        return response.json()

    def updateStatus(self, model_id: PathParameter, body: UpdateAutoscalingSettingsV1):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/production/autoscaling_settings"
        response = requests.patch(url, json=body.__dict__, headers=self.headers)
        return response.json()

    def updateDeploymentSettings(
        self,
        model_id: PathParameter,
        deployment_id: PathParameter,
        body: UpdateAutoscalingSettingsV1,
    ):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/{deployment_id}/autoscaling_settings"
        response = requests.patch(url, json=body.__dict__, headers=self.headers)
        return response.json()

    def deployPromote(self, model_id: PathParameter, body: PromoteRequestV1):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/development/promote"
        response = requests.post(url, json=body.__dict__, headers=self.headers)
        return response.json()

    def deploymentPromote(
        self,
        model_id: PathParameter,
        deployment_id: PathParameter,
        body: PromoteRequestV1,
    ):
        url = (
            f"{self.base_url}/v1/models/{model_id}/deployments/{deployment_id}/promote"
        )
        response = requests.post(url, json=body.__dict__, headers=self.headers)
        return response.json()

    def activateDevelopmentDeployment(self, model_id: PathParameter):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/development/activate"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def activateProduction(self, model_id: PathParameter):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/production/activate"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def activateDeploymentStatus(
        self, model_id: PathParameter, deployment_id: PathParameter
    ):
        url = (
            f"{self.base_url}/v1/models/{model_id}/deployments/{deployment_id}/activate"
        )
        response = requests.post(url, headers=self.headers)
        return response.json()

    def deactivateDevelopment(self, model_id: PathParameter):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/development/deactivate"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def deactivateProductionDeployment(self, model_id: PathParameter):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/production/deactivate"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def deactivateDeploymentStatus(
        self, model_id: PathParameter, deployment_id: PathParameter
    ):
        url = f"{self.base_url}/v1/models/{model_id}/deployments/{deployment_id}/deactivate"
        response = requests.post(url, headers=self.headers)
        return response.json()
