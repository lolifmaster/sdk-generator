from typing import TypedDict, List, Optional


class ApiKey(TypedDict):
    apiKey: str


class RefreshToken(TypedDict):
    refreshToken: str


class CurrentPage(TypedDict, total=False):
    currentPage: int


class PageSize(TypedDict, total=False):
    pageSize: int


class Metadata(TypedDict):
    key: str
    value: str


class VideoClip(TypedDict):
    startTimecode: str
    endTimecode: str


class VideoWatermark(TypedDict):
    id: str
    top: str
    left: str
    bottom: str
    right: str
    width: str
    height: str
    opacity: str


class VideoCreationPayload(TypedDict):
    tags: List[str]
    title: str
    source: str
    public: bool
    panoramic: bool
    mp4Support: bool
    playerId: str
    metadata: List[Metadata]
    clip: VideoClip
    watermark: VideoWatermark


class ThumbnailPickPayload(TypedDict):
    timecode: str


class VideoUpdatePayload(TypedDict):
    tags: List[str]
    title: str
    playerId: Optional[str]
    public: bool
    panoramic: bool
    mp4Support: bool
    metadata: List[Metadata]


class TokenCreationPayload(TypedDict):
    ttl: int


class RestreamsRequestObject(TypedDict):
    name: str
    serverUrl: str
    streamKey: str


class LiveStreamCreationPayload(TypedDict):
    name: str
    public: bool
    playerId: str
    restreams: List[RestreamsRequestObject]


class LiveStreamUpdatePayload(TypedDict):
    name: str
    public: bool
    playerId: str
    restreams: List[RestreamsRequestObject]


class PlayerThemeCreationPayload(TypedDict):
    name: str
    text: str
    link: str
    linkHover: str
    linkActive: str
    trackPlayed: str
    trackUnplayed: str
    trackBackground: str
    backgroundTop: str
    backgroundBottom: str
    backgroundText: str
    enableApi: bool
    enableControls: bool
    forceAutoplay: bool
    hideTitle: bool
    forceLoop: bool


class PlayerThemeUpdatePayload(TypedDict):
    name: str
    text: str
    link: str
    linkHover: str
    linkActive: str
    trackPlayed: str
    trackUnplayed: str
    trackBackground: str
    backgroundTop: str
    backgroundBottom: str
    backgroundText: str
    enableApi: bool
    enableControls: bool
    forceAutoplay: bool
    hideTitle: bool
    forceLoop: bool


class WebhooksCreationPayload(TypedDict):
    events: List[str]
    url: str
