import asyncio
from unittest.mock import AsyncMock

import httpx


class CommonTests(object):
    def test_get_counts(self):
        self.booru._get_data = AsyncMock(
            return_value=httpx.Response(status_code=200, text=self.count)
        )
        actual_pages, actual_posts = asyncio.run(self.booru._get_counts(tags='test'))
        self.assertEqual(actual_pages, 2)
        self.assertEqual(actual_posts, 11)
        self.booru.limit = 100
        actual_pages, actual_posts = asyncio.run(self.booru._get_counts(tags='test'))
        self.assertEqual(actual_pages, 1)
        self.assertEqual(actual_posts, 11)

    def test_get_url_list(self):
        actual = self.booru._get_url_list(page_count=2, tags='test')
        self.assertEqual(len(actual), 2)
        self.assertIn(f'{self.page_parameter}={0+self.page_increment}', actual[0])
        self.assertIn('tags=test', actual[0])
        self.assertIn(f'{self.page_parameter}={1+self.page_increment}', actual[-1])
        self.assertIn('tags=test', actual[-1])

    def test_get_posts(self):
        self.booru._get_page_json = AsyncMock(return_value=[self.object_data])
        self.booru._get_all_json = AsyncMock(return_value=[self.object_data])
        actual = self.booru.get_posts(tags='test')
        self.assertEqual(len(actual), 1)
        self.assertIs(type(actual[0]), self.image)
        actual = self.booru.get_posts(tags='test', page=1)
        self.assertEqual(len(actual), 1)
        self.assertIs(type(actual[0]), self.image)
        actual = self.booru.get_posts(tags='test', json=True)
        self.assertEqual(actual, [self.object_data])
        actual = self.booru.get_posts(tags='test', page=1, json=True)
        self.assertEqual(actual, [self.object_data])
