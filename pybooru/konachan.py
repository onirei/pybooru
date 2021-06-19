from typing import List, NoReturn, Optional, Tuple

import httpx
import xmltodict
from pydantic import BaseModel

from .booru import BaseBooru


class Konachan(BaseBooru):
    def __init__(
            self,
            api_key: Optional[str] = None,
            user_id: Optional[str] = None,
            limit: int = 100,
    ) -> NoReturn:
        super().__init__(api_key=api_key, user_id=user_id, limit=limit)
        self._api_url = 'https://konachan.net/post.json?'
        self._api_url_count = 'https://konachan.net/post.xml?limit=1'
        self._image_schema = KonachanImage

    async def _get_counts(
            self, client: httpx.AsyncClient = None, tags: str = ''
    ) -> Tuple[int, int]:
        url = f'{self._api_url_count}&tags={tags}'
        response = await self._get_data(url=url, client=client)
        post_count = int(xmltodict.parse(response.text).get('posts').get('@count'))
        page_count = post_count // self.limit + 1
        return page_count, post_count

    def _get_url_list(self, page_count: int, tags: str = '') -> List[str]:
        url = self._api_url + 'page={page}' + f'&limit={self.limit}&tags={tags}'
        return list(url.format(page=page) for page in range(1, page_count + 1))


class KonachanImage(BaseModel):
    id: int
    tags: str
    created_at: int
    creator_id: int
    author: str
    change: int
    source: str
    score: int
    md5: str
    file_size: int
    file_url: str
    is_shown_in_index: bool
    preview_url: str
    preview_width: int
    preview_height: int
    actual_preview_width: int
    actual_preview_height: int
    sample_url: str
    sample_width: int
    sample_height: int
    sample_file_size: int
    jpeg_url: str
    jpeg_width: int
    jpeg_height: int
    jpeg_file_size: int
    rating: str
    has_children: bool
    parent_id: Optional[int]
    status: str
    width: int
    height: int
    is_held: bool
    frames_pending_string: str
    frames_pending: List
    frames_string: str
    frames: List
