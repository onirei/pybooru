import unittest

from pybooru import Yandere, YandereImage

from .common import CommonTests

object_data = {
    "id": 1,
    "tags": "tags",
    "created_at": 1,
    "updated_at": 1,
    "creator_id": 1,
    "approver_id": None,
    "author": "author",
    "change": 1,
    "source": "",
    "score": 2,
    "md5": "image_name",
    "file_size": 1,
    "file_ext": "png",
    "file_url": "https://file_url.ext",
    "is_shown_in_index": True,
    "preview_url": "https://preview_url.ext",
    "preview_width": 1,
    "preview_height": 1,
    "actual_preview_width": 1,
    "actual_preview_height": 1,
    "sample_url": "https://sample_url.ext",
    "sample_width": 1,
    "sample_height": 1,
    "sample_file_size": 1,
    "jpeg_url": "https://jpeg_url.ext",
    "jpeg_width": 1,
    "jpeg_height": 1,
    "jpeg_file_size": 1,
    "rating": "q",
    "is_rating_locked": False,
    "has_children": False,
    "parent_id": 1,
    "status": "status",
    "is_pending": False,
    "width": 1,
    "height": 1,
    "is_held": False,
    "frames_pending_string": "",
    "frames_pending": [],
    "frames_string": "",
    "frames": [],
    "is_note_locked": False,
    "last_noted_at": 0,
    "last_commented_at": 0
}


class YandereTestCase(CommonTests, unittest.TestCase):
    def setUp(self):
        self.booru = Yandere(limit=10)
        self.image = YandereImage
        self.object_data = object_data
        self.count = '<?xml version="1.0" encoding="UTF-8"?><posts count="11" offset="0"></posts>'
        self.page_increment = 1
        self.page_parameter = 'page'


class YandereImageTestCase(unittest.TestCase):
    def setUp(self):
        self.image = YandereImage(**object_data)