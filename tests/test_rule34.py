import unittest

from pybooru import Rule34, Rule34Image

from .common import CommonTests

object_data = {
    "preview_url": "https://url_to_preview_file.ext",
    "sample_url": "https://url_to_sample_file.ext",
    "file_url": "https://url_to_file.extg",
    "directory": "3139",
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
    "score": 1,
    "tags": "tags",
    "width": 1
}


class Rule34TestCase(CommonTests, unittest.TestCase):
    def setUp(self):
        self.booru = Rule34(limit=10)
        self.image = Rule34Image
        self.object_data = object_data
        self.count = '<?xml version="1.0" encoding="UTF-8"?><posts count="11" offset="0"></posts>'
        self.page_increment = 0
        self.page_parameter = 'pid'


class Rule34ImageTestCase(unittest.TestCase):
    def setUp(self):
        self.image = Rule34Image(**object_data)
