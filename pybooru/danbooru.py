from datetime import datetime
from typing import List, NoReturn, Optional, Tuple

import httpx
from pydantic import BaseModel, validator

from .booru import BaseBooru


class Danbooru(BaseBooru):
    """
    Danbooru
    """
    def __init__(
            self,
            api_key: Optional[str] = None,
            user_id: Optional[str] = None,
            limit: int = 100,
    ) -> NoReturn:
        super().__init__(api_key=api_key, user_id=user_id, limit=limit)
        self._api_url = 'https://danbooru.donmai.us/posts.json?'
        self._api_url_count = 'https://danbooru.donmai.us/counts/posts.json?tags='
        self._image_schema = DanbooruImage

    async def _get_counts(
            self, client: httpx.AsyncClient = None, tags: str = ''
    ) -> Tuple[int, int]:
        url = self._api_url_count + tags
        response = await self._get_data(url=url, client=client)
        post_count = int(response.json()['counts']['posts'])
        page_count = post_count // self.limit + 1
        return page_count, post_count

    def _get_url_list(self, page_count: int, tags: str = '') -> List[str]:
        url = self._api_url + 'page={page}' + f'&limit={self.limit}&tags={tags}'
        return list(url.format(page=page) for page in range(1, page_count + 1))


class DanbooruImage(BaseModel):
    id: int = 0
    created_at: datetime
    uploader_id: int
    score: int
    source: str
    md5: Optional[str]
    last_comment_bumped_at: Optional[datetime]
    rating: str
    image_width: int
    image_height: int
    tag_string: str
    is_note_locked: bool
    fav_count: int
    file_ext: Optional[str]
    last_noted_at: Optional[datetime]
    is_rating_locked: bool
    parent_id: Optional[int]
    has_children: bool
    approver_id: Optional[int]
    tag_count_general: int
    tag_count_artist: int
    tag_count_character: int
    tag_count_copyright: int
    file_size: int
    is_status_locked: bool
    pool_string: str
    up_score: int
    down_score: int
    is_pending: bool
    is_flagged: bool
    is_deleted: bool
    tag_count: int
    updated_at: datetime
    is_banned: bool
    pixiv_id: Optional[int]
    last_commented_at: Optional[datetime]
    has_active_children: bool
    bit_flags: int
    tag_count_meta: int
    has_large: Optional[bool]
    has_visible_children: bool
    tag_string_general: str
    tag_string_character: str
    tag_string_copyright: str
    tag_string_artist: str
    tag_string_meta: str
    file_url: Optional[str]
    large_file_url: Optional[str]
    preview_file_url: Optional[str]

    def __str__(self):
        return self.file_url

    def __repr__(self):
        return str(self.id)

    @validator(
        'tag_string_general',
        'tag_string_character',
        'tag_string_copyright',
        'tag_string_artist',
        'tag_string_meta',
    )
    def check_tags(cls, v):
        return v.split(' ')

    @property
    def get_comments(self):
        return None
