import asyncio
from abc import ABC, abstractmethod
from functools import reduce
from operator import iconcat
from typing import List, NoReturn, Optional, Tuple

import httpx

# TODO add authorization
# TODO add proxy connection
# TODO add docstrings


class BaseBooru(ABC):
    def __init__(
            self, api_key: Optional[str] = None, user_id: Optional[str] = None, limit: int = 100
    ) -> NoReturn:
        self._api_key = api_key
        self._user_id = user_id
        self.limit = limit
        self._image_schema = None

    @abstractmethod
    async def _get_counts(
            self, client: httpx.AsyncClient = None, tags: str = ''
    ) -> Tuple[int, int]:
        """
        _get_page_count
        :param tags: search posts by tags
        :return: posts count
        """

    @abstractmethod
    def _get_url_list(self, page_count: int, tags: str = '') -> List[str]:
        """
        _get_url_list
        :param page_count:
        :param tags:
        :return:
        """

    @staticmethod
    async def _get_data(url: str, client: httpx.AsyncClient = None,) -> httpx.Response:
        response = await client.get(url) if client else httpx.get(url)
        return response

    @staticmethod
    async def _get_all_data(url_list: List[Optional[str]], client: httpx.AsyncClient) -> List:
        responses = await asyncio.gather(*[client.get(url) for url in url_list])
        return list(responses)

    @staticmethod
    def _join_responses(responses: List[httpx.Response]) -> List[Optional[dict]]:
        gelbooru_200_pages_limit = 'Too deep! Pull it back some. Holy fuck.'
        responses = list(
            filter(
                lambda x: x.text and x.status_code == 200 and x.text != gelbooru_200_pages_limit,
                responses
            )
        )
        data = reduce(iconcat, [response.json() for response in responses if response.text], [])
        return data

    async def _get_all_json(self, tags: str = '') -> List[Optional[dict]]:
        async with httpx.AsyncClient() as client:
            page_count, *_ = await self._get_counts(tags=tags, client=client)
            url_list = self._get_url_list(page_count=page_count, tags=tags)
            responses = await self._get_all_data(url_list=url_list, client=client)
        data = self._join_responses(responses=responses)
        return data

    async def _get_page_json(self, page: int, tags: str = '') -> List[Optional[dict]]:
        url = self._get_url_list(page_count=page, tags=tags)
        url = url[-1]
        responses = await self._get_data(url=url)
        data = responses.json()
        return data

    def get_posts(
            self, tags: str = '', page: int = None, json: bool = False
    ) -> List[Optional[object]]:
        if not self._image_schema:
            return []
        if page:
            data = asyncio.run(self._get_page_json(tags=tags, page=page))
        else:
            data = asyncio.run(self._get_all_json(tags=tags))
        if json:
            return data
        return list(self._image_schema(**image) for image in data)

    def count_facets(self, tags: str = '') -> dict:
        page_count, post_count = asyncio.run(self._get_counts(tags=tags))
        return {'pages': page_count, 'posts': post_count}
