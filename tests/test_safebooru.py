import unittest

from pybooru import Safebooru, SafebooruImage

from .common import CommonTests

object_data = {
    "directory": "3375",
    "hash": "image_name",
    "height": 1,
    "id": 1,
    "image": "image.ext",
    "change": 1,
    "owner": "owner",
    "parent_id": 0,
    "rating": "rating",
    "sample": True,
    "sample_height": 1,
    "sample_width": 1,
    "score": 0,
    "tags": "tags",
    "width": 1
}


class SafebooruTestCase(CommonTests, unittest.TestCase):
    def setUp(self):
        self.booru = Safebooru(limit=10)
        self.image = SafebooruImage
        self.object_data = object_data
        self.count = '<?xml version="1.0" encoding="UTF-8"?><posts count="11" offset="0"></posts>'
        self.page_increment = 0
        self.page_parameter = 'pid'


class SafebooruImageTestCase(unittest.TestCase):
    def setUp(self):
        self.image = SafebooruImage(**object_data)
