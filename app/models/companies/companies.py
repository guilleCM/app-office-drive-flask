from app import db
import mongoengine_goodjson as gj
from datetime import datetime


class Companies(gj.Document):
    name = db.StringField(unique=True)
    address = db.StringField()
    zip_code = db.StringField()
    city = db.StringField()
    tel = db.StringField()
    nif = db.StringField()
    c_date = db.DateTimeField(default=datetime.now())
    _active = db.BooleanField(default=True)
