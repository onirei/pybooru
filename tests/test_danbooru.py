import unittest

from pybooru import Danbooru, DanbooruImage

from .common import CommonTests

object_data = {
    "id": 1,
    "created_at": "2021-05-16T23:56:26.188-04:00",
    "uploader_id": 1,
    "score": 1,
    "source": "https://i.pximg.net/img-original/img/2021/05/15/09/19/57/89846340_p0.png",
    "md5": "0f70fd1225f836a95a27e1f5fbe71b8e",
    "last_comment_bumped_at": None,
    "rating": "s",
    "image_width": 1,
    "image_height": 1,
    "tag_string": "tags",
    "is_note_locked": False,
    "fav_count": 1,
    "file_ext": "png",
    "last_noted_at": None,
    "is_rating_locked": False,
    "parent_id": None,
    "has_children": False,
    "approver_id": None,
    "tag_count_general": 1,
    "tag_count_artist": 1,
    "tag_count_character": 1,
    "tag_count_copyright": 1,
    "file_size": 1,
    "is_status_locked": False,
    "pool_string": "",
    "up_score": 1,
    "down_score": 0,
    "is_pending": False,
    "is_flagged": False,
    "is_deleted": False,
    "tag_count": 1,
    "updated_at": "2021-05-17T12:50:50.673-04:00",
    "is_banned": False,
    "pixiv_id": 1,
    "last_commented_at": None,
    "has_active_children": False,
    "bit_flags": 1,
    "tag_count_meta": 1,
    "has_large": True,
    "has_visible_children": False,
    "tag_string_general": "tags",
    "tag_string_character": "tags",
    "tag_string_copyright": "tags",
    "tag_string_artist": "tags",
    "tag_string_meta": "tags",
    "file_url": "https://url_to_file.ext",
    "large_file_url": "https://url_to_large_file.ext",
    "preview_file_url": "https://url_to_preview_file.ext"
}


class DanbooruTestCase(CommonTests, unittest.TestCase):
    def setUp(self):
        self.booru = Danbooru(limit=10)
        self.image = DanbooruImage
        self.object_data = object_data
        self.count = '{"counts": {"posts": 11}}'
        self.page_increment = 1
        self.page_parameter = 'page'


class DanbooruImageTestCase(unittest.TestCase):
    def setUp(self):
        self.image = DanbooruImage(**object_data)
