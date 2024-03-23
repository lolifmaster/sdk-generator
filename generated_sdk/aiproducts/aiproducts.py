import requests
from typing import Literal, TypedDict, List, NotRequired


class AskYourDataProjectRequest(TypedDict):
    credential: NotRequired[str]
    asset: NotRequired[str]
    project_name: str
    collection_name: str
    db_provider: NotRequired[Literal['qdrant', 'supabase']]
    embeddings_provider: NotRequired[str]
    llm_provider: NotRequired[str]
    llm_model: NotRequired[str]
    ocr_provider: str
    speech_to_text_provider: str


class AddFileRequest(TypedDict):
    data_type: Literal['pdf', 'audio', 'csv']
    file: str
    metadata: str
    provider: str


class AddTextRequest(TypedDict):
    texts: List[str]
    metadata: List[dict]


class AddUrlRequest(TypedDict):
    urls: List[str]
    metadata: List[dict]


class AskLLMRequest(TypedDict):
    query: str
    llm_provider: str
    llm_model: str
    k: int
    history: List[dict]
    personality: dict
    filter_documents: dict
    temperature: float
    max_tokens: int


class PatchedAskYodaProjectUpdateRequest(TypedDict):
    llm_provider: str
    llm_model: str


class UniversalTranslatorCreatetRequest(TypedDict):
    source_language: NotRequired[str]
    target_language: NotRequired[str]
    project_name: str
    fall_back_providers: List[str]
    provider: str


class PatchedUniversalTranslatorCreatetRequest(TypedDict):
    source_language: NotRequired[str]
    target_language: NotRequired[str]
    project_name: str
    fall_back_providers: List[str]
    provider: str


class UniversalTranslatorCallRequest(TypedDict):
    text: str
    source_language: NotRequired[str]
    target_language: str


class DocParserCreateRequest(TypedDict):
    project_name: str
    structure_providers: dict
    subfeature: str


class PatchedDocParserUpdateRequest(TypedDict):
    structure_providers: dict


class DocParserCallParametersRequest(TypedDict):
    file: str
    file_url: NotRequired[str]
    language: NotRequired[str]


class AskYoDa:
    def __init__(self, api_key: str):
        self.base_url = 'https://api.edenai.run/v2'
        self.api_key = api_key

    def _make_request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def _make_authenticated_request(self, method: str, endpoint: str, **kwargs):
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.api_key}'
        kwargs['headers'] = headers
        return self._make_request(method, endpoint, **kwargs)

    def list_projects(self, project_type: str = None) -> dict:
        if project_type:
            return self._make_authenticated_request('GET', f'aiproducts/?project_type={project_type}')
        return self._make_authenticated_request('GET', 'aiproducts')

    def retrieve_project(self, project_id: str) -> dict:
        return self._make_authenticated_request('GET', f'aiproducts/{project_id}')

    def create_project(self, data: AskYourDataProjectRequest) -> dict:
        return self._make_authenticated_request('POST', 'aiproducts/askyoda/v2/', json=data)

    def add_file(self, project_id: str, data: AddFileRequest) -> dict:
        return self._make_authenticated_request('POST', f'aiproducts/askyoda/v2/{project_id}/add_file', json=data)

    def add_text(self, project_id: str, data: AddTextRequest) -> dict:
        return self._make_authenticated_request('POST', f'aiproducts/askyoda/v2/{project_id}/add_text', json=data)

    def add_url(self, project_id: str, data: AddUrlRequest) -> dict:
        return self._make_authenticated_request('POST', f'aiproducts/askyoda/v2/{project_id}/add_url', json=data)

    def ask_llm(self, project_id: str, data: AskLLMRequest) -> dict:
        return self._make_authenticated_request('POST', f'aiproducts/askyoda/v2/{project_id}/ask_llm', json=data)

    def delete_chunk(self, project_id: str, id: str) -> dict:
        return self._make_authenticated_request('DELETE', f'aiproducts/askyoda/v2/{project_id}/delete_chunk?id={id}')

    def get_info(self, project_id: str) -> dict:
        return self._make_authenticated_request('GET', f'aiproducts/askyoda/v2/{project_id}/info')

    def query(self, project_id: str, data: AskLLMRequest) -> dict:
        return self._make_authenticated_request('POST', f'aiproducts/askyoda/v2/{project_id}/query', json=data)

    def update_project(self, project_id: str, data: PatchedAskYodaProjectUpdateRequest) -> dict:
        return self._make_authenticated_request('PATCH', f'aiproducts/askyoda/v2/{project_id}/update_project',
                                                json=data)

    def delete_project(self, project_id: str) -> dict:
        return self._make_authenticated_request('DELETE', f'aiproducts/delete/{project_id}')

    def create_language_provider_pair(self, data: UniversalTranslatorCreatetRequest) -> dict:
        return self._make_authenticated_request('POST', 'aiproducts/translathor/', json=data)

    def update_language(self, project_id: str, source_lang: str, target_lang: str,
                        data: PatchedUniversalTranslatorCreatetRequest) -> dict:
        return self._make_authenticated_request('PATCH',
                                                f'aiproducts/translathor/{project_id}?source_lang={source_lang}&target_lang={target_lang}',
                                                json=data)

    def delete_language(self, project_id: str, source_lang: str, target_lang: str) -> dict:
        return self._make_authenticated_request('DELETE',
                                                f'aiproducts/translathor/{project_id}?source_lang={source_lang}&target_lang={target_lang}')

    def translate(self, project_id: str, data: UniversalTranslatorCallRequest) -> dict:
        return self._make_authenticated_request('POST', f'aiproducts/translathor/{project_id}/translate', json=data)

    def create_doc_parser_project(self, data: DocParserCreateRequest) -> dict:
        return self._make_authenticated_request('POST', 'aiproducts/x_merge/doc_parser/', json=data)

    def update_doc_parser_project(self, project_id: str, data: PatchedDocParserUpdateRequest) -> dict:
        return self._make_authenticated_request('PATCH', f'aiproducts/x_merge/doc_parser/{project_id}', json=data)

    def doc_parser_launch_call(self, project_id: str, data: DocParserCallParametersRequest) -> dict:
        return self._make_authenticated_request('POST', f'aiproducts/x_merge/doc_parser/{project_id}/launch_call',
                                                json=data)
