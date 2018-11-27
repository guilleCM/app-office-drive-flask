import mongoengine as db
import mongoengine_goodjson as gj


class BaseDocument(gj.Document):
    meta = {
        'abstract': True,
    }
