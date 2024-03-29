from working_sdks.aiproducts import AskYoDa
import dotenv
import os
from pprint import pprint

dotenv.load_dotenv()


def main():
    client = AskYoDa(
        api_key=os.getenv("EDEN_AI_AUTH_TOKEN"),
    )

    # Delete all projects

    projects = client.list_projects().json()
    for project in projects:
        response = client.delete_project(project["project_id"])
        pprint(response.text)

    # Create a project

    response = client.create_project(
        data={
            "project_name": "Test Project",
            "collection_name": "Test Collection",
            "ocr_provider": "microsoft",
            "speech_to_text_provider": "google",
            "llm_provider": "openai",
        }
    )
    pprint(response.text)

    # Get all projects

    response = client.list_projects()
    projects: list = response.json()
    project_id = projects[0]["project_id"]
    pprint(project_id)

    # Ask LLM

    response = client.ask_llm(
        project_id=project_id,
        data={
            "query": "What is the capital of Nigeria?",
            "llm_provider": "openai",
            "llm_model": "gpt-4",
        },
    )
    pprint(response.text)

    # Project info retrieval

    response = client.get_info(project_id)
    pprint(response.text)

    # Update project

    response = client.update_project(
        project_id=project_id,
        data={
            "ocr_provider": "google",
            "speech_to_text_provider": "google",
            "llm_provider": "meta",
            "llm_model": "llama2-13b-chat-v1",
        },
    )
    pprint(response.text)

    # Create a translation project

    client.create_language_provider_pair(
        data={
            "project_name": "Test translation Project",
            "provider": "openai",
            "source_language": "en",
            "target_language": "fr",
        }
    )

    # Get all translation projects

    response = client.list_projects()
    projects: list = response.json()
    if projects:
        project_id = projects[0]["project_id"]
    else:
        raise Exception("No translation projects found")

    # translate

    response = client.translate(
        project_id=project_id,
        data={
            "text": "Hello, how are you?",
            "source_language": "en",
            "target_language": "fr",
        },
    )
    pprint(response.json())


if __name__ == "__main__":
    main()
