import requests
from typing import Optional, Literal, TypedDict, List, Dict, Any, NotRequired


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
    data_type: str
    file: str
    metadata: NotRequired[str]
    provider: NotRequired[str]


class AddTextRequest(TypedDict):
    texts: List[str]
    metadata: NotRequired[List[Dict[str, Any]]]


class AddUrlRequest(TypedDict):
    urls: List[str]
    metadata: NotRequired[List[Dict[str, Any]]]


class AskLLMRequest(TypedDict):
    query: str
    llm_provider: str
    llm_model: str
    k: NotRequired[int]
    history: NotRequired[List[Dict[str, Any]]]
    personality: NotRequired[Dict[str, Any]]
    filter_documents: NotRequired[Dict[str, Any]]
    temperature: NotRequired[float]
    max_tokens: NotRequired[int]


class PatchedAskYodaProjectUpdateRequest(TypedDict):
    llm_provider: str
    llm_model: str


class UniversalTranslatorCreatetRequest(TypedDict):
    source_language: NotRequired[str]
    target_language: NotRequired[str]
    project_name: str
    fall_back_providers: NotRequired[List[str]]
    provider: str


class PatchedUniversalTranslatorCreatetRequest(TypedDict):
    source_language: NotRequired[str]
    target_language: NotRequired[str]
    project_name: str
    fall_back_providers: NotRequired[List[str]]
    provider: str


class UniversalTranslatorCallRequest(TypedDict):
    text: str
    source_language: NotRequired[str]
    target_language: str


class DocParserCreateRequest(TypedDict):
    project_name: str
    structure_providers: Dict[str, Any]
    subfeature: str


class PatchedDocParserUpdateRequest(TypedDict):
    structure_providers: Dict[str, Any]


class DocParserCallParametersRequest(TypedDict):
    file: str
    file_url: NotRequired[str]
    language: NotRequired[str]


class AskYoDa:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.edenai.run/v2"

    def _make_request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def _make_authenticated_request(self, method: str, endpoint: str, **kwargs):
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        kwargs["headers"] = headers
        return self._make_request(method, endpoint, **kwargs)

    def aiproducts_aiproducts_list(self, project_type: Optional[str] = None):
        return self._make_authenticated_request("GET", "/aiproducts/", params={"project_type": project_type})

    def aiproducts_aiproducts_retrieve(self, project_id: str):
        return self._make_authenticated_request("GET", f"/aiproducts/{project_id}")

    def aiproducts_aiproducts_askyoda_v2_create(self, data: AskYourDataProjectRequest):
        return self._make_authenticated_request("POST", "/aiproducts/askyoda/v2/", json=data)

    def aiproducts_aiproducts_askyoda_v2_add_file_create(self, project_id: str, data: AddFileRequest):
        return self._make_authenticated_request("POST", f"/aiproducts/askyoda/v2/{project_id}/add_file", json=data)

    def aiproducts_aiproducts_askyoda_v2_add_text_create(self, project_id: str, data: AddTextRequest):
        return self._make_authenticated_request("POST", f"/aiproducts/askyoda/v2/{project_id}/add_text", json=data)

    def aiproducts_aiproducts_askyoda_v2_add_url_create(self, project_id: str, data: AddUrlRequest):
        return self._make_authenticated_request("POST", f"/aiproducts/askyoda/v2/{project_id}/add_url", json=data)

    def aiproducts_aiproducts_askyoda_v2_ask_llm_create(self, project_id: str, data: AskLLMRequest):
        return self._make_authenticated_request("POST", f"/aiproducts/askyoda/v2/{project_id}/ask_llm", json=data)

    def aiproducts_aiproducts_askyoda_v2_delete_chunk_destroy(self, project_id: str, id: str):
        return self._make_authenticated_request("DELETE", f"/aiproducts/askyoda/v2/{project_id}/delete_chunk",
                                                params={"id": id})

    def aiproducts_aiproducts_askyoda_v2_info_retrieve(self, project_id: str):
        return self._make_authenticated_request("GET", f"/aiproducts/askyoda/v2/{project_id}/info")

    def aiproducts_aiproducts_askyoda_v2_query_create(self, project_id: str, data: AskLLMRequest):
        return self._make_authenticated_request("POST", f"/aiproducts/askyoda/v2/{project_id}/query", json=data)

    def aiproducts_aiproducts_askyoda_v2_update_project_partial_update(self, project_id: str,
                                                                       data: PatchedAskYodaProjectUpdateRequest):
        return self._make_authenticated_request("PATCH", f"/aiproducts/askyoda/v2/{project_id}/update_project",
                                                json=data)

    def aiproducts_aiproducts_delete_destroy(self, project_id: str):
        return self._make_authenticated_request("DELETE", f"/aiproducts/delete/{project_id}")

    def aiproducts_aiproducts_translathor_create(self, data: UniversalTranslatorCreatetRequest):
        return self._make_authenticated_request("POST", "/aiproducts/translathor/", json=data)

    def aiproducts_aiproducts_translathor_retrieve(self, project_id: str, source_lang: str, target_lang: str):
        return self._make_authenticated_request("GET", f"/aiproducts/translathor/{project_id}",
                                                params={"source_lang": source_lang, "target_lang": target_lang})

    def aiproducts_aiproducts_translathor_partial_update(self, project_id: str, source_lang: str, target_lang: str,
                                                         data: PatchedUniversalTranslatorCreatetRequest):
        return self._make_authenticated_request("PATCH", f"/aiproducts/translathor/{project_id}",
                                                params={"source_lang": source_lang, "target_lang": target_lang},
                                                json=data)

    def aiproducts_aiproducts_translathor_destroy(self, project_id: str, source_lang: str, target_lang: str):
        return self._make_authenticated_request("DELETE", f"/aiproducts/translathor/{project_id}",
                                                params={"source_lang": source_lang, "target_lang": target_lang})

    def aiproducts_aiproducts_translathor_translate_create_2(self, project_id: str,
                                                             data: UniversalTranslatorCallRequest):
        return self._make_authenticated_request("POST", f"/aiproducts/translathor/{project_id}/translate", json=data)

    def aiproducts_aiproducts_x_merge_doc_parser_create(self, data: DocParserCreateRequest):
        return self._make_authenticated_request("POST", "/aiproducts/x_merge/doc_parser/", json=data)

    def aiproducts_aiproducts_x_merge_doc_parser_partial_update(self, project_id: str,
                                                                data: PatchedDocParserUpdateRequest):
        return self._make_authenticated_request("PATCH", f"/aiproducts/x_merge/doc_parser/{project_id}", json=data)

    def aiproducts_aiproducts_x_merge_doc_parser_launch_call_create(self, project_id: str,
                                                                    data: DocParserCallParametersRequest):
        return self._make_authenticated_request("POST", f"/aiproducts/x_merge/doc_parser/{project_id}/launch_call",
                                                json=data)
