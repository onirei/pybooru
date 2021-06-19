import asyncio
import unittest
from typing import List, Tuple
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import httpx

from pybooru.booru import BaseBooru


class Booru(BaseBooru):
    async def _get_counts(
            self, client: httpx.AsyncClient = None, tags: str = ''
    ) -> Tuple[int, int]:
        pass

    def _get_url_list(self, page_count: int, tags: str = '') -> List[str]:
        pass


class BooruTestCase(unittest.TestCase):
    def setUp(self):
        self.booru = Booru(limit=10)

    @patch('httpx.AsyncClient.get')
    @patch('httpx.get')
    def test_get_data(self, mock_get, mock_async_get):
        mock_get.return_value = httpx.Response(status_code=200, text='sync')
        actual = asyncio.run(self.booru._get_data(url='test_url'))
        self.assertEqual(actual.status_code, 200)
        self.assertEqual(actual.text, 'sync')
        mock_async_get.return_value = httpx.Response(status_code=200, text='async')
        actual = asyncio.run(self.booru._get_data(url='test_url', client=httpx.AsyncClient()))
        self.assertEqual(actual.status_code, 200)
        self.assertEqual(actual.text, 'async')

    @patch('httpx.AsyncClient.get')
    def test_get_all_data(self, mock_async_get):
        mock_async_get.return_value = httpx.Response(status_code=200, text='async')
        url_list = ['test']
        actual = asyncio.run(
            self.booru._get_all_data(client=httpx.AsyncClient(), url_list=url_list)
        )
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].status_code, 200)
        self.assertEqual(actual[0].text, 'async')

    def test_join_responses(self):
        response = httpx.Response(status_code=200, text='[{"test": "test"}]')
        empty_response = httpx.Response(status_code=200, text='')
        wrong_response = httpx.Response(status_code=405, text='')
        responces = [response, empty_response, response, wrong_response]
        actual = self.booru._join_responses(responses=responces)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual, [{'test': 'test'}, {'test': 'test'}])

    # def test_get_all_json(self):
    #     response_text = '[{"test": "test"},{"test": "test"}]'
    #     response = httpx.Response(status_code=200, text=response_text)
    #     self.booru._get_counts = AsyncMock(return_value=(1, 1))
    #     self.booru._get_data = AsyncMock(return_value=[response])
    #     resp = asyncio.run(self.booru._get_all_json(tags='test'))
    #     self.assertEqual(len(resp), 2)

    @patch.object(Booru, '_get_all_data')
    @patch.object(Booru, '_get_counts')
    def test_get_all_json(self, mock_get_counts, mock_get_all_data):
        response_text = '[{"test": "test"},{"test": "test"}]'
        response = httpx.Response(status_code=200, text=response_text)
        mock_get_counts.return_value = 1, 1
        mock_get_all_data.return_value = [response]
        actual = asyncio.run(self.booru._get_all_json(tags='test'))
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual, [{'test': 'test'}, {'test': 'test'}])

    @patch.object(Booru, '_get_url_list')
    @patch.object(Booru, '_get_data')
    def test_get_page_json(self, mock_get_data, mock_get_url_list):
        mock_get_data.return_value = httpx.Response(status_code=200, text='[{"test": "test"}]')
        mock_get_url_list.return_value = ['test_url']
        actual = asyncio.run(self.booru._get_page_json(tags='test', page=1))
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual, [{"test": "test"}])

    @patch.object(Booru, '_get_counts')
    def test_count_facets(self, mock_get_counts):
        mock_get_counts.return_value = 1, 2
        actual = self.booru.count_facets()
        self.assertEqual(actual, {'pages': 1, 'posts': 2})

    def test_get_posts(self):
        actual = self.booru.get_posts()
        self.assertEqual(actual, [])
