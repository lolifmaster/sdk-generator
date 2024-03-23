import requests
from generated_sdk.aiproducts import AskYoDa
import dotenv
import os
from pprint import pprint

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
            pprint(response.text)
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)

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
        pprint(response.text)
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)

    # Get all projects
    try:
        response = client.aiproducts_aiproducts_list()
        projects: list = response.json()
        project_id = projects[0]['project_id']
        pprint(project_id)
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)
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
        pprint(response.text)
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)

    # Project info retrieval
    try:
        response = client.aiproducts_aiproducts_askyoda_v2_info_retrieve(project_id)
        pprint(response.text)
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)

    # Update project
    try:
        response = client.aiproducts_aiproducts_askyoda_v2_update_project_partial_update(
            project_id=project_id,
            data={
                'ocr_provider': 'google',
                'speech_to_text_provider': 'google',
                'llm_provider': 'meta',
                'llm_model': 'llama2-13b-chat-v1',
            }
        )
        pprint(response.text)
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)

    # Create a translation project
    try:
        client.aiproducts_aiproducts_translathor_create(
            data={
                'project_name': 'Test translation Project',
                'provider': 'openai',
                'source_language': 'en',
                'target_language': 'fr',
            }
        )
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)
        return

    # Get all translation projects
    try:
        response = client.aiproducts_aiproducts_translathor_list()
        projects: list = response.json()
        if projects:
            project_id = projects[0]['project_id']
        else:
            raise Exception('No translation projects found')
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)
        return

    # translate
    try:
        response = client.aiproducts_aiproducts_translathor_translate_create_2(
            project_id=project_id,
            data={
                'text': 'Hello, how are you?',
                'source_language': 'en',
                'target_language': 'fr',
            }
        )
        pprint(response.json())
    except requests.exceptions.RequestException as e:
        pprint(e.response.text)


if __name__ == "__main__":
    main()
