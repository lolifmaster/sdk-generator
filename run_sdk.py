from generated_sdk.aiproducts import AskYoDa
import dotenv
import os

dotenv.load_dotenv()


def main():
    client = AskYoDa(
        api_key=os.getenv('EDEN_AI_AUTH_TOKEN'),
    )

    try:
        client.create_project(data={
            'project_name': 'AskYoDa',
            'collection_name': 'doc_parser',
            'ocr_provider': 'microsoft',
            'speech_to_text_provider': 'openai',
        })
    except Exception as e:
        print(e)

    res = client.list_projects(project_type='doc_parser')
    print(res)


if __name__ == "__main__":
    main()
