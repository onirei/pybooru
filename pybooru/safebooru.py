from typing import List, NoReturn, Optional, Tuple

import httpx
import xmltodict
from pydantic import BaseModel

from .booru import BaseBooru


class Safebooru(BaseBooru):
    def __init__(
            self,
            api_key: Optional[str] = None,
            user_id: Optional[str] = None,
            page: str = 'dapi',
            s: str = 'post',
            q: str = 'index',
            limit: int = 100,
    ) -> NoReturn:
        super().__init__(api_key=api_key, user_id=user_id, limit=limit)
        self._api_url = f'https://safebooru.org/index.php?page={page}&s={s}&q={q}'
        self._image_schema = SafebooruImage

    async def _get_counts(
            self, client: httpx.AsyncClient = None, tags: str = ''
    ) -> Tuple[int, int]:
        url = f'{self._api_url}&json=0&pid=0&limit=0&tags={tags}'
        response = await self._get_data(url=url, client=client)
        post_count = int(xmltodict.parse(response.text).get('posts').get('@count'))
        page_count = post_count // self.limit + 1
        return page_count, post_count

    def _get_url_list(self, page_count: int, tags: str = '') -> List[str]:
        url = self._api_url + '&json=1&pid={pid}' + f'&limit={self.limit}&tags={tags}'
        return list(url.format(pid=page) for page in range(page_count))


class SafebooruImage(BaseModel):
    directory: str
    hash: str
    height: int
    id: int
    image: str
    change: int
    owner: str
    parent_id: int
    rating: str
    sample: bool
    sample_height: int
    sample_width: int
    score: Optional[int]
    tags: str
    width: int
