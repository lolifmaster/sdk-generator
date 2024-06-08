from typing import TypedDict, Optional, Literal, List


class Article(TypedDict, total=False):
    tags: str
    title: str
    body_markdown: str
    published: bool
    series: Optional[str]
    main_image: Optional[str]
    canonical_url: Optional[str]
    organization_id: Optional[int]


class PageParam(TypedDict, total=False):
    page: int


class PerPageParam30to1000(TypedDict, total=False):
    per_page: int


class SegmentUserIds(TypedDict):
    user_ids: List[int]


PlacementArea = Literal[
    "sidebar_left",
    "sidebar_left_2",
    "sidebar_right",
    "feed_first",
    "feed_second",
    "feed_third",
    "home_hero",
    "post_sidebar",
    "post_comments",
]
AudienceSegmentType = Literal[
    "manual",
    "trusted",
    "posted",
    "no_posts_yet",
    "dark_theme",
    "light_theme",
    "no_experience",
    "experience1",
    "experience2",
    "experience3",
    "experience4",
    "experience5",
]
DisplayTo = Literal["all", "logged_in", "logged_out"]
TypeOf = Literal["in_house", "community", "external"]


class Billboard(TypedDict, total=False):
    id: int
    name: str
    body_markdown: str
    approved: bool
    published: bool
    organization_id: Optional[int]
    creator_id: Optional[int]
    placement_area: PlacementArea
    tag_list: str
    exclude_article_ids: Optional[str]
    audience_segment_id: int
    audience_segment_type: AudienceSegmentType
    target_geolocations: List[str]
    display_to: DisplayTo
    type_of: TypeOf


class BillboardsCreateNewBillboardRequest(TypedDict):
    Billboard: Billboard


class BillboardsUpdateByIdRequest(TypedDict):
    Billboard: Billboard


class PerPageParam10to1000(TypedDict, total=False):
    per_page: int


class Organization(TypedDict, total=False):
    summary: str
    type_of: str
    username: str
    name: str
    twitter_username: str
    github_username: str
    url: str
    location: str
    joined_at: str
    tech_stack: str
    tag_line: Optional[str]
    story: Optional[str]


Template = Literal["contained", "full_within_layout", "nav_bar_included", "json"]


class PagesCreateNewPageRequest(TypedDict, total=False):
    title: str
    slug: str
    body_markdown: str
    body_json: str
    is_top_level_path: bool
    template: Template


class Page(TypedDict, total=False):
    title: str
    slug: str
    body_markdown: Optional[str]
    body_json: Optional[str]
    is_top_level_path: bool
    social_image: Optional[dict]
    template: Template


class UserInviteParam(TypedDict, total=False):
    email: str
    name: Optional[str]


class PerPageParam24to1000(TypedDict, total=False):
    per_page: int
