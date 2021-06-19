import unittest

from pybooru import Gelbooru, GelbooruImage

from .common import CommonTests

object_data = {
            "source": "source",
            "directory": "d0/0c",
            "hash": "file_name",
            "height": 1,
            "id": 1,
            "image": "file_name_with_ext",
            "change": 1,
            "owner": "owner",
            "parent_id": None,
            "rating": "s",
            "sample": 0,
            "preview_height": 1,
            "preview_width": 1,
            "sample_height": 0,
            "sample_width": 0,
            "score": 1,
            "tags": "tags",
            "title": "",
            "width": 1,
            "file_url": "https://url_to_file.ext",
            "created_at": "Sun May 24 00:00:00 -0500 2020",
            "post_locked": 0
        }


class GelbooruTestCase(CommonTests, unittest.TestCase):
    def setUp(self):
        self.booru = Gelbooru(limit=10)
        self.image = GelbooruImage
        self.object_data = object_data
        self.count = '<?xml version="1.0" encoding="UTF-8"?><posts count="11" offset="0"></posts>'
        self.page_increment = 0
        self.page_parameter = 'pid'


class GelbooruImageTestCase(unittest.TestCase):
    def setUp(self):
        self.image = GelbooruImage(**object_data)

    def test_thumbnail(self):
        actual = self.image.thumbnail
        self.assertEqual(
            actual, 'https://img3.gelbooru.com/thumbnails/d0/0c/thumbnail_file_name.jpg'
        )
