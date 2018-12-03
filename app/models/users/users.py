from app import db
import mongoengine_goodjson as gj
from datetime import datetime
from app.models.companies.companies import Companies


class Roles(gj.Document):
    description = db.StringField()
    name = db.StringField()


class Users(gj.Document):
    username = db.StringField(unique=True)
    password = db.StringField()
    company_ref = db.ReferenceField(Companies, default=None)
    email = db.StringField()
    name = db.StringField()
    address = db.StringField()
    city = db.StringField()
    nif = db.StringField()
    tel = db.StringField()
    roles = db.ListField(db.ReferenceField(Roles), default=[])
    c_date = db.DateTimeField(default=datetime.now())
    _active = db.BooleanField(default=True)
