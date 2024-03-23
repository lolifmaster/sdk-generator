import requests
from generated_sdk.aiproducts import AskYoDa
import dotenv
import os

dotenv.load_dotenv()


def main():
    client = AskYoDa(
        api_key=os.getenv('EDEN_AI_AUTH_TOKEN'),
    )

    # Delete all projects
    try:
        projects = client.aiproducts_aiproducts_list().json()
        for project in projects:
            response = client.aiproducts_aiproducts_delete_destroy(project['project_id'])
            print(response.text, project['project_id'])
    except requests.exceptions.RequestException as e:
        print(e.response.text)

    # Create a project
    try:
        response = client.aiproducts_aiproducts_askyoda_v2_create(
            data={
                'project_name': 'Test Project',
                'collection_name': 'Test Collection',
                'ocr_provider': 'microsoft',
                'speech_to_text_provider': 'google',
                'llm_provider': 'openai',
            }
        )
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(e.response.text)

    # Get all projects
    try:
        response = client.aiproducts_aiproducts_list()
        projects: list = response.json()
        project_id = projects[0]['project_id']
        print(project_id)
    except requests.exceptions.RequestException as e:
        print(e.response.text)
        return
    # Ask LLM
    try:
        response = client.aiproducts_aiproducts_askyoda_v2_ask_llm_create(
            project_id=project_id,
            data={
                'query': 'What is the capital of Nigeria?',
                "llm_provider": "openai",
                "llm_model": "gpt-4",
            }
        )
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(e.response.text)


if __name__ == "__main__":
    main()
