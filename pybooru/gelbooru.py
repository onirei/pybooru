from datetime import datetime
from typing import List, NoReturn, Optional, Tuple

import httpx
import xmltodict
from pydantic import BaseModel, validator

from .booru import BaseBooru


class Gelbooru(BaseBooru):
    """

    """
    def __init__(
            self,
            api_key: Optional[str] = None,
            user_id: Optional[str] = None,
            limit: int = 100,
    ) -> NoReturn:
        super().__init__(api_key=api_key, user_id=user_id, limit=limit)
        self._api_url = f'https://gelbooru.com/index.php?page=dapi&s=post&q=index'
        self._image_schema = GelbooruImage

    async def _get_counts(
            self, client: httpx.AsyncClient = None, tags: str = ''
    ) -> Tuple[int, int]:
        url = f'{self._api_url}&json=0&limit=0&tags={tags}'
        response = await self._get_data(url=url, client=client)
        post_count = int(xmltodict.parse(response.text).get('posts').get('@count'))
        page_count = post_count // self.limit + 1
        return page_count, post_count

    def _get_url_list(self, page_count: int, tags: str = '') -> List[str]:
        url = self._api_url + '&json=1&pid={pid}' + f'&limit={self.limit}&tags={tags}'
        return list(url.format(pid=page) for page in range(page_count))


class GelbooruImage(BaseModel):
    source: Optional[str]
    directory: str
    hash: str
    height: int
    id: int
    image: str
    change: int
    owner: str
    parent_id: Optional[str]
    rating: str
    sample: int
    preview_height: int
    preview_width: int
    sample_height: int
    sample_width: int
    score: int
    tags: str
    title: str
    width: int
    file_url: str
    created_at: str
    post_locked: int

    @validator('created_at')
    def check_created_at(cls, v):
        try:
            created_at = datetime.strptime(v, '%a %b %d %H:%M:%S %z %Y')
            return created_at
        except ValueError:
            return None

    @validator('tags')
    def check_tags(cls, v):
        return v.split(' ')

    def __str__(self):
        return self.file_url

    def __repr__(self):
        return str(self.id)

    @property
    def comments(self):
        with httpx.Client() as client:
            response = client.get(
                f'https://gelbooru.com/index.php?page=dapi&s=comment&q=index&json=1&post_id={self.id}'
            )
        comments = list(
            comment for comment in xmltodict.parse(response.text).get('comments').get('comment', ())
        )
        if comments:
            return list(text.get('@body') for text in comments)
        return comments

    @property
    def thumbnail(self):
        return f'https://img3.gelbooru.com/thumbnails/{self.directory}/thumbnail_{self.hash}.jpg'
